"""Run codeComp as the code-understanding engine and adapt its evidence graph.

The matching project owns this integration layer. codeComp source remains in its
own directory and is invoked through its documented command-line interface.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


EXCLUDED_PARTS = {"unit-test", "unit_test", "tests", "test", "stubs", "mocks", "mock"}


def _is_test_node(node: dict[str, Any]) -> bool:
    file_path = str((node.get("evidence") or {}).get("file") or "").replace("\\", "/")
    return any(part.lower() in EXCLUDED_PARTS for part in file_path.split("/"))


def production_graph(raw: Path, output: Path) -> Path:
    """Keep application functions before model enrichment to avoid test stubs."""
    graph = json.loads(raw.read_text(encoding="utf-8"))
    original_count = len(graph["nodes"])
    nodes = [node for node in graph["nodes"] if not _is_test_node(node)]
    ids = {node["id"] for node in nodes}
    for node in nodes:
        for key in ("callers", "callees"):
            node[key] = [value for value in node.get(key, []) if value in ids]
    graph["nodes"] = nodes
    graph["edges"] = [edge for edge in graph["edges"]
                      if edge.get("source") in ids and edge.get("target") in ids]
    graph["production_filter"] = {"original_nodes": original_count,
                                  "excluded_test_nodes": original_count - len(nodes)}
    output.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def source_revision(source: Path, graph_path: Path | None = None) -> str:
    digest = hashlib.sha256()
    files = sorted(path for path in source.rglob("*") if path.is_file() and path.suffix.lower() in {".c", ".h"})
    if not files and graph_path:
        return "graph-sha256:" + hashlib.sha256(graph_path.read_bytes()).hexdigest()
    for path in files:
        digest.update(path.relative_to(source).as_posix().encode("utf-8"))
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    tree_hash = "source-tree-sha256:" + digest.hexdigest()
    try:
        result = subprocess.run(
            ["git", "-c", f"safe.directory={source.as_posix()}", "-C", str(source), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip() + ";" + tree_hash
    except (OSError, subprocess.SubprocessError):
        return tree_hash


def verify_graph_source(graph_path: Path, source: Path) -> dict[str, int]:
    """Reject a reused graph whose cited function text differs from source."""
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    checked = 0
    truncated = 0
    cache: dict[Path, list[str]] = {}
    problems = []
    for node in graph.get("nodes", []):
        evidence = node.get("evidence") or {}
        rel = str(evidence.get("file") or "")
        excerpt = str(evidence.get("code") or "").strip()
        start = evidence.get("start_line")
        end = evidence.get("end_line")
        if not rel or not excerpt or not isinstance(start, int) or not isinstance(end, int):
            continue
        path = next((candidate for candidate in (source / rel, source / "src" / rel)
                     if candidate.is_file()), None)
        if path is None:
            problems.append(f"{rel}: missing file")
            continue
        if path not in cache:
            cache[path] = path.read_text(encoding="utf-8", errors="replace").splitlines()
        actual = "\n".join(cache[path][start - 1:end]).strip()
        normalized = excerpt.replace("\r\n", "\n")
        if actual == normalized:
            checked += 1
        elif actual.startswith(normalized):
            checked += 1
            truncated += 1
        else:
            problems.append(f"{rel}:{start}-{end}: excerpt differs")
    if problems:
        raise ValueError("Code graph/source mismatch: " + "; ".join(problems[:8]) +
                         (f"; +{len(problems) - 8} more" if len(problems) > 8 else ""))
    if checked == 0:
        raise ValueError("Code graph has no verifiable function excerpts")
    return {"checked": checked, "truncated_prefixes": truncated}


def run_codecomp(source: Path, tool_dir: Path, output: Path, *, backend: str = "clang",
                 prepare_build: bool = False, static_only: bool = False,
                 model: str = "", base_url: str = "", api_key: str = "",
                 concurrency: int = 4) -> Path:
    if not tool_dir.joinpath("extract_evidence.py").is_file() or not tool_dir.joinpath("llm_enrich.py").is_file():
        raise ValueError(f"codeComp 工具目录无效: {tool_dir}")
    if not source.is_dir():
        raise ValueError(f"源码目录不存在: {source}")
    raw = output / "raw_graph.json"
    enriched = output / "enriched_raw_graph.json"
    extract = [sys.executable, str(tool_dir / "extract_evidence.py"), "--root", str(source),
               "--out", str(raw), "--backend", backend]
    if prepare_build:
        extract.append("--prepare-build")
    subprocess.run(extract, cwd=tool_dir, check=True)
    if static_only:
        return raw
    production = production_graph(raw, output / "production_graph.json")
    enrich = [sys.executable, str(tool_dir / "llm_enrich.py"), "--input", str(production),
              "--output", str(enriched), "--concurrency", str(concurrency), "--retries", "2", "--resume"]
    if model:
        enrich += ["--model", model]
    if base_url:
        enrich += ["--base-url", base_url]
    env = os.environ.copy()
    if api_key:
        env["LLM_API_KEY"] = api_key
    subprocess.run(enrich, cwd=tool_dir, check=True, env=env)
    return enriched


def _io_text(entry: dict[str, Any]) -> str:
    name = str(entry.get("name", "")).strip()
    comment = str(entry.get("comment", "")).strip()
    return f"{name} {comment}".strip()


def adapt_graph(path: Path, source: Path, *, static_only: bool = False) -> dict[str, Any]:
    graph = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(graph.get("nodes"), list) or not isinstance(graph.get("edges"), list):
        raise ValueError("codeComp 图缺少 nodes 或 edges")
    parser = graph.get("parser", {})
    controls: dict[str, list[str]] = {}
    for edge in graph["edges"]:
        if edge.get("type") == "control" and edge.get("source") and edge.get("condition"):
            controls.setdefault(edge["source"], []).append(str(edge["condition"]))
    units = []
    hints: list[dict[str, str]] = []
    excluded = 0
    for node in graph["nodes"]:
        evidence = node.get("evidence") or {}
        if _is_test_node(node):
            excluded += 1
            continue
        description = str(node.get("description") or "").strip()
        if not description and not static_only:
            raise ValueError(f"富化图存在空描述节点: {node.get('id')}")
        comment = str(node.get("comment") or "").strip()
        inputs = [x for x in node.get("inputs", []) if isinstance(x, dict)]
        outputs = [x for x in node.get("outputs", []) if isinstance(x, dict)]
        summary = description or comment or str(node.get("name", ""))
        steps = [line.strip("-• ") for line in summary.splitlines() if line.strip("-• ")]
        symbol_names = set()
        for entry in inputs + outputs:
            name = str(entry.get("name", "")).strip()
            if name:
                if re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", name):
                    symbol_names.add(name)
                if entry.get("comment") and re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", name):
                    hints.append({"symbol": name, "comment": str(entry["comment"]),
                                  "source": str(node.get("id", ""))})
            for origin in entry.get("origins", []) or []:
                if isinstance(origin, str):
                    symbol_names.update(x for x in re.findall(r"[A-Za-z_]\w*", origin)
                                        if len(x) > 2 and x.lower() not in {"const", "sizeof", "struct", "uint32"})
        units.append({"id": node["id"], "name": node.get("name", ""),
                      "file": evidence.get("file", ""), "line_start": evidence.get("start_line"),
                      "line_end": evidence.get("end_line"), "summary": summary,
                      "conditions": sorted(set(controls.get(node["id"], []))),
                      "steps": steps, "reads": [_io_text(x) for x in inputs],
                      "writes": [_io_text(x) for x in outputs],
                      "outputs": [_io_text(x) for x in outputs], "errors": [],
                      "symbols": sorted(symbol_names),
                      "code_excerpt": str(evidence.get("code") or "")[:12000],
                      "callers": node.get("callers", []), "callees": node.get("callees", [])})
    index = graph.get("evidence_index") or {}
    for entry in index.get("globals", []):
        if entry.get("name") and entry.get("comment"):
            hints.append({"symbol": str(entry["name"]), "comment": str(entry["comment"]),
                          "source": "evidence_index.globals"})
    for struct in index.get("structs", []):
        for field in struct.get("fields", []):
            if field.get("name") and field.get("comment"):
                hints.append({"symbol": f"{struct.get('name', '')}.{field['name']}",
                              "comment": str(field["comment"]), "source": "evidence_index.structs"})
    has_source = any(path.is_file() for suffix in ("*.c", "*.h") for path in source.rglob(suffix))
    label = graph.get("repo_label") or source.name
    if label.lower() == "src" and source.name.lower() == "src":
        label = source.parent.name
    return {"project": label, "revision": source_revision(source, path),
            "configuration": parser.get("compilation_database") or "codeComp default build configuration",
            "units": units, "data_hints": hints,
            "graph": {"schema_version": graph.get("schema_version"), "backend": parser.get("backend"),
                      "diagnostic_count": len(parser.get("diagnostics", [])),
                      "source_checkout_available": has_source,
                      "node_count": len(units), "excluded_test_nodes": excluded,
                      "edge_count": len(graph["edges"]),
                      "static_only": static_only, "path": str(path)}}
