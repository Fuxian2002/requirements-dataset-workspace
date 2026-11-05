#!/usr/bin/env python3
"""Generate function descriptions without modifying static graph evidence."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Dict, List, NamedTuple, Optional, Set, Tuple

from static_evidence_core.text import read_text


PROMPT_FILENAMES = {
    "description_system": "description_system.md",
    "group_summary_system": "group_summary_system.md",
}


class PromptTemplates(NamedTuple):
    description_system: str
    group_summary_system: str


def load_prompt_templates(prompt_root: Path) -> PromptTemplates:
    """Load the required LLM system prompts from the configured prompts folder."""
    contents = {}
    for key, filename in PROMPT_FILENAMES.items():
        path = prompt_root / filename
        if not path.is_file():
            raise RuntimeError(f"prompt template not found: {path}")
        content = read_text(path).strip()
        if not content:
            raise RuntimeError(f"prompt template is empty: {path}")
        contents[key] = content
    return PromptTemplates(**contents)


def _get_env(key: str, fallback: str = "") -> str:
    """Read LLM_* settings, falling back to compatible OPENAI_* names."""
    return os.environ.get(key) or os.environ.get(key.replace("LLM_", "OPENAI_")) or fallback


def read_dotenv(script_dir: Path) -> Dict[str, str]:
    """Read local LLM settings without overriding the process environment."""
    path = script_dir / ".env"
    if not path.is_file():
        return {}
    values: Dict[str, str] = {}
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key in {
            "LLM_MODEL",
            "LLM_BASE_URL",
            "LLM_API_KEY",
            "LLM_MAX_CONCURRENCY",
            "LLM_MAX_RETRIES",
        }:
            values[key] = value.strip().strip('"').strip("'")
    return values


def _get_env_int(key: str, fallback: int) -> int:
    """Read an integer LLM_* setting, falling back to OPENAI_* and a default."""
    value = _get_env(key).strip()
    if not value:
        return fallback
    try:
        return int(value)
    except ValueError:
        return fallback


def internal_callees(node: dict, function_ids: Set[str]) -> List[str]:
    """Return direct callees already represented by function nodes in this graph."""
    return sorted({callee for callee in node.get("callees", []) if callee in function_ids})


def estimate_tokens(value: str) -> int:
    """Conservatively estimate tokens without assuming a provider-specific tokenizer."""
    cjk_chars = sum("\u4e00" <= char <= "\u9fff" for char in value)
    return max(1, cjk_chars + (len(value) - cjk_chars + 3) // 4)


def make_context_card(node: dict, description: str) -> dict:
    """Keep static I/O verbatim while making a callee description addressable."""
    return {
        "function_id": node["id"],
        "name": node.get("name", ""),
        "description": description,
        "direct_inputs": node.get("inputs", []),
        "direct_outputs": node.get("outputs", []),
        "source_comment": node.get("comment", ""),
    }


def render_context_entries(items: List[dict]) -> str:
    """Render context cards or grouped summaries as one shared Markdown structure
    (``- <id> <name>`` heading plus an indented ``  - 功能：...`` line), matching the
    group-summary output format so description context and summary input stay isomorphic."""
    lines: List[str] = []
    for item in items:
        if "function_id" in item:
            identity = " ".join(part for part in (item.get("function_id"), item.get("name")) if part)
            body = item.get("description", "").strip() or "功能未提供"
        else:
            member_ids = item.get("function_ids", [])
            identity = f"{item.get('group_id', '')}（包含：{'、'.join(member_ids)}）"
            body = item.get("summary", "").strip() or "功能未提供"
        lines.append(f"- {identity}")
        lines.append(f"  - 功能：{body}")
    return "\n".join(lines)


def pack_by_token_budget(items: List[dict], budget: int) -> List[List[dict]]:
    """Pack complete items in stable order; never split or drop an item."""
    groups: List[List[dict]] = []
    current: List[dict] = []
    current_tokens = 0
    for item in items:
        item_tokens = estimate_tokens(render_context_entries([item]))
        if current and current_tokens + item_tokens > budget:
            groups.append(current)
            current = []
            current_tokens = 0
        current.append(item)
        current_tokens += item_tokens
    if current:
        groups.append(current)
    return groups


def split_base_field(expr: str) -> Tuple[str, str]:
    """Split ``x.y`` / ``*x->y`` / ``x->y[i]`` into (base, field)."""
    text = expr.strip().lstrip("*")
    match = re.search(r"([A-Za-z_]\w*)\s*(?:\.|->)\s*([A-Za-z_]\w*)", text)
    if match:
        return match.group(1), match.group(2)
    return text, ""


def collect_io_symbols(node: dict, evidence_index: dict) -> Tuple[List[str], Dict[str, Set[str]]]:
    """Derive the symbol dictionary scope from node I/O instead of the whole source.

    Returns ``(global_names, {struct_name: {field_name}})``:
    - a bare input/output name that matches a global -> that global variable;
    - an instance member ``inst.field`` -> the instance's struct type + field;
    - an IP-function member ``pIp->field`` -> the node's ``ip_struct`` + field.
    """
    globals_by_name = {item.get("name"): item for item in evidence_index.get("globals", [])}
    instance_type = {item.get("name"): item.get("type") for item in evidence_index.get("instances", [])}
    struct_names = {item.get("name") for item in evidence_index.get("structs", [])}
    ip_struct = node.get("ip_struct") or ""
    used_globals: Set[str] = set()
    struct_fields: Dict[str, Set[str]] = {}

    def add_struct(name: str, field: str = "") -> None:
        if name not in struct_names:
            return
        struct_fields.setdefault(name, set())
        if field:
            struct_fields[name].add(field)

    for key in ("inputs", "outputs"):
        for item in node.get(key, []):
            name = item.get("name", "") or ""
            via = item.get("via", "") or name
            if name in globals_by_name:
                used_globals.add(name)
            if "." in via or "->" in via:
                base, field = split_base_field(via)
                if base in instance_type:
                    if base in globals_by_name:
                        used_globals.add(base)
                    add_struct(instance_type[base], field)
                elif ip_struct:
                    add_struct(ip_struct, field)
    return sorted(used_globals), struct_fields


def render_symbol_dictionary(node: dict, evidence_index: dict) -> str:
    """Render the symbol dictionary for this function's I/O.

    The scope comes from ``inputs``/``outputs`` (not the whole source): the
    global variables referenced there, plus the structs behind instance/IP
    member accesses.  Each entry is rendered as ``代码名：需求名称`` with the
    requirement/business name taken from the declaration comment (e.g.
    ``attiang：控制姿态角 [deg] (phi, theta, psi)``), so the model can translate
    identifiers without guessing.
    """
    used_globals, struct_fields = collect_io_symbols(node, evidence_index)
    if not used_globals and not struct_fields:
        return "（无）"
    globals_by_name = {item.get("name"): item for item in evidence_index.get("globals", [])}
    structs_by_name = {item.get("name"): item for item in evidence_index.get("structs", [])}
    lines: List[str] = []
    if used_globals:
        lines.append("全局变量：")
        for name in used_globals:
            comment = (globals_by_name.get(name) or {}).get("comment", "") or ""
            lines.append(f"- {name}：{comment}" if comment else f"- {name}")
    if struct_fields:
        lines.append("结构体：")
        for struct_name in sorted(struct_fields):
            struct = structs_by_name.get(struct_name) or {}
            comment = struct.get("comment", "") or ""
            lines.append(f"- {struct_name}：{comment}" if comment else f"- {struct_name}")
            fields_by_name = {field.get("name"): field for field in struct.get("fields", [])}
            for field_name in sorted(struct_fields[struct_name]):
                field = fields_by_name.get(field_name) or {}
                detail_parts = []
                if field.get("comment"):
                    detail_parts.append(field["comment"])
                if field.get("role"):
                    detail_parts.append(f"({field['role']})")
                detail = " ".join(detail_parts)
                lines.append(f"  - {field_name}：{detail}" if detail else f"  - {field_name}")
    return "\n".join(lines)


def build_description_message(node: dict, callee_context: str, evidence_index: dict) -> str:
    """Build a prompt from direct source evidence, the symbol dictionary and
    completed callee summaries."""
    return "\n".join((
        "# 当前函数注释",
        node.get("comment", "") or "（无）",
        "",
        "# 当前函数源码",
        "```c",
        node.get("evidence", {}).get("code", ""),
        "```",
        "",
        "# 数据字典（当前函数输入/输出引出的全局变量与结构体）",
        render_symbol_dictionary(node, evidence_index),
        "",
        "# 已生成的直接被调函数说明（仅作调用语义上下文）",
        callee_context,
    ))


def build_group_summary_message(group: List[dict], depth: int) -> str:
    """Ask for a loss-aware summary that keeps every function independently named."""
    return "\n".join((
        f"# 第 {depth} 层调用上下文分组",
        "以下是完整条目。请压缩功能说明，但不得删除任一条目的函数 ID、函数名或功能说明。",
        render_context_entries(group),
    ))


def summarize_group(
    group: List[dict],
    depth: int,
    model: str,
    api_key: str,
    base_url: str,
    dry_run: bool,
    group_summary_system_prompt: str,
    request_description: Callable[[List[dict], str, str, str], Tuple[Optional[str], str]],
) -> Tuple[Optional[str], str]:
    """Summarize a complete group, returning an error instead of dropping context."""
    if dry_run:
        names = ", ".join(item.get("name", item.get("function_id", "")) for item in group)
        return f"（dry-run：第 {depth} 层分组摘要，包含：{names}）", ""
    print(
        f"group-summary [gen] 第 {depth} 层分组摘要（{len(group)} 条）",
        file=sys.stderr,
    )
    started_at = time.monotonic()
    summary, error = request_description(
        [
            {"role": "system", "content": group_summary_system_prompt},
            {"role": "user", "content": build_group_summary_message(group, depth)},
        ],
        model,
        api_key,
        base_url,
    )
    if summary is not None and summary.strip():
        print(
            f"group-summary [ok] 第 {depth} 层分组摘要（{time.monotonic() - started_at:.1f}s）",
            file=sys.stderr,
        )
    return summary, error


def build_budgeted_callee_context(
    node: dict,
    node_by_id: Dict[str, dict],
    descriptions: Dict[str, str],
    function_ids: Set[str],
    context_window_tokens: int,
    reserved_output_tokens: int,
    model: str,
    api_key: str,
    base_url: str,
    dry_run: bool,
    request_description: Callable[[List[dict], str, str, str], Tuple[Optional[str], str]],
    group_summary_system_prompt: str,
    evidence_index: dict,
) -> Tuple[Optional[str], dict, str]:
    """Use full cards when possible; otherwise summarize complete stable groups."""
    callee_ids = [callee_id for callee_id in internal_callees(node, function_ids) if callee_id in descriptions]
    cards = [make_context_card(node_by_id[callee_id], descriptions[callee_id]) for callee_id in callee_ids]
    base_message = build_description_message(node, "", evidence_index)
    budget = context_window_tokens - reserved_output_tokens - estimate_tokens(base_message)
    trace = {"callee_ids": callee_ids, "mode": "direct", "groups": []}
    if budget <= 0:
        return None, trace, "current function source exceeds the configured context budget"
    direct_context = render_context_entries(cards) if cards else "（无已生成的工程内被调函数说明）"
    if estimate_tokens(direct_context) <= budget:
        return direct_context, trace, ""

    trace["mode"] = "grouped"
    items = cards
    depth = 1
    group_budget = max(256, budget // 2)
    while depth <= 4:
        groups = pack_by_token_budget(items, group_budget)
        summaries: List[dict] = []
        for group_index, group in enumerate(groups, start=1):
            summary, error = summarize_group(
                group,
                depth,
                model,
                api_key,
                base_url,
                dry_run,
                group_summary_system_prompt,
                request_description,
            )
            if summary is None or not summary.strip():
                return None, trace, error or "empty group summary"
            function_ids_in_group = []
            for item in group:
                function_ids_in_group.extend(item.get("function_ids", [item.get("function_id", "")]))
            summaries.append({
                "group_id": f"depth-{depth}-group-{group_index}",
                "function_ids": function_ids_in_group,
                "summary": summary.strip(),
            })
        trace["groups"].append(summaries)
        context = render_context_entries(summaries)
        if estimate_tokens(context) <= budget:
            return context, trace, ""
        items = summaries
        depth += 1

    return None, trace, "group summaries still exceed the configured context budget"


def cyclic_components(
    pending: Set[str],
    node_by_id: Dict[str, dict],
    function_ids: Set[str],
) -> List[List[str]]:
    """Find recursive call groups from existing ``callees`` with Tarjan's algorithm."""
    index = 0
    stack: List[str] = []
    stack_members: Set[str] = set()
    indexes: Dict[str, int] = {}
    lowlinks: Dict[str, int] = {}
    components: List[List[str]] = []

    def visit(node_id: str) -> None:
        nonlocal index
        indexes[node_id] = index
        lowlinks[node_id] = index
        index += 1
        stack.append(node_id)
        stack_members.add(node_id)
        for callee_id in internal_callees(node_by_id[node_id], function_ids):
            if callee_id not in pending:
                continue
            if callee_id not in indexes:
                visit(callee_id)
                lowlinks[node_id] = min(lowlinks[node_id], lowlinks[callee_id])
            elif callee_id in stack_members:
                lowlinks[node_id] = min(lowlinks[node_id], indexes[callee_id])
        if lowlinks[node_id] != indexes[node_id]:
            return
        component: List[str] = []
        while stack:
            member = stack.pop()
            stack_members.remove(member)
            component.append(member)
            if member == node_id:
                break
        if len(component) > 1 or node_id in internal_callees(node_by_id[node_id], function_ids):
            components.append(sorted(component))

    for node_id in sorted(pending):
        if node_id not in indexes:
            visit(node_id)
    return components


def call_llm(messages: List[dict], model: str, api_key: str, base_url: str) -> tuple[Optional[str], str]:
    payload = json.dumps({"model": model, "messages": messages, "temperature": 0}).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=600.0) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"], ""
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, KeyError, OSError, ValueError) as exc:
        return None, f"LLM request failed: {exc}"


def write_graph_checkpoint(graph: dict, path: Path) -> None:
    """Atomically persist completed descriptions so a later run can resume."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    temporary_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary_path.replace(path)


def merge_checkpoint_descriptions(graph: dict, checkpoint: dict) -> int:
    """Copy completed descriptions from a prior checkpoint into fresh static evidence."""
    descriptions = {
        node.get("id"): str(node.get("description", "")).strip()
        for node in checkpoint.get("nodes", [])
        if node.get("id") and str(node.get("description", "")).strip()
    }
    restored = 0
    for node in graph.get("nodes", []):
        description = descriptions.get(node.get("id"))
        if description:
            node["description"] = description
            restored += 1
    return restored


def enrich_graph(
    graph: dict,
    model: str,
    api_key: str,
    base_url: str,
    dry_run: bool,
    prompt_dir: Optional[Path],
    prompts_dir: Optional[Path] = None,
    checkpoint_path: Optional[Path] = None,
    context_window_tokens: int = 64000,
    reserved_output_tokens: int = 1500,
    resume: bool = False,
    request_description: Callable[[List[dict], str, str, str], Tuple[Optional[str], str]] = call_llm,
    context_store: Optional[dict] = None,
    max_concurrency: int = 1,
    retries: int = 0,
) -> dict:
    """Generate descriptions from leaves upward using existing node ``callees``."""
    templates = load_prompt_templates(
        prompts_dir or Path(__file__).resolve().parent / "prompts"
    )
    enriched = dict(graph)
    nodes = [dict(node) for node in graph.get("nodes", [])]
    if prompt_dir is not None:
        prompt_dir.mkdir(parents=True, exist_ok=True)

    node_by_id = {
        node.get("id"): node
        for node in nodes
        if node.get("id")
    }
    function_ids = set(node_by_id)
    if context_store is not None:
        context_store.update({
            "schema_version": "1.0",
            "context_window_tokens": context_window_tokens,
            "reserved_output_tokens": reserved_output_tokens,
            "cards": {},
            "nodes": {},
        })
    descriptions = {
        node_id: str(node.get("description", "")).strip()
        for node_id, node in node_by_id.items()
        if resume and str(node.get("description", "")).strip()
    }
    for node in node_by_id.values():
        if not resume:
            node["description"] = ""
    if context_store is not None:
        context_store["cards"].update({
            node_id: make_context_card(node_by_id[node_id], description)
            for node_id, description in descriptions.items()
        })

    pending = {
        node_id
        for node_id, node in node_by_id.items()
        if node.get("evidence", {}).get("code", "").strip() and node_id not in descriptions
    }
    failed: Set[str] = set()
    if retries > 0 and not dry_run:
        base_request = request_description

        def retrying_request(messages: List[dict], model: str, api_key: str, base_url: str):
            last_error = ""
            for attempt in range(retries + 1):
                result, error = base_request(messages, model, api_key, base_url)
                if result is not None and result.strip():
                    return result, ""
                last_error = error
                if attempt < retries:
                    print(
                        f"[retry] 第 {attempt + 1}/{retries} 次重试（{error or 'empty response'}）",
                        file=sys.stderr,
                    )
                    time.sleep(2.0 * (attempt + 1))
            return None, last_error

        request_description = retrying_request

    lock = threading.Lock()
    sequence = 0
    max_workers = max(1, max_concurrency)

    def generate_many(node_ids: List[str], cyclic: bool) -> None:
        """Generate a dependency-free batch, concurrently when configured."""
        if max_workers <= 1:
            for node_id in node_ids:
                generate(node_id, cyclic)
            return
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(executor.map(lambda node_id: generate(node_id, cyclic), node_ids))

    def generate(node_id: str, cyclic: bool) -> bool:
        nonlocal sequence
        node = node_by_id[node_id]
        context, trace, context_error = build_budgeted_callee_context(
            node,
            node_by_id,
            descriptions,
            function_ids,
            context_window_tokens,
            reserved_output_tokens,
            model,
            api_key,
            base_url,
            dry_run,
            request_description,
            templates.group_summary_system,
            graph.get("evidence_index", {}),
        )
        if context is None:
            print(f"{node_id} [skip] {context_error}", file=sys.stderr)
            failed.add(node_id)
            return False
        if context_store is not None:
            context_store["nodes"][node_id] = trace
        message = build_description_message(node, context, graph.get("evidence_index", {}))
        with lock:
            sequence += 1
            safe_name = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in node["name"])
            prefix = f"{sequence:03d}_{safe_name}"
        if prompt_dir is not None:
            (prompt_dir / f"{prefix}_description_prompt.md").write_text(
                f"# System\n\n{templates.description_system}\n\n# User\n\n{message}\n",
                encoding="utf-8",
            )
        if dry_run:
            descriptions[node_id] = "（dry-run：该函数描述将在实际富化时生成）"
            return True

        suffix = "（循环调用初版）" if cyclic else ""
        mode = trace.get("mode", "direct")
        context_info = f"{len(trace.get('callee_ids', []))} 个被调函数" if mode == "direct" else "分组摘要上下文"
        print(f"{node_id} [gen]{suffix} {node['name']}（{context_info}）", file=sys.stderr)
        started_at = time.monotonic()
        description, error = request_description(
            [
                {"role": "system", "content": templates.description_system},
                {"role": "user", "content": message},
            ],
            model,
            api_key,
            base_url,
        )
        if description is None or not description.strip():
            print(f"{node_id} [skip]{suffix} {error or 'empty description'}", file=sys.stderr)
            failed.add(node_id)
            return False

        node["description"] = description.strip()
        print(f"{node_id} [ok]{suffix} {node['name']}（{time.monotonic() - started_at:.1f}s）", file=sys.stderr)
        descriptions[node_id] = node["description"]
        if checkpoint_path is not None:
            with lock:
                enriched["nodes"] = nodes
                write_graph_checkpoint(enriched, checkpoint_path)
        if context_store is not None:
            context_store["cards"][node_id] = make_context_card(node, node["description"])
        if prompt_dir is not None:
            (prompt_dir / f"{prefix}_description_response.md").write_text(
                node["description"],
                encoding="utf-8",
            )
        return True

    while pending:
        ready = sorted(
            node_id for node_id in pending
            if all(callee_id in descriptions for callee_id in internal_callees(node_by_id[node_id], function_ids))
        )
        if ready:
            for node_id in ready:
                pending.remove(node_id)
            generate_many(ready, cyclic=False)
            continue

        blocked = sorted(
            node_id for node_id in pending
            if any(callee_id in failed for callee_id in internal_callees(node_by_id[node_id], function_ids))
        )
        if blocked:
            for node_id in blocked:
                pending.remove(node_id)
                failed.add(node_id)
                print(f"{node_id} [skip] waiting for a failed callee description", file=sys.stderr)
            continue

        components = cyclic_components(pending, node_by_id, function_ids)
        cycle = sorted({node_id for component in components for node_id in component})
        if not cycle:
            raise RuntimeError("description scheduler stalled without a recursive call group")
        print(
            "Cycle detected; generating source-based initial descriptions for: " + ", ".join(cycle),
            file=sys.stderr,
        )
        for node_id in cycle:
            pending.remove(node_id)
        generate_many(cycle, cyclic=True)

    if failed and not dry_run:
        raise RuntimeError(
            "description generation did not complete for: " + ", ".join(sorted(failed))
        )

    enriched["nodes"] = nodes
    enriched.pop("semantic_candidates", None)
    return enriched


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate function descriptions for a direct static graph.")
    parser.add_argument("--input", "-i", required=True, help="Input raw graph JSON.")
    parser.add_argument("--output", "-o", default=None, help="Output graph JSON.")
    parser.add_argument("--model", default="", help="LLM model name.")
    parser.add_argument("--base-url", default="", help="API base URL.")
    parser.add_argument("--api-key", default="", help="API key.")
    parser.add_argument("--dry-run", action="store_true", help="Write prompts without calling the model.")
    parser.add_argument("--prompt-dir", default=None, help="Directory for description prompts and responses.")
    parser.add_argument(
        "--prompts-dir",
        default=None,
        help="Directory containing the required system-prompt templates.",
    )
    parser.add_argument(
        "--context-window-tokens",
        type=int,
        default=16000,
        help="Model context-window budget used for complete cards or grouped summaries.",
    )
    parser.add_argument(
        "--reserved-output-tokens",
        type=int,
        default=1500,
        help="Output-token budget reserved before placing callee context into a prompt.",
    )
    parser.add_argument(
        "--context-output",
        default=None,
        help="Separate JSON path for context cards and grouped-summary provenance.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse non-empty descriptions from an existing output checkpoint and generate only remaining nodes.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=None,
        help="Maximum number of functions generated in parallel per dependency-free batch "
        "(default: LLM_MAX_CONCURRENCY, or 1 when unset).",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=None,
        help="Retries per LLM request before it is marked failed "
        "(default: LLM_MAX_RETRIES, or 0 when unset).",
    )
    args = parser.parse_args()

    in_path = Path(args.input).resolve()
    if not in_path.is_file():
        parser.error(f"input not found: {in_path}")
    out_path = Path(args.output).resolve() if args.output else in_path.parent / f"enriched_{in_path.name}"
    script_dir = Path(__file__).resolve().parent
    dotenv = read_dotenv(script_dir)
    model = args.model or _get_env("LLM_MODEL", dotenv.get("LLM_MODEL", "gpt-4o-mini"))
    base_url = args.base_url or _get_env("LLM_BASE_URL", dotenv.get("LLM_BASE_URL", "https://api.openai.com/v1"))
    api_key = args.api_key or _get_env("LLM_API_KEY", dotenv.get("LLM_API_KEY", ""))
    if not api_key and not args.dry_run:
        parser.error("LLM_API_KEY or --api-key is required unless --dry-run is used")
    if args.context_window_tokens <= 0 or args.reserved_output_tokens < 0:
        parser.error("context token budgets must be non-negative, and the context window must be positive")
    max_concurrency = args.concurrency if args.concurrency is not None else _get_env_int("LLM_MAX_CONCURRENCY", 1)
    retries = args.retries if args.retries is not None else _get_env_int("LLM_MAX_RETRIES", 0)
    if max_concurrency < 1:
        parser.error("--concurrency must be at least 1")
    if retries < 0:
        parser.error("--retries must be non-negative")

    prompt_dir = Path(args.prompt_dir).resolve() if args.prompt_dir else out_path.parent / "llm_logs" / time.strftime("%Y%m%d-%H%M%S")
    prompts_dir = Path(args.prompts_dir).resolve() if args.prompts_dir else script_dir / "prompts"
    graph = json.loads(read_text(in_path))
    if args.resume and out_path.is_file():
        checkpoint = json.loads(read_text(out_path))
        restored = merge_checkpoint_descriptions(graph, checkpoint)
        print(f"Resuming from checkpoint {out_path} ({restored} descriptions restored)")
    context_store: dict = {}
    try:
        enriched = enrich_graph(
            graph,
            model,
            api_key,
            base_url,
            args.dry_run,
            prompt_dir,
            prompts_dir=prompts_dir,
            checkpoint_path=None if args.dry_run else out_path,
            context_window_tokens=args.context_window_tokens,
            reserved_output_tokens=args.reserved_output_tokens,
            resume=args.resume,
            context_store=context_store,
            max_concurrency=max_concurrency,
            retries=retries,
        )
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.dry_run:
        print(f"[dry-run] 未写回输出：{out_path}（提示词已生成于 {prompt_dir}）")
        return 0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
    context_path = (
        Path(args.context_output).resolve()
        if args.context_output
        else out_path.with_name(f"{out_path.stem}_context.json")
    )
    context_path.write_text(json.dumps(context_store, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"Wrote {context_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
