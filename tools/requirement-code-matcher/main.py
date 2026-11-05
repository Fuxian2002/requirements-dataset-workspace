"""Single-DOCX requirement extraction and auditable code-candidate retrieval.

This module was written for the current project; it shares no source code with
the earlier requirement_stitcher experiment.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from codecomp_bridge import adapt_graph, run_codecomp
from llm_match import load_model_config, match_project


FIELD_PATTERN = re.compile(r"^\s*([a-fA-F])\s*[.．、]\s*(需求标识|功能描述|调用条件|输入|输出|处理)\s*[:：]\s*(.*)$")
STEP_PATTERN = re.compile(r"^\s*(?:[（(]\d+[）)]|\d+[.．、])\s*(.*)$")
FIGURE_CAPTION_PATTERN = re.compile(r"^图\s*\d+(?:[.．-]\d+)*\s+[^。；：:]{1,60}$")
IDENTIFIER_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")
WORD_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]+|[\u4e00-\u9fff]{2,}")
STOP_WORDS = {"NOT_FOUND", "NASA", "AOCS", "FR", "IR", "RR", "SR", "PR"}
FIELD_KEY = {"需求标识": "requirement_id", "功能描述": "description", "调用条件": "condition", "输入": "inputs", "输出": "outputs", "处理": "processing"}


def dump_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def resolve_document(source: str, output: Path) -> tuple[Path, str]:
    """Accept a local DOCX or a GitHub blob URL and retain the retrieved input."""
    if not source.startswith(("https://", "http://")):
        path = Path(source)
        if not path.is_file() or path.suffix.lower() != ".docx":
            raise ValueError("--document 需要存在的 .docx 文件或 GitHub blob URL")
        return path, str(path)
    parsed = urllib.parse.urlparse(source)
    if parsed.scheme != "https" or parsed.hostname != "github.com":
        raise ValueError("在线文档仅接受 https://github.com/.../blob/.../*.docx")
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 5 or parts[2] != "blob" or not parsed.path.lower().endswith(".docx"):
        raise ValueError("GitHub URL 必须是仓库中的 .docx blob 链接")
    owner, repo, _, ref, *file_parts = parts
    if not all((owner, repo, ref)) or not file_parts:
        raise ValueError("GitHub URL 缺少仓库、版本或文件路径")
    raw_path = "/".join(urllib.parse.quote(urllib.parse.unquote(part), safe="") for part in file_parts)
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{raw_path}"
    request = urllib.request.Request(raw_url, headers={"User-Agent": "requirement-code-matcher/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read(30_000_001)
    if len(content) > 30_000_000 or not content.startswith(b"PK"):
        raise ValueError("下载内容不是可接受的 DOCX 文件")
    path = output / "source.docx"
    path.write_bytes(content)
    return path, source


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def split_steps(lines: list[dict[str, Any]], requirement_id: str) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    ordinal = 0
    for line in lines:
        text = clean(line["text"])
        if not text:
            continue
        ordinal += 1
        match = STEP_PATTERN.match(text)
        if match:
            text = clean(match.group(1))
        if not text:
            continue
        # A standalone figure caption labels an image; it is not an executable
        # processing step. Sentences beginning with a figure reference remain.
        if FIGURE_CAPTION_PATTERN.match(text):
            continue
        steps.append({"id": f"{requirement_id}/S{ordinal:02d}", "text": text,
                      "paragraph": line["paragraph"]})
    return steps


def extract_requirements(document: Path) -> dict[str, Any]:
    """Read the a-f structure used by the online repository's four DOCX examples."""
    doc = Document(document)
    extracted: list[dict[str, Any]] = []
    issues: list[str] = []
    current: dict[str, Any] | None = None
    active_field: str | None = None

    def finish() -> None:
        nonlocal current
        if current is None:
            return
        fields = current.pop("_fields")
        plain = current.pop("_plain")
        heading_id = current.pop("_heading_id")
        rid = clean(" ".join(x["text"] for x in fields.get("requirement_id", [])))
        if not rid and heading_id and plain:
            description = clean(" ".join(x["text"] for x in plain))
            current.update({"id": heading_id, "description": description, "condition": "",
                            "inputs": "", "outputs": "", "processing": description,
                            "steps": [{"id": f"{heading_id}/S01", "text": description,
                                       "paragraph": plain[0]["paragraph"]}],
                            "origin_kind": "headed_constraint"})
            extracted.append(current)
            current = None
            return
        if not rid:
            if fields:
                issues.append(f"标题“{current['title']}”有需求字段但缺少需求标识")
            current = None
            return
        current["id"] = rid
        for key in ("description", "condition", "inputs", "outputs"):
            current[key] = clean(" ".join(x["text"] for x in fields.get(key, [])))
            if not current[key]:
                issues.append(f"{rid} 缺少 {key}")
        processing = fields.get("processing", [])
        current["processing"] = "\n".join(x["text"] for x in processing)
        current["steps"] = split_steps(processing, rid)
        if not current["steps"]:
            issues.append(f"{rid} 没有可解析的处理步骤")
        extracted.append(current)
        current = None

    for number, paragraph in enumerate(doc.paragraphs, 1):
        value = paragraph.text.strip()
        if not value:
            continue
        if paragraph.style.name.startswith("Heading"):
            finish()
            heading_match = re.match(r"^([A-Za-z]+-(?:PREQ|SREQ)[\w-]*)\b", value)
            current = {"title": value, "heading_paragraph": number, "_fields": {},
                       "_plain": [], "_heading_id": heading_match.group(1) if heading_match else None}
            active_field = None
            continue
        if current is None:
            continue
        match = FIELD_PATTERN.match(value)
        if match:
            active_field = FIELD_KEY[match.group(2)]
            current["_fields"].setdefault(active_field, [])
            if match.group(3).strip():
                current["_fields"][active_field].append({"text": match.group(3).strip(), "paragraph": number})
        elif active_field:
            current["_fields"][active_field].append({"text": value, "paragraph": number})
        elif current["_heading_id"] and not paragraph.style.name.startswith("Caption"):
            current["_plain"].append({"text": value, "paragraph": number})
    finish()

    # Functional requirements can place a parameter table immediately after a
    # table caption inside the processing section. Keep the table's values in
    # that step; otherwise only the caption would be sent for matching.
    by_heading = {r["heading_paragraph"]: r for r in extracted
                  if isinstance(r.get("heading_paragraph"), int)
                  and r.get("origin_kind") != "headed_constraint"}
    active_req: dict[str, Any] | None = None
    last_caption_paragraph: int | None = None
    body_paragraph_number = 0
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            body_paragraph_number += 1
            paragraph = Paragraph(child, doc._body)
            if paragraph.style.name.startswith("Heading"):
                active_req = by_heading.get(body_paragraph_number)
                last_caption_paragraph = None
            elif clean(paragraph.text):
                last_caption_paragraph = (body_paragraph_number if
                                          re.match(r"^表\s*\d+(?:[.．-]\d+)*\s+", clean(paragraph.text))
                                          else None)
        elif child.tag == qn("w:tbl") and active_req and last_caption_paragraph:
            step = next((s for s in active_req["steps"]
                         if s["paragraph"] == last_caption_paragraph), None)
            last_caption_paragraph = None
            if step is None:
                continue
            table = Table(child, doc._body)
            rows = [[clean(cell.text) for cell in row.cells] for row in table.rows]
            if len(rows) < 2:
                continue
            headers = rows[0]
            detail = ["；".join(f"{headers[i]}：{cell}" for i, cell in enumerate(row)
                                if cell and i < len(headers)) for row in rows[1:]]
            detail = [line for line in detail if line]
            if detail:
                active_req.setdefault("context_tables", []).append({"headers": headers,
                                                                   "rows": rows[1:]})
                step["text"] += "\n表格参数：" + "；".join(detail)

    # A headed performance/safety requirement may refer to a Word table between
    # its heading and the next heading. python-docx separates paragraphs and
    # tables, so the paragraph-only pass above would otherwise lose the table.
    headed = {req["id"]: req for req in extracted if req.get("origin_kind") == "headed_constraint"}
    active_id: str | None = None
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            paragraph = Paragraph(child, doc._body)
            if paragraph.style.name.startswith("Heading"):
                found = re.match(r"^([A-Za-z]+-(?:PREQ|SREQ)[\w-]*)\b", paragraph.text.strip())
                active_id = found.group(1) if found and found.group(1) in headed else None
        elif child.tag == qn("w:tbl") and active_id:
            table = Table(child, doc._body)
            rows = [[clean(cell.text) for cell in row.cells] for row in table.rows]
            if len(rows) < 2:
                continue
            headers = rows[0]
            detail = ["；".join(f"{headers[i]}：{cell}" for i, cell in enumerate(row)
                                if cell and i < len(headers)) for row in rows[1:]]
            detail = [line for line in detail if line]
            if detail:
                headed[active_id].setdefault("context_tables", []).append(
                    {"headers": headers, "rows": rows[1:]})
                table_text = "表格参数：" + "；".join(detail)
                for step in headed[active_id]["steps"]:
                    step["text"] += "\n" + table_text

    known_ids = {x["id"] for x in extracted}
    for table_number, table in enumerate(doc.tables, 1):
        if not table.rows:
            continue
        headers = [clean(cell.text) for cell in table.rows[0].cells]
        if "编号" not in headers or "描述" not in headers:
            continue
        id_col, description_col = headers.index("编号"), headers.index("描述")
        for row_number, row in enumerate(table.rows[1:], 2):
            cells = [clean(cell.text) for cell in row.cells]
            if max(id_col, description_col) >= len(cells):
                continue
            rid, description = cells[id_col], cells[description_col]
            if not rid or not description or rid in known_ids:
                continue
            extracted.append({"id": rid, "title": rid, "heading_paragraph": None,
                              "table": table_number, "table_row": row_number,
                              "description": description, "condition": "", "inputs": "",
                              "outputs": "", "processing": description,
                              "steps": [{"id": f"{rid}/S01", "text": description,
                                         "paragraph": f"表{table_number}行{row_number}"}]})
            known_ids.add(rid)

    # Some documents express performance and safety constraints only in section
    # prose and tables, without requirement IDs. Preserve them as synthetic IDs.
    prefixes = [x["id"].split("-")[0] for x in extracted if "-" in x["id"]]
    prefix = Counter(prefixes).most_common(1)[0][0] if prefixes else "DOC"
    explicit_kinds = {kind for kind in ("PREQ", "SREQ")
                      if any(re.match(rf"^{re.escape(prefix)}-{kind}", x["id"]) for x in extracted)}
    section: str | None = None
    table_number = 0
    paragraph_number = 0
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            paragraph_number += 1
            paragraph = Paragraph(child, doc._body)
            value = clean(paragraph.text)
            if paragraph.style.name.startswith("Heading 1") or paragraph.style.name.startswith("Heading 2"):
                section = ("PREQ" if re.match(r"^3\.3(?:\D|$)", value) else
                           "SREQ" if re.match(r"^3\.4(?:\D|$)", value) else None)
            elif section and section not in explicit_kinds and value and paragraph.style.name == "Normal":
                if not re.match(r"^表\s*(?:3\.[34]|附)", value):
                    rid = f"{prefix}-{section}-P{paragraph_number:03d}"
                    extracted.append({"id": rid, "title": value[:55], "heading_paragraph": None,
                                      "description": value, "condition": "", "inputs": "", "outputs": "",
                                      "processing": value, "origin_kind": "unnumbered_constraint",
                                      "steps": [{"id": f"{rid}/S01", "text": value,
                                                 "paragraph": paragraph_number}]})
        elif child.tag == qn("w:tbl"):
            table_number += 1
            if not section or section in explicit_kinds:
                continue
            table = Table(child, doc._body)
            if len(table.rows) < 2:
                continue
            headers = [clean(cell.text) for cell in table.rows[0].cells]
            for row_number, row in enumerate(table.rows[1:], 2):
                cells = [clean(cell.text) for cell in row.cells]
                description = "；".join(f"{headers[i]}：{value}" for i, value in enumerate(cells)
                                       if value and i < len(headers))
                if not description:
                    continue
                rid = f"{prefix}-{section}-T{table_number:02d}R{row_number:02d}"
                extracted.append({"id": rid, "title": cells[0][:55], "heading_paragraph": None,
                                  "table": table_number, "table_row": row_number,
                                  "description": description, "condition": "", "inputs": "", "outputs": "",
                                  "processing": description, "origin_kind": "unnumbered_constraint",
                                  "steps": [{"id": f"{rid}/S01", "text": description,
                                             "paragraph": f"表{table_number}行{row_number}"}]})

    counts = Counter(x["id"] for x in extracted)
    issues.extend(f"重复需求标识 {rid}" for rid, count in counts.items() if count > 1)
    if not extracted:
        issues.append("没有识别到 a-f 格式的需求；请检查 Word 版式或增加适配器")
    trace_rows: dict[str, dict[str, str]] = {}
    for table in doc.tables:
        if not table.rows:
            continue
        headers = [clean(cell.text) for cell in table.rows[0].cells]
        id_col = next((i for i, value in enumerate(headers) if value in {"需求标识", "需求编号"}), None)
        if id_col is None:
            continue
        for row in table.rows[1:]:
            cells = [clean(cell.text) for cell in row.cells]
            if id_col < len(cells) and cells[id_col]:
                trace_rows[cells[id_col]] = {headers[i]: cells[i] for i in range(min(len(headers), len(cells)))}
    for req in extracted:
        req["trace"] = trace_rows.get(req["id"], {})
    scope_lines: list[str] = []
    in_scope = False
    for paragraph in doc.paragraphs:
        value = clean(paragraph.text)
        if paragraph.style.name.startswith("Heading"):
            in_scope = bool(re.search(r"范围与边界|系统组成|运行方案和场景|默认电池拓扑与算法", value))
        elif in_scope and paragraph.style.name == "Normal" and value:
            scope_lines.append(value)
    return {"document": str(document), "sha256": hashlib.sha256(document.read_bytes()).hexdigest(),
            "requirements": extracted, "issues": issues, "trace_row_count": len(trace_rows),
            "scope_note": " ".join(scope_lines)[:3500]}


def load_dictionary(path: Path | None, code: dict[str, Any]) -> list[dict[str, str]]:
    if path is None:
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    for field in ("project", "revision", "configuration"):
        if payload.get(field) != code[field]:
            raise ValueError(f"数据字典的 {field} 与代码理解输入不一致")
    mappings = payload.get("mappings", [])
    if not isinstance(mappings, list):
        raise ValueError("dictionary.mappings 必须是数组")
    result = []
    for mapping in mappings:
        if not isinstance(mapping, dict) or mapping.get("status") not in {"confirmed", "proposed", "rejected"}:
            raise ValueError("字典条目需要 status: confirmed/proposed/rejected")
        if not mapping.get("term") or not mapping.get("symbol"):
            raise ValueError("字典条目需要 term 和 symbol")
        if mapping["status"] == "confirmed" and not mapping.get("evidence"):
            raise ValueError("已确认的字典映射需要 evidence")
        if mapping.get("relation") not in {"same_as", "field_of", "encodes", "derived_from", "converted_to"}:
            raise ValueError("字典条目需要合法 relation")
        result.append({key: str(mapping.get(key, "")) for key in ("term", "symbol", "status", "relation", "evidence")})
    return result


def load_decisions(path: Path | None, step_ids: set[str], unit_ids: set[str]) -> list[dict[str, Any]]:
    if path is None:
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    values = payload.get("decisions", [])
    if not isinstance(values, list):
        raise ValueError("decisions 必须是数组")
    allowed = {"matched", "partial", "conflict", "unresolved"}
    dimensions = {"condition", "input", "action", "output", "exception", "constraint"}
    seen = set()
    result = []
    for value in values:
        sid = value.get("step_id")
        if sid not in step_ids or sid in seen:
            raise ValueError(f"判定使用无效或重复的 step_id: {sid}")
        seen.add(sid)
        if value.get("overall") not in allowed:
            raise ValueError(f"{sid} 的 overall 无效")
        linked = value.get("unit_ids", [])
        if not isinstance(linked, list) or any(uid not in unit_ids for uid in linked):
            raise ValueError(f"{sid} 的 unit_ids 包含未知代码单元")
        facts = value.get("dimensions", {})
        if not isinstance(facts, dict) or any(k not in dimensions for k in facts):
            raise ValueError(f"{sid} 的 dimensions 无效")
        if any(v not in {"supported", "partial", "conflict", "unknown", "not_applicable"} for v in facts.values()):
            raise ValueError(f"{sid} 的维度结论无效")
        evidence = value.get("evidence", [])
        if value["overall"] != "unresolved" and (not linked or not evidence):
            raise ValueError(f"{sid} 的已判定结果需要代码单元与证据")
        result.append(value)
    return result


def tokens(value: str) -> set[str]:
    found = set()
    for word in WORD_PATTERN.findall(value):
        if re.search(r"[\u4e00-\u9fff]", word):
            found.update(word[i:i+2] for i in range(len(word)-1))
        elif word.upper() not in STOP_WORDS:
            found.add(word.lower())
            found.update(x.lower() for x in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)|\d+", word) if len(x) > 2)
    return found


def overlap(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a) if a else 0.0


def requirement_terms(req: dict[str, Any]) -> set[str]:
    text = " ".join([req.get("inputs", ""), req.get("outputs", ""), req.get("processing", "")])
    terms = {x for x in IDENTIFIER_PATTERN.findall(text) if x.upper() not in STOP_WORDS}
    for value in (req.get("inputs", ""), req.get("outputs", "")):
        terms.update(clean(x) for x in re.split(r"[，,、；;。]\s*", value) if 2 <= len(clean(x)) <= 24)
    return terms


def propose_dictionary(requirements: list[dict[str, Any]], units: list[dict[str, Any]],
                       mappings: list[dict[str, str]],
                       data_hints: list[dict[str, str]] | None = None) -> list[dict[str, Any]]:
    known = {(m["term"].lower(), m["symbol"].lower()) for m in mappings}
    proposals = []
    for req in requirements:
        terms = requirement_terms(req)
        for term in terms:
            for hint in data_hints or []:
                if (term.lower(), hint.get("symbol", "").lower()) in known:
                    continue
                score = overlap(term, hint.get("comment", ""))
                if score >= 0.7:
                    proposals.append({"term": term, "symbol": hint["symbol"],
                                      "requirement_id": req["id"], "unit_id": hint["source"],
                                      "score": round(score, 3), "reason": "code declaration comment",
                                      "status": "proposed"})
        for unit in units:
            symbols = set(unit["symbols"] + unit["reads"] + unit["writes"] + unit["outputs"])
            for term in terms:
                for symbol in symbols:
                    if not re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", symbol):
                        continue
                    if (term.lower(), symbol.lower()) in known:
                        continue
                    score = 1.0 if term.lower() == symbol.lower() else overlap(term, symbol)
                    reason = "exact identifier" if score == 1.0 else "name similarity"
                    if score < 0.55 and len(term) >= 3 and term in unit["summary"]:
                        score = 0.65
                        reason = "code summary co-occurrence"
                    if score < 0.55:
                        continue
                    proposals.append({"term": term, "symbol": symbol, "requirement_id": req["id"],
                                      "unit_id": unit["id"], "score": round(score, 3),
                                      "reason": reason,
                                      "status": "proposed"})
    unique = {(x["term"], x["symbol"], x["requirement_id"], x["unit_id"]): x for x in proposals}
    ranked = sorted(unique.values(), key=lambda x: (-x["score"], x["requirement_id"], x["term"]))
    limited: list[dict[str, Any]] = []
    counts: Counter[tuple[str, str]] = Counter()
    for proposal in ranked:
        key = (proposal["requirement_id"], proposal["term"])
        if counts[key] < 3:
            limited.append(proposal)
            counts[key] += 1
    return limited


def retrieve(requirements: list[dict[str, Any]], units: list[dict[str, Any]],
             mappings: list[dict[str, str]], top_k: int = 5) -> dict[str, Any]:
    confirmed = [m for m in mappings if m["status"] == "confirmed"]
    rows = []
    hit_units: set[str] = set()
    for req in requirements:
        for step in req["steps"]:
            candidates = []
            query = " ".join([req["title"], req["description"], req["condition"], step["text"]])
            data_query = " ".join([req["inputs"], req["outputs"], step["text"]])
            direct_ids = {x.lower() for x in IDENTIFIER_PATTERN.findall(query + " " + data_query)}
            for unit in units:
                behavior = " ".join([unit["name"], unit["summary"], *unit["conditions"],
                                     *unit["steps"], *unit["errors"]])
                data = " ".join([*unit["reads"], *unit["writes"], *unit["outputs"], *unit["symbols"]])
                exact = sorted({symbol for symbol in unit["symbols"] + unit["reads"] + unit["writes"]
                                if symbol.lower() in direct_ids and len(symbol) >= 3})
                dictionary = sorted({m["term"] + " ↔ " + m["symbol"] for m in confirmed
                                     if m["term"] in data_query and m["symbol"] in data})
                behavior_score = overlap(step["text"], behavior)
                context_score = overlap(req["title"] + " " + req["description"] + " " + req["condition"], behavior)
                data_score = overlap(req["inputs"] + " " + req["outputs"], data)
                score = min(1.0, 0.5 * behavior_score + 0.15 * context_score + 0.15 * data_score
                            + (0.15 if exact else 0) + (0.20 if dictionary else 0))
                if score < 0.12:
                    continue
                candidates.append({"unit_id": unit["id"], "name": unit["name"], "file": unit["file"],
                                   "line_start": unit["line_start"], "line_end": unit["line_end"],
                                   "summary": unit["summary"], "score": round(score, 3),
                                   "components": {"step": round(behavior_score, 3),
                                                  "context": round(context_score, 3), "data": round(data_score, 3)},
                                   "exact_identifiers": exact, "confirmed_dictionary": dictionary,
                                   "status": "candidate_unverified",
                                   "code_excerpt": unit.get("code_excerpt", "")})
            candidates.sort(key=lambda x: (-x["score"], x["unit_id"]))
            selected = candidates[:top_k]
            hit_units.update(x["unit_id"] for x in selected)
            rows.append({"requirement_id": req["id"], "requirement_title": req["title"],
                         "step_id": step["id"], "step_text": step["text"],
                         "document_paragraph": step["paragraph"], "candidates": selected,
                         "status": "candidate_found" if selected else "no_candidate"})
    return {"steps": rows, "units_without_candidate": [u["id"] for u in units if u["id"] not in hit_units],
            "note": "Scores rank candidates only; semantic consistency has not been adjudicated."}


def render_report(extracted: dict[str, Any], code: dict[str, Any], result: dict[str, Any],
                  proposals: list[dict[str, Any]], mappings: list[dict[str, str]], output: Path) -> None:
    esc = lambda x: html.escape(str(x))
    steps = result["steps"]
    llm_decisions = {x["step_id"]: x for x in result.get("llm_matching", {}).get("decisions", [])}
    matched = (sum(x["verdict"] in {"supported", "partial"} for x in llm_decisions.values())
               if llm_decisions else sum(bool(x["candidates"]) for x in steps))
    verdict_labels = {"supported": "有代码证据", "partial": "部分支持", "conflict": "存在冲突", "unresolved": "证据不足"}
    rows = []
    decisions = {x["step_id"]: x for x in result.get("decisions", [])}
    for item in steps:
        decision = decisions.get(item["step_id"])
        decision_html = ""
        llm_decision = llm_decisions.get(item["step_id"])
        if llm_decision:
            refs = "".join(f"<details><summary>{esc(e['file'])}:{esc(e['line_start'])}-{esc(e['line_end'])} · "
                           f"{esc(e['observation'])}</summary><pre>{esc(e.get('snippet',''))}</pre></details>"
                            for e in llm_decision["evidence"])
            decision_html += (f"<p class='decision verdict-{esc(llm_decision['verdict'])}'>模型判断："
                              f"<strong>{esc(verdict_labels[llm_decision['verdict']])}</strong> · {esc(llm_decision['reason'])}"
                              f"</p>{refs}")
        if decision:
            dims = " · ".join(f"{esc(k)}: {esc(v)}" for k, v in decision.get("dimensions", {}).items())
            notes = "；".join(esc(str(x)) for x in decision.get("evidence", []))
            decision_html += f"<p class='decision'>人工复核：<strong>{esc(decision['overall'])}</strong> · {dims}<br>{notes}</p>"
        candidates = "".join(
            f"<div class='candidate'><div class='bar' style='width:{int(c['score']*100)}%'></div>"
            f"<strong>{esc(c['name'] or c['unit_id'])}</strong> <span>{c['score']:.2f}</span>"
            f"<small>{esc(c['file'])}:{esc(c['line_start'])}-{esc(c['line_end'])} · {esc(c['summary'])}</small>"
            f"<small>步骤 {c['components']['step']:.2f} · 上下文 {c['components']['context']:.2f} · 数据 {c['components']['data']:.2f}"
            f"{' · 精确标识 '+esc(', '.join(c['exact_identifiers'])) if c['exact_identifiers'] else ''}"
            f"{' · 已确认字典 '+esc(', '.join(c['confirmed_dictionary'])) if c['confirmed_dictionary'] else ''}</small>"
            f"<details><summary>源码片段</summary><pre>{esc(c['code_excerpt'])}</pre></details></div>"
            for c in item["candidates"])
        candidate_html = ("" if result.get("retrieval_skipped") else
                          (f"<details><summary>词面检索辅助候选 {len(item['candidates'])} 个</summary>"
                           f"{candidates or '<em>词面检索未召回；不影响模型判断</em>'}</details>"
                           if llm_decisions else candidates or '<em>未召回候选</em>'))
        rows.append(f"<article class='item' data-state='{item['status']}' data-verdict='{llm_decision['verdict'] if llm_decision else ''}'>"
                    f"<h3>{esc(item['step_id'])} {esc(item['requirement_title'])}</h3>"
                    f"<p>{esc(item['step_text'])}</p><small>Word 段落 {item['document_paragraph']}</small>"
                    f"{decision_html}<div class='results'>{candidate_html}</div></article>")
    issues = "".join(f"<li>{esc(x)}</li>" for x in extracted["issues"])
    dictionary_rows = "".join(
        f"<tr><td>{esc(m['term'])}</td><td>{esc(m['symbol'])}</td><td>{esc(m['status'])}</td><td>{esc(m['evidence'])}</td></tr>"
        for m in mappings)
    proposal_rows = "".join(
        f"<tr><td>{esc(p['term'])}</td><td>{esc(p['symbol'])}</td><td>{esc(p['reason'])}</td><td>{p['score']:.2f}</td></tr>"
        for p in proposals[:60])
    unit_steps: dict[str, list[str]] = {unit["id"]: [] for unit in code["units"]}
    if llm_decisions:
        for item in llm_decisions.values():
            for unit_id in item["unit_ids"]:
                if unit_id in unit_steps:
                    unit_steps[unit_id].append(item["step_id"])
    else:
        for item in steps:
            for candidate in item["candidates"]:
                unit_steps[candidate["unit_id"]].append(item["step_id"])
    coverage_rows = "".join(
        f"<tr><td>{esc(unit['name'])}</td><td>{esc(unit['file'])}:{esc(unit['line_start'])}-{esc(unit['line_end'])}</td>"
        f"<td>{esc(', '.join(unit_steps[unit['id']])) if unit_steps[unit['id']] else '<em>未进入 Top-K</em>'}</td></tr>"
        for unit in sorted(code["units"], key=lambda x: (bool(unit_steps[x["id"]]), x["file"], x["name"])))
    nav_buttons = ([("all", "全部"), ("supported", "有代码证据"), ("partial", "部分支持"),
                    ("conflict", "存在冲突"), ("unresolved", "证据不足")]
                   if llm_decisions else [("all", "全部"), ("no_candidate", "未召回"),
                                          ("candidate_found", "有候选")])
    nav_kind = "verdict" if llm_decisions else "state"
    nav_html = "".join(f"<button type='button' aria-pressed='{'true' if key == 'all' else 'false'}' "
                       f"onclick='filterItems(\"{nav_kind}\",\"{key}\",this)'>{label}</button>"
                       for key, label in nav_buttons)
    page = f"""<!doctype html><html lang='zh-CN'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>需求代码匹配候选</title><style>
body{{font:15px/1.6 system-ui,'Microsoft YaHei',sans-serif;color:#213448;background:#f7f9fc;margin:0}}
main{{max-width:1040px;margin:auto;padding:30px 18px}}h1{{margin:0 0 10px}}h2{{margin-top:32px}}
.summary{{display:flex;gap:20px;flex-wrap:wrap;margin:18px 0}}.summary b{{font-size:24px;display:block}}
.item{{background:white;border:1px solid #d9e2eb;border-radius:10px;padding:18px;margin:14px 0}}
.item h3{{margin:0 0 6px}}.item p{{margin:6px 0}}small{{display:block;color:#526678}}
.candidate{{position:relative;overflow:hidden;border-top:1px solid #e2e8ef;padding:10px 4px}}.candidate strong,.candidate span,.candidate small{{position:relative}}
.candidate span{{float:right}}.bar{{height:4px;background:#4f8cbf;border-radius:3px;margin-bottom:5px}}
.decision{{background:#eaf5ed;padding:8px;border-radius:6px}}
.verdict-conflict{{background:#ffe9e5}}.verdict-unresolved{{background:#f2f5f8}}.verdict-partial{{background:#fff4d9}}
pre{{white-space:pre-wrap;word-break:break-word;background:#f2f5f8;padding:10px;max-height:320px;overflow:auto}}
button{{padding:8px 12px;margin-right:8px;background:white;border:1px solid #bdccd8;border-radius:6px;cursor:pointer}}
button[aria-pressed=true]{{background:#17466c;color:white}}em{{color:#a63d30}}
table{{width:100%;border-collapse:collapse;background:white}}th,td{{border:1px solid #d9e2eb;text-align:left;padding:6px 9px;vertical-align:top}}th{{background:#eaf1f7}}
</style><main><h1>需求—代码候选匹配</h1>
<p>项目 {esc(code['project'])} · 版本 {esc(code['revision'])} · 构型 {esc(code['configuration'])}</p>
<p>代码理解：{esc(code.get('graph',{}).get('backend','unknown'))} · 函数 {len(code['units'])} 个 · {'仅静态图，描述未经 LLM 富化' if code.get('graph',{}).get('static_only') else '包含富化描述'}</p>
{'' if code.get('graph',{}).get('source_checkout_available') else '<p><strong>当前仅有代码理解图，源码快照未随附；引用片段来自图内证据，未独立核对源码版本与构型。</strong></p>'}
<p>静态解析诊断 {esc(code.get('graph',{}).get('diagnostic_count',0))} 条；诊断可能影响代码证据完整性。</p>
<p>需求—代码判定：{'模型 '+esc(result['llm_matching']['model'])+'（无数据字典基线）' if llm_decisions else '仅词面候选检索'}</p>
<p><strong>检索相关度仅用于排列候选，不能代表语义一致或实现完成。</strong>具体判定需核验代码路径。</p>
<div class='summary'><div><b>{len(extracted['requirements'])}</b>需求</div><div><b>{len(steps)}</b>步骤</div><div><b>{matched}</b>{'有代码证据步骤' if llm_decisions else '有候选步骤'}</div><div><b>{len(code['units'])}</b>代码单元</div><div><b>{len(proposals)}</b>字典候选</div></div>
{('<p>模型步骤判断：'+ ' · '.join(esc(verdict_labels[k])+' '+str(sum(x['verdict']==k for x in llm_decisions.values())) for k in verdict_labels) + '。模型结论尚需人工抽样复核。</p>') if llm_decisions else ''}
<h2>匹配检索</h2><nav>{nav_html}</nav>
{''.join(rows)}<h2>解析审计</h2><ul>{issues or '<li>未发现结构问题</li>'}</ul>
<h2>数据字典</h2><p>已确认映射参与检索加权；下列建议仅供审核，不自动确认为同义。</p>
<details><summary>已提供映射 {len(mappings)} 条</summary><table><tr><th>需求术语</th><th>代码符号</th><th>状态</th><th>证据</th></tr>{dictionary_rows}</table></details>
<details><summary>自动候选 {len(proposals)} 条（显示前 60 条）</summary><table><tr><th>需求术语</th><th>代码符号</th><th>建议理由</th><th>候选分</th></tr>{proposal_rows}</table></details>
<h2>代码反向覆盖</h2><p>{sum(not value for value in unit_steps.values())} 个代码单元没有{'模型引用证据' if llm_decisions else '进入任何步骤的 Top-K'}；这只是检查线索，不能直接断言需求缺失。</p>
<details><summary>查看全部 {len(code['units'])} 个代码单元及对应需求步骤</summary><table><tr><th>函数</th><th>源码位置</th><th>候选需求步骤</th></tr>{coverage_rows}</table></details>
<script>function filterItems(kind,state,button){{document.querySelectorAll('nav button').forEach(x=>x.setAttribute('aria-pressed',x===button));document.querySelectorAll('.item').forEach(x=>x.hidden=state!=='all'&&x.dataset[kind]!==state)}}</script></main></html>"""
    output.write_text(page, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="DOCX requirements to code-understanding candidates")
    parser.add_argument("--document", required=True, help="本地 DOCX 或 GitHub blob URL")
    parser.add_argument("--source", type=Path, help="项目 C 源码根目录；复用 --graph 时可省略")
    parser.add_argument("--code-tool", type=Path,
                        default=Path(__file__).resolve().parents[1] / "codeComp" / "tools")
    parser.add_argument("--backend", choices=("clang", "auto", "fallback"), default="auto")
    parser.add_argument("--prepare-build", action="store_true")
    parser.add_argument("--static-only", action="store_true", help="只用 codeComp 静态提取，跳过 LLM 富化")
    parser.add_argument("--model-env", type=Path, help="含 API key、base URL 的本地 .env 文件；密钥不写入结果")
    parser.add_argument("--model", default="deepseek-flash", help="代码富化与匹配模型，默认 DeepSeek V4.1 Flash")
    parser.add_argument("--model-workers", type=int, default=3)
    parser.add_argument("--match-mode", choices=("llm", "lexical"), default="llm")
    parser.add_argument("--graph", type=Path, help="使用已生成的 codeComp 图，跳过重新理解源码")
    parser.add_argument("--dictionary", type=Path)
    parser.add_argument("--decisions", type=Path, help="可选的人工或外部判定器复核结果 JSON")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
    if args.top_k < 1:
        parser.error("--top-k 必须大于零")
    if args.model_workers < 1:
        parser.error("--model-workers 必须大于零")
    match_mode = "lexical" if args.static_only else args.match_mode
    config = load_model_config(args.model_env, args.model) if not args.static_only and (match_mode == "llm" or not args.graph) else None
    args.output.mkdir(parents=True, exist_ok=True)
    document_path, document_source = resolve_document(args.document, args.output)
    extracted = extract_requirements(document_path)
    extracted["document_source"] = document_source
    if not args.source and not args.graph:
        parser.error("需要 --source 源码目录，或使用 --graph 已有代码理解图")
    source = args.source.resolve() if args.source else args.graph.resolve().parent
    if not source.is_dir():
        parser.error(f"源码目录不存在: {source}")
    graph_path = args.graph.resolve() if args.graph else run_codecomp(
        source, args.code_tool.resolve(), args.output.resolve(),
        backend=args.backend, prepare_build=args.prepare_build, static_only=args.static_only,
        model=config["model"] if config else "", base_url=config["base_url"] if config else "",
        api_key=config["api_key"] if config else "", concurrency=args.model_workers)
    code = adapt_graph(graph_path, source, static_only=args.static_only)
    mappings = load_dictionary(args.dictionary, code)
    large_llm_run = match_mode == "llm" and len(code["units"]) > 200
    proposals = ([] if large_llm_run else
                 propose_dictionary(extracted["requirements"], code["units"], mappings, code["data_hints"]))
    if large_llm_run:
        rows = [{"requirement_id": req["id"], "requirement_title": req["title"],
                 "step_id": step["id"], "step_text": step["text"],
                 "document_paragraph": step["paragraph"], "candidates": [], "status": "no_candidate"}
                for req in extracted["requirements"] for step in req["steps"]]
        result = {"steps": rows, "units_without_candidate": [], "retrieval_skipped": True,
                  "note": "Lexical retrieval and dictionary proposals skipped for large LLM run."}
    else:
        result = retrieve(extracted["requirements"], code["units"], [] if match_mode == "llm" else mappings, args.top_k)
    if match_mode == "llm":
        model_result = match_project(extracted["requirements"], code["units"], config,
                                     args.output.resolve(), workers=args.model_workers,
                                     scope_note=extracted.get("scope_note", ""))
        result["llm_matching"] = model_result
        dump_json(args.output / "llm_matches.json", model_result)
    result["decisions"] = load_decisions(args.decisions,
                                          {s["step_id"] for s in result["steps"]},
                                          {u["id"] for u in code["units"]})
    result["inputs"] = {"document_sha256": extracted["sha256"], "source": str(source),
                        "code_graph_path": str(graph_path),
                        "code_graph_sha256": hashlib.sha256(graph_path.read_bytes()).hexdigest()}
    result["code_graph"] = code["graph"]
    dump_json(args.output / "requirements.json", extracted)
    dump_json(args.output / "dictionary_proposals.json",
              {"project": code["project"], "revision": code["revision"],
               "configuration": code["configuration"], "proposals": proposals})
    dump_json(args.output / "matches.json", result)
    render_report(extracted, code, result, proposals, mappings, args.output / "report.html")
    print(f"{len(extracted['requirements'])} requirements, {len(result['steps'])} steps; output: {args.output}")


if __name__ == "__main__":
    main()
