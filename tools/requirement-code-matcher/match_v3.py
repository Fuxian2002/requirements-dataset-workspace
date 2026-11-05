"""Source-aware, claim-wise matching experiment; no data dictionary.

The model extracts atomic claims and interprets bounded code evidence. The
program validates citations and derives binary step verdicts from claim states.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from candidate_index import CandidateIndex, tokens
from codecomp_bridge import adapt_graph
from llm_match import _chat, _unit_card, load_model_config
from main import extract_requirements
from report_v2 import render_report
from review_requirements import load_review
from source_units_v3 import SYMBOL, SourceUnits
from semantic_index import HybridIndex, LocalEmbedder
from structural_candidates import expand_functions, expand_macros

HINT_SYMBOL = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z_][A-Za-z0-9_]{3,}(?![A-Za-z0-9_])")


EXTRACT_PROMPT = """把需求处理步骤拆成最小、可独立核验的事实。只拆 step 原句，不把 title/description/condition 重述成额外事实，不补充新的规范要求。
每个事实的 kind：code=可由源码行为/配置验证，包括带前提的正向和否定行为；scope=仅说明证据边界或不作保证（如“不保证固定时延”）；
external=部署/流程等代码外义务；runtime=只能用实测证明的性能保证。
保留否定词、量词、前提条件、默认构型、时间与单位。表格参数要逐项保留；同类连续数值可合为一事实。
“不能把X误写为Y”或“不得把X等同于Y”若只是在说明解释边界，通常是 scope；“收到 OK 时逐次递减”是 code。
输出 JSON：{"claims":[{"id":"C1","text":"...","kind":"code|scope|external|runtime"}],
"search_terms":["可用于检索的英文标识符/函数主题，最多8个"]}。最多 12 个事实；不得省略关键动作、条件或数值。"""

JUDGE_PROMPT = """你是需求—源码证据审查员。只根据当前给出的源文件片段和 previous_evidence 判读。
逐个 claim_id 返回 supported、contradicted、unresolved。保持否定极性；不能把“没有 DLC”读成“有 DLC”。
正常路径需有明确动作、条件和结果证据；配置值要找到定义及使用；结构字段缺失只能在完整结构声明和相关传递路径都可见时受证。
需求明确指定芯片/驱动型号时，不得用同族其他型号的实现作证；必须引用指定型号或共用实现的实际调用链。
计数器必须先写出初次触发与重置后下一次触发的调用序号，再换算时间；若材料不足返回 unresolved。若 if 内重置为 0，且 if 后在每次调用末尾 ++，下一次调用从 1 开始，稳态间隔为阈值 N 次调用，不是 N+1 次。
函数名、注释、摘要相似不是实现证据。没有找到证据不是冲突。反例必须有具体条件和相反语句。若理由实际上说“与需求一致”，不得标 contradicted。“第 N 次调用后触发”按第 N 次调用完成了触发动作理解。
scope/external/runtime 事实不强求代码实现：status=unresolved，reason 说明验证边界；不要用它们抵消已证实代码行为。
引用须指向输入单元 id 和可见行号。输出 JSON：{"decisions":[{"claim_id":"C1", 
"status":"supported|contradicted|unresolved","evidence":[{"unit_id":"...","line_start":1,"line_end":2,"observation":"..."}],
"reason":"..."}],"remaining":"仍缺哪些必要的代码证据","search_hints":["可继续检索的符号，最多5个"]}。"""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_digest(root: Path) -> str:
    """Include source/config content in checkpoint identity, not just its path."""
    digestor = hashlib.sha256()
    suffixes = {".c", ".h", ".cpp", ".hpp", ".json", ".py", ".xml", ".yaml", ".yml"}
    excluded = {".git", ".venv", "build", ".static-evidence-build", "__pycache__"}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        rel = path.relative_to(root)
        if any(part in excluded for part in rel.parts):
            continue
        digestor.update(rel.as_posix().encode("utf-8"))
        digestor.update(hashlib.sha256(path.read_bytes()).digest())
    return digestor.hexdigest()


def checkpoint_key(inputs: dict[str, Any], req: dict[str, Any], step: dict[str, Any]) -> str:
    step_inputs = {k: v for k, v in inputs.items() if k != "document_sha256"}
    semantic_req = {k: v for k, v in req.items() if k not in {"heading_paragraph", "steps"}}
    semantic_req["steps"] = [{"id": s["id"], "text": s["text"]} for s in req["steps"]]
    semantic_step = {"id": step["id"], "text": step["text"]}
    return hashlib.sha256(json.dumps({**step_inputs, "req": semantic_req, "step": semantic_step},
                                     ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def compact(unit: dict[str, Any], query: str, focus: list[int] | None = None,
            max_lines: int = 75) -> dict[str, Any]:
    result = dict(unit)
    lines = unit.get("code_excerpt", "").splitlines()
    if len(lines) <= max_lines:
        return result
    first = int(unit["line_start"])
    cues = tokens(query)
    scores = []
    for offset, line in enumerate(lines):
        score = len(set(tokens(line)) & set(cues))
        if focus and first + offset in focus:
            score += 40
        scores.append(score)
    best = max(range(len(lines)), key=lambda i: scores[i])
    start = max(0, min(best - max_lines // 3, len(lines) - max_lines))
    result["line_start"] = first + start
    result["line_end"] = first + start + max_lines - 1
    result["code_excerpt"] = "\n".join(lines[start:start + max_lines])
    result["id"] = unit["id"] + f"#L{first + start}"
    return result


def function_source_path(root: Path, function: dict[str, Any]) -> Path:
    """Resolve codeComp's project-relative paths in both src and flat repos."""
    relative = Path(str(function.get("file", "")))
    direct = root / relative
    if direct.is_file():
        return direct
    return root / "src" / relative


def evidence_valid(items: Any, visible: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        try:
            start, end = int(item["line_start"]), int(item["line_end"])
        except (KeyError, ValueError, TypeError):
            continue
        requested_id = str(item.get("unit_id", ""))
        unit = visible.get(requested_id)
        if unit is None:
            unit = next((candidate for candidate in visible.values()
                         if candidate["id"].split("#L")[0] == requested_id
                         and int(candidate["line_start"]) <= start <= end <= int(candidate["line_end"])), None)
        if unit is None:
            continue
        lines = unit["code_excerpt"].splitlines()
        offset = start - int(unit["line_start"])
        if start > end or offset < 0 or end - int(unit["line_start"]) >= len(lines):
            continue
        if end - start > 14:
            continue
        out.append({"unit_id": unit["id"], "file": unit["file"],
                    "line_start": start, "line_end": end,
                    "observation": str(item.get("observation", ""))[:500],
                    "snippet": "\n".join(f"{n}: {lines[n-int(unit['line_start'])]}"
                                         for n in range(start, end + 1))})
    return out


def normalize_claims(raw: Any, step: dict[str, Any]) -> tuple[list[dict[str, str]], list[str]]:
    claims = []
    for item in raw.get("claims", []) if isinstance(raw, dict) else []:
        if not isinstance(item, dict) or not str(item.get("text", "")).strip():
            continue
        if re.match(r"^(?:本)?需求(?:为|是|描述|要求的是)", str(item["text"]).strip()):
            continue
        claims.append({"id": f"C{len(claims) + 1}", "text": str(item["text"]).strip()[:450],
                       "kind": item.get("kind") if item.get("kind") in {"code", "scope", "external", "runtime"} else "code"})
        if len(claims) >= 12:
            break
    if not claims:
        claims = [{"id": "C1", "text": step["text"], "kind": "code"}]
    terms = [str(x)[:80] for x in raw.get("search_terms", []) if isinstance(x, str)][:8]
    return claims, terms


def claim_input_text(req: dict[str, Any], step: dict[str, Any]) -> str:
    """Review the description once, together with the first processing step.

    The description often states the main obligation while the processing
    paragraph only states a caveat. Repeating that description for every step
    creates duplicate, unrelated claims in later steps.
    """
    text = str(step["text"]).strip()
    if req.get("reviewed_input"):
        return text
    first = req.get("steps", [{}])[0].get("id") == step.get("id")
    description = str(req.get("description", "")).strip()
    if first and description and description not in text:
        return description + "\n" + text
    return text


def claim_verdicts(claims: list[dict[str, str]], answer: dict[str, Any],
                   visible: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {c["id"]: c for c in claims}
    output = {c["id"]: {**c, "status": "unresolved", "evidence": [], "reason": "模型未返回有效判断"}
              for c in claims}
    for item in answer.get("decisions", []) if isinstance(answer, dict) else []:
        if not isinstance(item, dict) or item.get("claim_id") not in by_id:
            continue
        cid = item["claim_id"]
        evidence = evidence_valid(item.get("evidence"), visible)
        reported = item.get("status") if item.get("status") in {"supported", "contradicted", "unresolved"} else "unresolved"
        status = reported
        citation_issue = status != "unresolved" and not evidence
        if status != "unresolved" and not evidence:
            status = "unresolved"
        reason = str(item.get("reason", ""))[:900]
        if status == "contradicted" and any(phrase in reason for phrase in
                                             ("没有证据", "未找到", "未检索到", "未出现", "未在给定", "无法确认", "证据不足")):
            status = "unresolved"
        if status == "supported" and (re.search(r"(?:条件|前提|调用链|触发).{0,30}(?:未受证|未在|缺少|不完整|无法确认)", reason)
                                      or re.search(r"(?:缺少|未给出).{0,30}(?:条件|前提|调用链)", reason)):
            status = "unresolved"
        if by_id[cid]["kind"] != "code":
            status = "unresolved"
        output[cid] = {**by_id[cid], "status": status, "evidence": evidence,
                       "reason": reason, "reported_status": reported,
                       "citation_issue": citation_issue,
                       "proposed_unit_ids": [str(e.get("unit_id", "")) for e in
                                             (item.get("evidence") if isinstance(item.get("evidence"), list) else [])
                                             if isinstance(e, dict)]}
    return list(output.values())


def step_label(claims: list[dict[str, Any]]) -> tuple[str, str]:
    code = [c for c in claims if c["kind"] == "code"]
    if not code:
        return "not_matched", "outside_code_scope"
    statuses = [c["status"] for c in code]
    if "contradicted" in statuses:
        return "not_matched", "counterexample"
    if all(s == "supported" for s in statuses):
        return "matched", "matched"
    if "supported" in statuses:
        return "not_matched", "incomplete_evidence"
    return "not_matched", "not_found"


def audit_periodic_counters(decisions: list[dict[str, Any]],
                            visible: dict[str, dict[str, Any]]) -> None:
    """Resolve the common reset-then-increment off-by-one pattern from code."""
    units = list(visible.values())
    for claim in decisions:
        if claim["kind"] != "code" or "稳态间隔" not in claim["text"]:
            continue
        milliseconds = re.search(r"(?:为|约)\s*(\d+)\s*ms", claim["text"], re.I)
        seconds = re.search(r"(?:为|约)\s*(\d+(?:\.\d+)?)\s*s\b", claim["text"], re.I)
        target = int(milliseconds.group(1)) if milliseconds else (
            float(seconds.group(1)) * 1000 if seconds else None)
        if target is None:
            continue
        for function in units:
            period = re.search(r"Cyclic(\d+)ms", function.get("name", ""), re.I)
            if not period or function.get("kind") != "function":
                continue
            code = function["code_excerpt"]
            match = re.search(r"static\s+\w+\s+(\w*[Cc]ounter)\s*=\s*0\s*;", code)
            if not match:
                continue
            counter = match.group(1)
            condition = re.search(rf"if\s*\(\s*{re.escape(counter)}\s*==\s*(\w+)\s*\)", code)
            if not condition:
                continue
            symbol = condition.group(1)
            if not re.search(rf"{re.escape(counter)}\s*=\s*0\s*;", code[condition.end():]):
                continue
            if not re.search(rf"{re.escape(counter)}\s*\+\+", code[condition.end():]):
                continue
            macro = next(((u, re.search(rf"#\s*define\s+{re.escape(symbol)}\s*\(?\s*(\d+)u?\s*\)?",
                                        u["code_excerpt"])) for u in units
                          if re.search(rf"#\s*define\s+{re.escape(symbol)}\b", u["code_excerpt"])), None)
            if not macro or not macro[1]:
                continue
            threshold = int(macro[1].group(1))
            actual = threshold * int(period.group(1))
            if abs(actual - target) > max(1, target * 0.02):
                continue
            f_lines = function["code_excerpt"].splitlines()
            m_lines = macro[0]["code_excerpt"].splitlines()
            f_start = int(function["line_start"])
            m_start = int(macro[0]["line_start"])
            f_line = f_start + next(i for i, line in enumerate(f_lines) if symbol in line and "if" in line)
            m_line = m_start + next(i for i, line in enumerate(m_lines) if re.search(rf"#\s*define\s+{re.escape(symbol)}\b", line))
            citations = evidence_valid([{"unit_id": function["id"], "line_start": f_line,
                                         "line_end": min(f_line + 3, int(function["line_end"]))},
                                        {"unit_id": macro[0]["id"], "line_start": m_line,
                                         "line_end": m_line}], visible)
            claim["status"] = "supported"
            claim["reason"] = (f"程序复核：触发时计数清零，调用末尾递增；稳态下一轮从 1 开始，"
                               f"阈值 {threshold} × 任务周期 {period.group(1)} ms = {actual} ms。")
            claim["evidence"] = citations
            break


def aggregate_v3(requirements: list[dict[str, Any]], steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_step = {s["step_id"]: s for s in steps}
    result = []
    for req in requirements:
        ids = [s["id"] for s in req["steps"]]
        states = [by_step[sid]["verdict"] for sid in ids]
        count = states.count("matched")
        label = "matched" if states and count == len(states) else (
            "partial" if count else "unmatched")
        result.append({"requirement_id": req["id"], "title": req["title"],
                       "verdict": label, "matched_steps": count, "total_steps": len(ids),
                       "step_ids": ids, "matched_step_ids": [sid for sid in ids if by_step[sid]["verdict"] == "matched"],
                       "unmatched_step_ids": [sid for sid in ids if by_step[sid]["verdict"] != "matched"]})
    return result


def requirement_anchor_ids(req: dict[str, Any], baseline: dict[str, dict[str, Any]]) -> list[str]:
    """Promote functions cited by several matched steps of one requirement."""
    matched = [baseline[s["id"]] for s in req["steps"]
               if s["id"] in baseline and baseline[s["id"]].get("verdict") == "matched"]
    if len(matched) < 3:
        return []
    votes: dict[str, int] = {}
    for result in matched:
        cited = {str(e.get("unit_id", "")).split("#L")[0]
                 for e in result.get("evidence", [])
                 if str(e.get("unit_id", "")).startswith("func:")}
        for uid in cited:
            votes[uid] = votes.get(uid, 0) + 1
    minimum = max(3, (len(matched) + 1) // 2)
    return [uid for uid, count in sorted(votes.items(), key=lambda item: (-item[1], item[0]))
            if count >= minimum][:2]


def candidates(req: dict[str, Any], step: dict[str, Any], claims: list[dict[str, str]],
               search_terms: list[str], func_index: CandidateIndex, source_index: CandidateIndex,
               source_units: SourceUnits, baseline: dict[str, Any] | None,
               anchor_ids: list[str] | None = None,
               compact_lines: int = 75,
               structure_expand: bool = True) -> list[dict[str, Any]]:
    query = " ".join([req["title"], req["description"], req.get("processing", ""), step["text"],
                      *[c["text"] for c in claims if c["kind"] == "code"], *search_terms])
    code_claims = [c for c in claims if c["kind"] == "code"]
    functions = []
    seen = set()
    prior_ids = [str(e["unit_id"]).split("#L")[0]
                 for e in (baseline or {}).get("evidence", [])]
    by_id = {unit["id"]: unit for unit in func_index.units}
    for uid in prior_ids:
        if uid in by_id and uid not in seen:
            functions.append(by_id[uid]); seen.add(uid)
    for uid in anchor_ids or []:
        if uid in by_id and uid not in seen and applicable_variant(req, by_id[uid]):
            functions.append(by_id[uid]); seen.add(uid)
    for claim in code_claims:
        for pos, _ in func_index.rank(claim["text"] + " " + " ".join(search_terms))[:2]:
            unit = func_index.units[pos]
            if unit["id"] not in seen:
                functions.append(unit); seen.add(unit["id"])
            if len(functions) >= 18:
                break
        if len(functions) >= 18:
            break
    for pos, _ in func_index.rank(query)[:40]:
        unit = func_index.units[pos]
        if unit["id"] not in seen:
            functions.append(unit); seen.add(unit["id"])
        if len(functions) >= 18:
            break
    state_entries = []
    for unit in func_index.units:
        if unit["id"] in seen:
            continue
        name = str(unit.get("name", ""))
        score = 0
        if "预运行" in query and re.search(r"PreRunning|PreRun", name, re.I):
            score += 6
        if "初始化" in query and re.search(r"ProcessInitialization", name, re.I):
            score += 5
        if "状态机" in query and "LTC" in query and name == "LTC_Trigger" and applicable_variant(req, unit):
            score += 7
        if score and name.split("_")[0] in query:
            score += 3
        if score:
            state_entries.append((score, unit))
    state_entries.sort(key=lambda pair: (-pair[0], pair[1]["file"], pair[1]["line_start"]))
    if state_entries:
        preferred = [unit for _, unit in state_entries[:3]]
        functions = preferred + functions
        seen.update(unit["id"] for unit in preferred)
    # In a module with paired initialization/run entry points, lexical ranking
    # can return only the run function. Inspect a few same-file siblings whose
    # names express the requested operation, before generic lower-ranked hits.
    requested = query.casefold()
    sibling_files = {u["file"] for u in functions[:18]}
    siblings = []
    for unit in func_index.units:
        if unit["id"] in seen or unit["file"] not in sibling_files:
            continue
        name = str(unit.get("name", "")).casefold()
        score = 0
        if ("初始化" in requested or "initialize" in requested or " init" in requested) and "initialize" in name:
            score += 3
        if "预运行" in requested and "prerunning" in name:
            score += 4
        if "初始化" in requested and "processinitialization" in name:
            score += 4
        score += sum(2 for word in ("engine", "cyclic", "measurement", "diagnostic", "precharge")
                     if word in requested and word in name)
        if score >= 3:
            siblings.append((score, unit))
    siblings.sort(key=lambda pair: (-pair[0], pair[1]["file"], pair[1]["line_start"]))
    if siblings:
        preferred = [unit for _, unit in siblings[:4]]
        functions = preferred + functions
        seen.update(unit["id"] for unit in preferred)
    callers = []
    for callee in functions[:12]:
        name = str(callee.get("name", ""))
        if len(name) < 8:
            continue
        pattern = re.compile(rf"\b{re.escape(name)}\s*\(")
        for index in func_index.by_file.get(callee["file"], []):
            unit = func_index.units[index]
            if unit["id"] in seen or not pattern.search(unit.get("code_excerpt", "")):
                continue
            score = (4 if unit["file"] == callee["file"] else 0) + (
                len(set(tokens(query)) & set(tokens(unit.get("name", "")))))
            callers.append((score, unit))
    callers.sort(key=lambda pair: (-pair[0], pair[1]["file"], pair[1]["line_start"]))
    if callers:
        preferred = []
        for _, unit in callers:
            if unit["id"] not in seen:
                preferred.append(unit)
                seen.add(unit["id"])
            if len(preferred) >= 4:
                break
        functions = preferred + functions
    structure_query = step["text"] + " " + " ".join(search_terms)
    if structure_expand:
        structure_ranks = {func_index.units[pos]["id"]: rank + 1
                           for rank, (pos, _) in enumerate(func_index.rank(structure_query))}
        functions = expand_functions(functions, func_index.units, structure_query,
                                     ranked_ids=structure_ranks, by_file=func_index.by_file)
    function_text = " ".join(u.get("code_excerpt", "")[:2500] for u in functions[:10])
    source = hint_source_windows(search_terms, functions[:18], source_units.root, limit=8)
    source += [u for u in claim_source_windows(code_claims, functions[:18], source_units.root)
               if u["id"] not in {x["id"] for x in source}]
    sseen = {u["id"] for u in source}
    def add_source(unit: dict[str, Any]) -> None:
        if unit["id"] not in sseen:
            source.append(unit); sseen.add(unit["id"])
    def ranked_source(q: str, numbers: set[str], limit: int) -> list[dict[str, Any]]:
        scores = dict(source_index.rank(q)[:100])
        if any(len(n) >= 3 for n in numbers):
            for pos, unit in enumerate(source_index.units):
                if unit["kind"] in {"config", "source", "macro"} and any(
                    len(n) >= 3 and re.search(rf"\b{re.escape(n)}\b", unit["code_excerpt"])
                    for n in numbers):
                    scores.setdefault(pos, 0.0)
        ordered = sorted(scores, key=lambda pos: -(
            scores[pos] + sum(0.5 if len(n) >= 3 else 0.08 for n in numbers
                              if re.search(rf"\b{re.escape(n)}\b", source_index.units[pos]["code_excerpt"]))))
        return [source_index.units[pos] for pos in ordered[:limit]]
    for claim in code_claims:
        numbers = {x for x in re.findall(r"\b\d{2,}\b", claim["text"]) if int(x) >= 20}
        for unit in ranked_source(claim["text"] + " " + " ".join(search_terms), numbers, 2):
            add_source(unit)
    source_query = query + " " + str((baseline or {}).get("missing", ""))
    numbers = {x for x in re.findall(r"\b\d{2,}\b", step["text"]) if int(x) >= 20}
    for unit in ranked_source(source_query, numbers, 30):
        add_source(unit)
        if len(source) >= 30:
            break
    # Exact symbol references are stronger than broad co-occurrence in a long
    # function body. Keep both channels and avoid letting generic macros crowd out
    # direct value/config hits.
    for unit in source_units.expand_symbols(query + " " + function_text, 36):
        if unit["id"] not in sseen:
            source.append(unit); sseen.add(unit["id"])
        if len(source) >= 30:
            break
    # Follow definitions and config references around the best function and
    # value hits. This bridges a function graph to macros and generated config.
    relevant_paths = {"src/" + u["file"] for u in functions[:8]}
    modules = {Path(u["file"]).stem.split("_")[0] for u in functions[:8]}
    relevant_numbers = {x for x in re.findall(r"\b\d{2,}\b", query) if int(x) >= 20}
    adjacent = []
    seed_symbols = set(SYMBOL.findall(query))
    for unit in functions[:8] + source[:12]:
        seed_symbols.update(SYMBOL.findall(unit.get("code_excerpt", "")[:3500]))
        seed_symbols.update(SYMBOL.findall(unit.get("name", "")))
    for unit in source_units.units:
        if unit["id"] in sseen:
            continue
        path = unit["file"]
        stem = Path(path).stem.lower()
        same_file = path in relevant_paths
        same_module = any(len(m) >= 3 and m.lower() in stem for m in modules)
        referenced = set(SYMBOL.findall(unit["code_excerpt"])) & seed_symbols
        if not (same_file or same_module or (unit["kind"] in {"macro", "config"} and referenced)):
            continue
        score = (4 if same_file else 0) + (2 if same_module else 0)
        score += min(4, len(referenced))
        score += sum(2 for n in relevant_numbers if re.search(rf"\b{re.escape(n)}\b", unit["code_excerpt"]))
        score += len(set(tokens(query)) & set(tokens(unit["name"])))
        if unit["kind"] == "macro" and not same_module and not same_file:
            score -= 2
        if score >= 4:
            adjacent.append((score, unit))
    adjacent.sort(key=lambda pair: (-pair[0],
                                     -int(pair[1]["kind"] == "macro" and any(
                                         re.search(rf"\b{re.escape(n)}\b", pair[1]["name"])
                                         for n in relevant_numbers)),
                                     pair[1]["file"], pair[1]["line_start"]))
    # Insert high-value adjacent definitions early enough for the first round.
    for _, unit in adjacent[:10]:
        if unit["id"] not in sseen:
            source.insert(min(2, len(source)), unit)
            sseen.add(unit["id"])
    direct = []
    for unit in source_units.units:
        if unit["kind"] != "macro" or unit["id"] in sseen:
            continue
        name = unit["name"]
        stem = Path(unit["file"]).stem.lower()
        numeric_name = any(re.search(rf"(?:_|^)({re.escape(n)})(?:_|$)", name)
                           for n in relevant_numbers)
        direct_topic = any(word in name.lower() for word in ("diag", "voltage", "task", "cycle"))
        if numeric_name and any(m.lower() in stem for m in modules):
            direct.append((8, unit))
        elif direct_topic and any(sym in unit["code_excerpt"] for sym in
                                  (u["name"] for u in source[:8] if u["kind"] == "config")):
            direct.append((6, unit))
    direct.sort(key=lambda pair: (-pair[0], pair[1]["file"], pair[1]["line_start"]))
    source = [u for _, u in direct[:5]] + [u for u in source if u["id"] not in {x[1]["id"] for x in direct[:5]}]
    # Preserve cross-type diversity and keep a bounded pool for model calls.
    # A CAN ID table names numeric IDs, while the source uses symbolic names
    # for the ID, period and phase. Keep each definition group together.
    table_windows = can_id_definition_windows(step["text"], source_units)
    table_windows += limit_config_windows(step["text"], source_units)
    table_windows += can_endianness_windows(step["text"], source_units)
    table_windows += explicit_source_symbols(step["text"], source_units)
    table_windows += macro_context_windows(step["text"], source[:12], source_units)
    table_windows += pulse_scale_windows(step["text"], source_units)
    source = table_windows + [u for u in source if u["id"] not in {w["id"] for w in table_windows}]
    if structure_expand:
        macro_neighbors = expand_macros(functions, source_units.units, structure_query)
        preserved = max(12, len(table_windows))
        existing = {u["id"] for u in source[:preserved]}
        macro_neighbors = [u for u in macro_neighbors if u["id"] not in existing]
        macro_ids = {u["id"] for u in macro_neighbors}
        source = source[:preserved] + macro_neighbors + [
            u for u in source[preserved:] if u["id"] not in macro_ids]
    if anchor_ids:
        anchors_first = [by_id[uid] for uid in anchor_ids
                         if uid in by_id and applicable_variant(req, by_id[uid])]
        functions = anchors_first + [u for u in functions
                                     if u["id"] not in {a["id"] for a in anchors_first}]
    result = functions[:18] + source[:max(24, len(table_windows))]
    focus = [int(e["line_start"]) for e in (baseline or {}).get("evidence", [])]
    return [compact(u, query, focus if u["kind"] == "function" else None,
                    max_lines=compact_lines)
            for u in result]


def can_id_definition_windows(step_text: str, source_units: SourceUnits) -> list[dict[str, Any]]:
    ids = {int(value, 16) for value in re.findall(r"\b0x([0-9a-fA-F]{2,8})\b", step_text)}
    if not ids:
        return []
    found = []
    for unit in source_units.units:
        if unit["kind"] != "macro" or not unit["name"].endswith("_ID"):
            continue
        if "can_cfg_tx" not in unit["file"]:
            continue
        match = re.search(r"\(\s*0x([0-9a-fA-F]+)u?\s*\)", unit["code_excerpt"])
        if not match or int(match.group(1), 16) not in ids:
            continue
        path = source_units.root / unit["file"]
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        start = int(unit["line_start"])
        end = min(len(lines), start + 5)
        found.append({"id": f"source:{unit['file']}:{start}:can-id", "name": unit["name"],
                      "file": unit["file"], "line_start": start, "line_end": end,
                      "kind": "source", "summary": unit["name"], "conditions": [],
                      "code_excerpt": "\n".join(lines[start - 1:end]), "callers": [], "callees": []})
    return found[:16]


def limit_config_windows(step_text: str, source_units: SourceUnits) -> list[dict[str, Any]]:
    if "表格参数" not in step_text or not all(x in step_text for x in ("MOL", "RSL", "MSL")):
        return []
    found = []
    for path in sorted((source_units.root / "conf" / "bms").glob("*_cfg.json")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        groups: dict[str, list[int]] = {}
        for number, line in enumerate(lines, 1):
            match = re.search(r'"name"\s*:\s*"([A-Z][A-Z0-9_]*_(?:MOL|RSL|MSL)_[A-Za-z0-9]+)"', line)
            if match:
                group = re.sub(r"_(?:MOL|RSL|MSL)_", "_LIMIT_", match.group(1))
                groups.setdefault(group, []).append(number)
        for group, numbers in groups.items():
            if len(numbers) < 3 or max(numbers) - min(numbers) > 30:
                continue
            start, end = min(numbers), min(len(lines), max(numbers) + 2)
            rel = path.relative_to(source_units.root).as_posix()
            found.append({"id": f"config:{rel}:{start}:limit-group", "name": group,
                          "file": rel, "line_start": start, "line_end": end,
                          "kind": "config", "summary": group, "conditions": [],
                          "code_excerpt": "\n".join(lines[start - 1:end]), "callers": [], "callees": []})
    return found[:12]


def can_endianness_windows(step_text: str, source_units: SourceUnits) -> list[dict[str, Any]]:
    if "引导程序" not in step_text or not any(x in step_text for x in ("CAN_LITTLE_ENDIAN", "CAN_BIG_ENDIAN")):
        return []
    matches = [u for u in source_units.units if u["kind"] == "source"
               and u["file"].startswith("src/bootloader/")
               and u["file"].endswith("/can_cfg.c")
               and "CAN_LITTLE_ENDIAN" in u["code_excerpt"]
               and any(name in u["code_excerpt"] for name in ("can_rxMessages", "can_txMessages"))]
    return matches[:3]


def explicit_source_symbols(step_text: str, source_units: SourceUnits) -> list[dict[str, Any]]:
    names = set(re.findall(r"(?<![A-Za-z0-9_])(?:[A-Z][A-Za-z0-9]*|[a-z][a-z0-9]+)_[A-Za-z0-9_]{6,}(?![A-Za-z0-9_])", step_text))
    found = []
    seen = set()
    for name in sorted(names):
        for unit in source_units.by_symbol.get(name, []):
            if unit["kind"] not in {"source_function", "default_config"} or unit["id"] in seen:
                continue
            found.append(compact(unit, step_text, max_lines=100))
            seen.add(unit["id"])
            if len(found) >= 8:
                return found
    return found


def macro_context_windows(step_text: str, selected: list[dict[str, Any]],
                          source_units: SourceUnits, limit: int = 5) -> list[dict[str, Any]]:
    """Show adjacent definitions when one configuration macro is retrieved.

    Channel mappings and derived bounds are often several consecutive defines;
    individual one-line macro cards hide the relationship from the judge.
    """
    chosen = []
    seen = set()
    for name in SYMBOL.findall(step_text):
        for unit in source_units.by_symbol.get(name, [])[:1]:
            if unit["kind"] == "macro" and unit["id"] not in seen:
                chosen.append(unit); seen.add(unit["id"])
    for unit in selected:
        if unit["kind"] == "macro" and unit["id"] not in seen:
            chosen.append(unit); seen.add(unit["id"])
    chosen.sort(key=lambda u: (0 if u["name"] in step_text else 1,
                               len(Path(u["file"]).parts), u["file"], u["line_start"]))
    windows = []
    for unit in chosen:
        if len(windows) >= limit:
            break
        path = source_units.root / unit["file"]
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        center = int(unit["line_start"])
        if any(w["file"] == unit["file"] and
               w["line_start"] <= center <= w["line_end"] for w in windows):
            continue
        start, end = max(1, center - 5), min(len(lines), center + 6)
        windows.append({"id": f"source:{unit['file']}:{start}:macro-context",
                        "name": unit["name"], "file": unit["file"],
                        "line_start": start, "line_end": end, "kind": "source",
                        "summary": f"Nearby definitions for {unit['name']}",
                        "conditions": [], "code_excerpt": "\n".join(lines[start - 1:end]),
                        "callers": [], "callees": []})
    return windows


def pulse_scale_windows(step_text: str, source_units: SourceUnits) -> list[dict[str, Any]]:
    """Retrieve unit conversion next to PWM output scaling when microseconds matter."""
    if not re.search(r"(?:μs|µs|微秒|\bus\b)", step_text, re.I):
        return []
    macros = source_units.by_symbol.get("SCALE_FOR_PWM_OUT", [])
    if not macros:
        return []
    path = source_units.root / macros[0]["file"]
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    hits = [int(macros[0]["line_start"])]
    hits += [i for i, line in enumerate(lines, 1)
             if "SCALE_FOR_PWM_OUT" in line and
             ("ms" in line.lower() or "udb_pwOut" in line)][:2]
    out = []
    for hit in hits:
        start, end = max(1, hit - 2), min(len(lines), hit + 7)
        if any(u["line_start"] <= hit <= u["line_end"] for u in out):
            continue
        out.append({"id": f"source:{macros[0]['file']}:{start}:pulse-scale",
                    "name": "SCALE_FOR_PWM_OUT", "file": macros[0]["file"],
                    "line_start": start, "line_end": end, "kind": "source",
                    "summary": "PWM output unit conversion and timer use",
                    "conditions": [], "code_excerpt": "\n".join(lines[start - 1:end]),
                    "callers": [], "callees": []})
    timing = [i for i, line in enumerate(lines, 1) if "T4CONbits.TCKPS" in line]
    if timing:
        start, end = max(1, timing[0] - 3), min(len(lines), timing[-1] + 4)
        out.append({"id": f"source:{macros[0]['file']}:{start}:timer-prescaler",
                    "name": "Timer 4 prescaler", "file": macros[0]["file"],
                    "line_start": start, "line_end": end, "kind": "source",
                    "summary": "PWM output timer prescaler", "conditions": [],
                    "code_excerpt": "\n".join(lines[start - 1:end]),
                    "callers": [], "callees": []})
    for symbol in ("MIPS", "FCY"):
        defining = next((u for u in source_units.by_symbol.get(symbol, [])
                         if u["file"] != macros[0]["file"] and u["kind"] == "macro"), None)
        if not defining:
            continue
        definition_path = source_units.root / defining["file"]
        definition_lines = definition_path.read_text(encoding="utf-8", errors="replace").splitlines()
        center = int(defining["line_start"])
        start, end = max(1, center - 3), min(len(definition_lines), center + 8)
        out.append({"id": f"source:{defining['file']}:{start}:timer-clock",
                    "name": symbol, "file": defining["file"],
                    "line_start": start, "line_end": end, "kind": "source",
                    "summary": f"Timer clock definition {symbol}", "conditions": [],
                    "code_excerpt": "\n".join(definition_lines[start - 1:end]),
                    "callers": [], "callees": []})
    return out


def claim_source_windows(claims: list[dict[str, Any]], functions: list[dict[str, Any]],
                         root: Path, limit: int = 8) -> list[dict[str, Any]]:
    """Expose claim-relevant lines inside long functions before LLM review."""
    found = []
    seen = set()
    indexed = []
    for function in functions:
        if int(function["line_end"]) - int(function["line_start"]) < 90:
            continue
        path = function_source_path(root, function)
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        first, last = int(function["line_start"]), min(int(function["line_end"]), len(lines))
        indexed.append((function, path, lines, first, last,
                        [set(tokens(lines[n - 1])) for n in range(first, last + 1)]))
    for claim in claims:
        terms = {t for t in tokens(claim["text"]) if t.isascii() and len(t) >= 3}
        if not terms:
            continue
        best = None
        for function, path, lines, first, last, line_terms_list in indexed:
            for offset, line_terms in enumerate(line_terms_list):
                number = first + offset
                score = len(terms & line_terms)
                if score and (best is None or score > best[0]):
                    best = (score, function, path, lines, number)
        if best is None:
            continue
        _, function, path, lines, hit = best
        start, end = max(int(function["line_start"]), hit - 8), min(int(function["line_end"]), hit + 12)
        key = (path, start)
        if key in seen:
            continue
        seen.add(key)
        rel = path.relative_to(root).as_posix()
        found.append({"id": f"source:{rel}:{start}:claim", "name": function["name"],
                      "file": rel, "line_start": start, "line_end": end,
                      "kind": "source", "summary": f"{function['name']} · {claim['text'][:100]}",
                      "conditions": [], "code_excerpt": "\n".join(lines[start - 1:end]),
                      "callers": [], "callees": []})
        if len(found) >= limit:
            break
    return found


def hint_functions(hints: Any, functions: list[dict[str, Any]],
                   seen_ids: set[str], limit: int = 6) -> list[dict[str, Any]]:
    """Follow exact source symbol hints from the first evidence review."""
    if not isinstance(hints, list):
        return []
    by_name: dict[str, list[dict[str, Any]]] = {}
    for unit in functions:
        by_name.setdefault(str(unit.get("name", "")), []).append(unit)
    found = []
    for hint in hints:
        if not isinstance(hint, str):
            continue
        for symbol in HINT_SYMBOL.findall(hint):
            for unit in by_name.get(symbol, []):
                if unit["id"] in seen_ids:
                    continue
                found.append(unit)
                seen_ids.add(unit["id"])
                if len(found) >= limit:
                    return found
            callers = [u for u in functions if u["id"] not in seen_ids and
                       re.search(rf"\b{re.escape(symbol)}\b", u.get("code_excerpt", ""))]
            callers.sort(key=lambda u: (0 if "Process" in u.get("name", "") or "Trigger" in u.get("name", "") else 1,
                                        u["file"], u["line_start"]))
            for unit in callers[:2]:
                found.append(unit)
                seen_ids.add(unit["id"])
                if len(found) >= limit:
                    return found
    return found


def hint_source_windows(hints: Any, selected_functions: list[dict[str, Any]],
                        root: Path, limit: int = 6) -> list[dict[str, Any]]:
    """Expose source lines around exact hints inside already selected functions."""
    if not isinstance(hints, list):
        return []
    symbols = [s for hint in hints if isinstance(hint, str) for s in HINT_SYMBOL.findall(hint)]
    found = []
    seen = set()
    for symbol in symbols:
        pattern = rf"\b(?:[A-Za-z0-9]+_)*{re.escape(symbol)}\b"
        for function in selected_functions:
            relative = Path(str(function.get("file", "")))
            path = function_source_path(root, function)
            if not path.is_file() or (path, symbol) in seen:
                continue
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            first = int(function["line_start"])
            last = min(int(function["line_end"]), len(lines))
            matches = [n for n in range(first, last + 1)
                       if re.search(pattern, lines[n - 1])
                       and not lines[n - 1].lstrip().startswith(("//", "*", "#"))]
            if not matches:
                continue
            def hit_score(number: int) -> int:
                line = lines[number - 1]
                return (4 if re.search(rf"\bcase\s+{re.escape(symbol)}\b", line) else 0) + (
                    3 if re.search(rf"\bsubstate\s*==\s*{re.escape(symbol)}\b", line) else 0) + (
                    1 if "(" in line else 0)
            hit = max(matches, key=lambda n: (hit_score(n), -n))
            start, end = max(first, hit - 8), min(last, hit + 12)
            excerpt = "\n".join(lines[start - 1:end])
            rel = path.relative_to(root).as_posix()
            found.append({"id": f"source:{rel}:{start}:{symbol}", "name": symbol,
                          "file": rel, "line_start": start, "line_end": end,
                          "kind": "source", "summary": f"{symbol} in {function['name']}",
                          "conditions": [], "code_excerpt": excerpt,
                          "callers": [], "callees": []})
            seen.add((path, symbol))
            break
        if len(found) >= limit:
            break
    return found


def hint_source_units(hints: Any, source_units: SourceUnits, limit: int = 6) -> list[dict[str, Any]]:
    if not isinstance(hints, list):
        return []
    found = []
    seen = set()
    for hint in hints:
        if not isinstance(hint, str):
            continue
        for symbol in HINT_SYMBOL.findall(hint):
            for unit in source_units.by_symbol.get(symbol, []):
                if unit["id"] not in seen:
                    found.append(unit)
                    seen.add(unit["id"])
                    if len(found) >= limit:
                        return found
    return found


def applicable_variant(req: dict[str, Any], unit: dict[str, Any]) -> bool:
    """Reject evidence from a sibling LTC driver when a variant is explicit."""
    match = re.search(r"\bLTC(\d{4}(?:-\d)?)\b", str(req.get("description", "")), re.I)
    if not match:
        return True
    path_variant = re.search(r"/ltc/(\d{4}(?:-\d)?)/", "/" + str(unit.get("file", "")).replace("\\", "/"), re.I)
    return path_variant is None or path_variant.group(1).casefold() == match.group(1).casefold()


def repair_missing_citations(req: dict[str, Any], step: dict[str, Any],
                             decisions: list[dict[str, Any]],
                             visible: dict[str, dict[str, Any]],
                             config: dict[str, str]) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    """Retry only claims the model called supported but cited invalid lines."""
    pending = [c for c in decisions if c.get("kind") == "code" and c.get("status") == "unresolved"
               and c.get("reported_status") == "supported" and c.get("citation_issue")]
    if not pending:
        return decisions, None
    proposed = {uid for c in pending for uid in c.get("proposed_unit_ids", [])}
    available = [u for u in visible.values() if applicable_variant(req, u)]
    selected = [u for u in available if u["id"] in proposed]
    selected += [u for u in available if u["kind"] == "source" and u["id"].count(":") >= 3
                 and u not in selected]
    selected += [u for u in available if u["kind"] == "source" and u not in selected]
    selected += [u for u in available if u not in selected]
    selected = selected[:12]
    answer, usage = _chat(config, JUDGE_PROMPT + "\n本轮只修复前次无效引用。必须从以下 numbered_source 重选直接包含动作与条件的行；没有则 unresolved。",
                          {"requirement": {"id": req["id"], "title": req["title"]},
                           "step": step["text"],
                           "claims": [{"id": c["id"], "text": c["text"], "kind": c["kind"]}
                                      for c in pending],
                           "previous_decisions": [{"claim_id": c["id"], "reason": c["reason"],
                                                   "invalid_unit_ids": c.get("proposed_unit_ids", [])}
                                                  for c in pending],
                           "code_units": [_unit_card(u, detailed=True) for u in selected]}, 1600)
    repaired = {c["id"]: c for c in claim_verdicts(pending, answer,
                                                   {u["id"]: u for u in selected})}
    return [repaired[c["id"]] if c["id"] in repaired and repaired[c["id"]]["status"] == "supported"
            else c for c in decisions], usage


def judge(req: dict[str, Any], step: dict[str, Any], claims: list[dict[str, str]],
          pool: list[dict[str, Any]], config: dict[str, str], max_rounds: int = 2,
          all_functions: list[dict[str, Any]] | None = None,
          source_root: Path | None = None,
          source_units: SourceUnits | None = None,
          economy: bool = False) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    # Keep a small first batch in economy mode; later rounds add new evidence.
    funcs = [u for u in pool if u.get("kind") == "function" and applicable_variant(req, u)]
    sources = [u for u in pool if u.get("kind") != "function" and applicable_variant(req, u)]
    rounds = ([funcs[:4] + sources[:6], funcs[4:8] + sources[6:12],
               funcs[8:16] + sources[12:24], []] if economy else
              [funcs[:8] + sources[:12], funcs[8:16] + sources[12:24], [], []])
    visible: dict[str, dict[str, Any]] = {}
    usages = []
    latest: dict[str, Any] = {}
    merged: dict[str, dict[str, Any]] = {}
    for round_index in range(min(max_rounds, len(rounds))):
        group = rounds[round_index]
        if not group:
            continue
        visible.update({u["id"]: u for u in group})
        answer, usage = _chat(config, JUDGE_PROMPT,
                              {"requirement": {"id": req["id"], "title": req["title"],
                                               "description": req["description"], "condition": req["condition"]},
                               "step": step["text"], "claims": claims,
                               "previous_evidence": [e for c in merged.values() for e in c.get("evidence", [])],
                               "previous_decisions": [{"claim_id": c["id"], "status": c["status"], "reason": c["reason"]}
                                                      for c in merged.values()],
                               "code_units": [_unit_card(u, detailed=True) for u in group]}, 2600)
        if round_index + 1 < max_rounds and all_functions:
            hinted = hint_functions(answer.get("search_hints"),
                                    [u for u in all_functions if applicable_variant(req, u)],
                                    set(visible) | {u["id"] for u in rounds[round_index + 1]})
            full_by_id = {u["id"]: u for u in all_functions}
            selected_full = [full_by_id.get(u["id"].split("#L")[0], u) for u in funcs]
            windows = hint_source_windows(answer.get("search_hints"), selected_full,
                                          source_root) if source_root else []
            exact_source = hint_source_units(answer.get("search_hints"), source_units) if source_units else []
            existing_ids = set(visible) | {u["id"] for u in rounds[round_index + 1]}
            fresh_windows = [u for u in windows if u["id"] not in existing_ids]
            fresh_source = [u for u in exact_source if u["id"] not in existing_ids]
            rounds[round_index + 1] = ([compact(u, step["text"]) for u in hinted] +
                                       fresh_source + fresh_windows + rounds[round_index + 1])
        usages.append(usage)
        latest = answer
        for c in claim_verdicts(claims, answer, visible):
            old = merged.get(c["id"])
            if old and old["status"] in {"supported", "contradicted"} and c["status"] == "unresolved":
                continue
            merged[c["id"]] = c
        current = [merged.get(c["id"], {**c, "status": "unresolved", "evidence": []}) for c in claims]
        if step_label(current)[0] == "matched" or step_label(current)[1] == "counterexample":
            break
    decisions = [merged.get(c["id"], {**c, "status": "unresolved", "evidence": [], "reason": "未审查"})
                 for c in claims]
    for claim in decisions:
        if claim["kind"] == "code" and claim["status"] == "supported" and claim.get("evidence"):
            if any(not applicable_variant(req, e) for e in claim["evidence"]):
                claim.update(status="unresolved", reason="引用了需求指定型号之外的驱动实现；需核对适用型号源码。",
                             reported_status="supported", citation_issue=True,
                             proposed_unit_ids=[e["unit_id"] for e in claim["evidence"]])
    if max_rounds > 1:
        decisions, repair_usage = repair_missing_citations(req, step, decisions, visible, config)
        if repair_usage is not None:
            usages.append(repair_usage)
    audit_periodic_counters(decisions, visible)
    verdict, reason = step_label(decisions)
    evidence = list({(e["unit_id"], e["line_start"], e["line_end"]): e
                     for c in decisions for e in c.get("evidence", [])}.values())
    missing = "；".join(c["id"] + " " + c["text"] for c in decisions
                       if c["kind"] == "code" and c["status"] == "unresolved")[:900]
    if reason == "counterexample":
        missing = "存在带源码证据的相反事实；需人工复核适用条件。" + missing
    output = {"step_id": step["id"], "text": step["text"], "verdict": verdict,
              "reason_kind": reason, "candidate_count": len(pool),
              "inspected_count": len(visible), "inspected_ids": list(visible),
              "claims": decisions, "evidence": evidence, "missing": missing,
              "verification": None, "usage": usages,
              "search_hints": latest.get("search_hints", [])}
    return output, list(visible.values())


def main() -> None:
    ap = argparse.ArgumentParser(description="Source-aware claim-wise matching V3")
    ap.add_argument("--document", type=Path, required=True)
    ap.add_argument("--graph", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--model-env", type=Path, required=True)
    ap.add_argument("--model", default="deepseek-flash")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--baseline", type=Path, help="旧结果仅作为检索提示；不沿用旧判定")
    ap.add_argument("--limit-steps", type=int, default=0)
    ap.add_argument("--only-steps", nargs="*", default=[])
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--max-rounds", type=int, choices=[1, 2, 3, 4], default=2)
    ap.add_argument("--compact-lines", type=int, default=75,
                    help="Experimental source-line cap; smaller windows can require more rounds")
    ap.add_argument("--economy", action="store_true",
                    help="Experimental: start with four functions and six source units")
    ap.add_argument("--embedding-model", type=Path,
                    help="Local Hugging Face embedding model directory; enables hybrid function retrieval")
    ap.add_argument("--embedding-weight", type=float, default=1.0,
                    help="Semantic channel weight in reciprocal-rank fusion (default: 1.0)")
    ap.add_argument("--no-structure-expand", action="store_true",
                    help="Disable bounded codeComp call-graph and macro candidate expansion")
    ap.add_argument("--checkpoint-from", type=Path, help="Reuse valid per-step checkpoints from a previous output directory")
    ap.add_argument("--reviewed-input", type=Path,
                    help="Pre-match requirement and atomic-step review JSON")
    args = ap.parse_args()
    if args.compact_lines < 12:
        ap.error("--compact-lines must be at least 12")
    if args.embedding_weight <= 0:
        ap.error("--embedding-weight must be positive")
    args.output.mkdir(parents=True, exist_ok=True)
    extracted = extract_requirements(args.document)
    review = load_review(args.reviewed_input, args.document) if args.reviewed_input else None
    if review:
        extracted["requirements"] = review["requirements"]
    graph = adapt_graph(args.graph, args.source)
    for u in graph["units"]:
        u["kind"] = "function"
    extra = SourceUnits(args.source)
    indexed_source = [u for u in extra.units if u["kind"] not in {"source_function", "default_config"} or
                      any(part.casefold() == "config" for part in Path(u["file"]).parts) or
                      u["file"].startswith("conf/")]
    graph_locations = {(u["file"], u["line_start"]) for u in graph["units"]}
    fallback_functions = [u for u in extra.units if u["kind"] == "source_function"
                          and (u["file"], u["line_start"]) not in graph_locations]
    f_index = CandidateIndex(graph["units"] + fallback_functions)
    s_index = CandidateIndex(indexed_source)
    if args.embedding_model:
        embedder = LocalEmbedder(args.embedding_model.resolve())
        f_index = HybridIndex(f_index, embedder, args.embedding_model.resolve(),
                              args.output / "embedding_function_index.json",
                              args.embedding_weight)
    config = load_model_config(args.model_env, args.model)
    baseline = {}
    if args.baseline:
        raw = json.loads(args.baseline.read_text(encoding="utf-8"))
        if raw.get("graph_sha256") != digest(args.graph) or (raw.get("source_sha256") and
                raw["source_sha256"] != source_digest(args.source)):
            ap.error("基线的代码图或源码哈希不匹配")
        current_steps = {s["id"]: (r["id"], s["text"])
                         for r in extracted["requirements"] for s in r["steps"]}
        old_steps = {s["id"]: (r["id"], s["text"])
                     for r in raw.get("input_requirements", []) for s in r.get("steps", [])}
        baseline = {s["step_id"]: s for s in raw["steps"]
                    if s["step_id"] in current_steps and
                    old_steps.get(s["step_id"], (None,))[0] == current_steps[s["step_id"]][0]}
    unchanged_baseline = {sid: result for sid, result in baseline.items()
                          if current_steps[sid] == old_steps.get(sid)} if args.baseline else {}
    anchors = {r["id"]: requirement_anchor_ids(r, unchanged_baseline)
               for r in extracted["requirements"]}
    tasks = [(r, s) for r in extracted["requirements"] for s in r["steps"]]
    if args.only_steps:
        tasks = [(r, s) for r, s in tasks if s["id"] in set(args.only_steps)]
    if args.limit_steps:
        tasks = tasks[:args.limit_steps]
    selected_ids = {s["id"] for _, s in tasks}
    requirements = [{**r, "steps": [s for s in r["steps"] if s["id"] in selected_ids]}
                    for r in extracted["requirements"] if any(s["id"] in selected_ids for s in r["steps"])]
    prompt_hash = hashlib.sha256((EXTRACT_PROMPT + JUDGE_PROMPT +
                                  "retrieval-v3.39-revision-evidence-hints").encode("utf-8")).hexdigest()
    inputs = {"document_sha256": extracted["sha256"], "graph_sha256": digest(args.graph),
              "source_sha256": source_digest(args.source),
              "source": str(args.source), "model": config["model"], "prompt_hash": prompt_hash,
              "max_rounds": args.max_rounds, "compact_lines": args.compact_lines,
              "economy": args.economy,
              "retrieval": ("hybrid-rrf-lexical8-v2" if args.embedding_model else "lexical-v3") +
                           ("+structure-v1" if not args.no_structure_expand else ""),
              "embedding_model": str(args.embedding_model.resolve()) if args.embedding_model else None,
              "embedding_identity": f_index.identity if args.embedding_model else None,
              "embedding_weight": args.embedding_weight if args.embedding_model else None}
    checkpoint_dir = args.output / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)
    prior_checkpoint_dir = args.checkpoint_from / "checkpoints" if args.checkpoint_from else None
    def run_one(req: dict[str, Any], step: dict[str, Any]):
        # A change to another requirement must not invalidate this step.
        key = checkpoint_key(inputs, req, step)
        path = checkpoint_dir / (re.sub(r"[^A-Za-z0-9_-]", "_", step["id"]) + ".json")
        checkpoint_paths = [path]
        if prior_checkpoint_dir is not None:
            checkpoint_paths.append(prior_checkpoint_dir / path.name)
        for candidate_path in checkpoint_paths:
            if not candidate_path.exists():
                continue
            cached = json.loads(candidate_path.read_text(encoding="utf-8"))
            if cached.get("fingerprint") == key:
                if candidate_path != path:
                    path.write_text(candidate_path.read_text(encoding="utf-8"), encoding="utf-8")
                return cached["result"], cached.get("units", []), True
        review_text = claim_input_text(req, step)
        raw_claims, claim_usage = _chat(config, EXTRACT_PROMPT,
                                        {"step": review_text}, 1800)
        claims, terms = normalize_claims(raw_claims, {**step, "text": review_text})
        pool = candidates(req, step, claims, terms, f_index, s_index, extra,
                          baseline.get(step["id"]), anchors[req["id"]], args.compact_lines,
                          not args.no_structure_expand)
        result, inspected = judge(req, step, claims, pool, config, args.max_rounds,
                                  f_index.units, args.source, extra, args.economy)
        result["usage"].insert(0, claim_usage)
        result["search_terms"] = terms
        result["structural_candidate_ids"] = [u["id"] for u in pool
                                               if str(u.get("retrieval_origin", "")).startswith("structure:")]
        path.write_text(json.dumps({"fingerprint": key, "result": result,
                                    "units": inspected}, ensure_ascii=False, indent=2), encoding="utf-8")
        return result, inspected, False
    results = {}
    cached_ids = set()
    used_units: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(run_one, req, step): step["id"] for req, step in tasks}
        for future in as_completed(futures):
            sid = futures[future]
            result, inspected, cached = future.result()
            results[sid] = result
            if cached:
                cached_ids.add(sid)
            used_units.update({u["id"]: u for u in inspected})
            print(f"[v3] {len(results)}/{len(tasks)} {sid} {result['verdict']}"
                  f" {'cached' if cached else ''}", flush=True)
    steps = [results[s["id"]] for r, s in tasks]
    summary = aggregate_v3(requirements, steps)
    payload = {**inputs, "document": str(args.document), "graph": str(args.graph),
               "input_requirements": requirements,
               "reviewed_input": str(args.reviewed_input) if args.reviewed_input else None,
               "baseline": str(args.baseline) if args.baseline else None,
               "source_unit_count": len(extra.units), "function_count": len(graph["units"]),
               "requirements": summary, "steps": steps,
               "usage_total": sum(u.get("total_tokens", 0) for s in steps for u in s["usage"]),
               "usage_this_run": sum(u.get("total_tokens", 0) for s in steps
                                     if s["step_id"] not in cached_ids for u in s["usage"]),
               "cached_steps": len(cached_ids)}
    (args.output / "matches_v3.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    display_units = graph["units"] + [u for uid, u in used_units.items() if uid not in {g["id"] for g in graph["units"]}]
    render_report(args.output / "report_v3.html", summary, steps, display_units,
                  scope_note="逐事实源码补证 V3；模型回答经行号校验，最终标签由程序汇总",
                  json_name="matches_v3.json", metadata=payload)
    print(json.dumps({"requirements": len(summary), "steps": len(steps),
                      "labels": {k: sum(r["verdict"] == k for r in summary)
                                 for k in ("matched", "partial", "unmatched")},
                      "usage_total": payload["usage_total"],
                      "usage_this_run": payload["usage_this_run"],
                      "cached_steps": payload["cached_steps"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
