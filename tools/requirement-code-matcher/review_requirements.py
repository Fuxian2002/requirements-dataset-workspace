"""Review extracted Word requirements before matching embedded source code.

The original document is never modified. Every selected atomic step retains its
source step ID, and every excluded item remains visible in the review artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any

from llm_match import _chat, load_model_config
from main import extract_requirements


REVIEW_PROMPT = """你在审查嵌入式项目的需求文档提取结果，不能根据代码匹配答案筛选需求。
目标是只把可由项目源码或配置明确核验的功能性行为送入后续匹配。安全相关需求只要描述具体可编码的保护逻辑也可保留；纯性能实测、可靠性指标、硬件物理特性、人工流程、部署记录应排除。
先判断整条需求：include=至少含一个可由源码/配置核验的具体行为；exclude=完全不属于代码核验范围。不得仅凭 FREQ/PREQ/SREQ 编号决定。
逐一审查原始步骤：保留采集、环境感知、设备交互（含控制/通信/存储）和计算/判定四类可编码行为。纯标题、表头、图注、“算法如下/见图”、残缺公式、背景说明、代码外义务必须排除并说明理由。
每个保留的步骤必须只有一个可单独判定的行为；条件、输入、参数和该行为的结果可留在一起。多个独立动作必须拆成多个 atomic_steps；保留原文中的数值、单位、条件和否定词，不得补写原文没有的动作。公式或图像未提取完整时不得猜补，标为 needs_review 并排除自动匹配。
对每个输入 step_id 必须恰好返回一项。输出 JSON：{"requirement":{"decision":"include|exclude","reason":"...","uncovered_obligations":[]},"steps":[{"source_id":"原 step_id","decision":"include|exclude|needs_review","reason":"...","atomic_steps":[{"text":"单一可核验行为","category":"acquisition|perception|interaction|computation"}]}]}。
include 才填写 atomic_steps；exclude/needs_review 的 atomic_steps 为空。只返回 JSON。"""

DESCRIPTION_PROMPT = """检查功能描述中是否还有可由源码/配置明确核验、但没有被已保留原子步骤覆盖的独立行为。
仅提取描述原文真正要求的行为；不要把领域常识或代码实现细节补成需求。排除纯背景、性能实测、人工部署流程、免责声明和与已保留步骤同义的内容。
每个新步骤只能属于 acquisition（采集）、perception（感知）、interaction（设备交互/控制/通信/存储）、computation（计算/判定）之一，只含一个可独立判定的动作及其必要条件/结果。保留原文数值、单位、否定词。若没有遗漏，返回空列表。
输出 JSON：{"atomic_steps":[{"text":"...","category":"acquisition|perception|interaction|computation"}],"reason":"..."}。只返回 JSON。"""

DIRTY_STEP = re.compile(r"^(?:算法|流程|处理流程|功能分解|输入|输出|步骤|表头|数据定义)(?:如下|如图所示|见图)?[：:。.]?$|^见图\s*\d+[。.]?$|^图\s*\d+(?:[.．-]\d+)*\b|^表\s*\d+(?:[.．-]\d+)*\b")
NUMBER = re.compile(r"(?<![A-Za-z_])(?:0[xX][0-9A-Fa-f]+|\d+(?:\.\d+)?)(?![A-Za-z_])")
ACTION_CUES = {
    "acquisition": re.compile(r"采集|读取|获取|接收"),
    "perception": re.compile(r"检测|感知|识别|监测"),
    "interaction": re.compile(r"发送|写入|控制|驱动|输出|存储|传输"),
    "computation": re.compile(r"计算|比较|判定|滤波|转换|估计"),
}


def _review_one(req: dict[str, Any], config: dict[str, str]) -> tuple[dict[str, Any], dict[str, Any], int]:
    request = {"id": req["id"], "title": req.get("title", ""),
               "description": req.get("description", ""),
               "condition": req.get("condition", ""),
               "inputs": req.get("inputs", ""), "outputs": req.get("outputs", ""),
               "steps": [{"id": s["id"], "text": s["text"]} for s in req["steps"]]}
    answer, usage = _chat(config, REVIEW_PROMPT, request, 6000)
    if not isinstance(answer, dict):
        raise ValueError(f"{req['id']}: model did not return a JSON object")
    decision = answer.get("requirement", {})
    if not isinstance(decision, dict) or decision.get("decision") not in {"include", "exclude"}:
        raise ValueError(f"{req['id']}: invalid requirement decision")
    raw_steps = answer.get("steps", [])
    if not isinstance(raw_steps, list):
        raise ValueError(f"{req['id']}: missing step review")
    by_id = {s["id"]: s for s in req["steps"]}
    entries = {}
    for item in raw_steps:
        if not isinstance(item, dict) or item.get("source_id") not in by_id or item["source_id"] in entries:
            raise ValueError(f"{req['id']}: duplicate or unknown source step")
        entries[item["source_id"]] = item
    if set(entries) != set(by_id):
        raise ValueError(f"{req['id']}: model omitted a source step")
    reviewed_steps = []
    log_steps = []
    for original in req["steps"]:
        item = entries[original["id"]]
        state = item.get("decision")
        if state not in {"include", "exclude", "needs_review"}:
            raise ValueError(f"{original['id']}: invalid review decision")
        if decision["decision"] == "exclude" and state == "include":
            raise ValueError(f"{req['id']}: excluded requirement contains included step")
        pieces = item.get("atomic_steps", [])
        if state == "include" and DIRTY_STEP.match(original["text"].strip()):
            state, pieces = "exclude", []
            item = {**item, "reason": "规则检查：纯标题、图注或表头"}
        if state == "include" and (not isinstance(pieces, list) or not 1 <= len(pieces) <= 20):
            raise ValueError(f"{original['id']}: no valid atomic steps")
        if state != "include" and pieces:
            raise ValueError(f"{original['id']}: excluded step has matching material")
        produced = []
        if state == "include":
            old_numbers = set(NUMBER.findall(original["text"]))
            new_numbers = set(NUMBER.findall(" ".join(str(p.get("text", "")) for p in pieces
                                                   if isinstance(p, dict))))
            if not new_numbers.issubset(old_numbers):
                state, pieces = "needs_review", []
                item = {**item, "reason": "规则检查：拆分结果引入原文没有的数值"}
            elif old_numbers - new_numbers:
                item = {**item, "reason": str(item.get("reason", "")) +
                        "；需人工核对未进入原子步骤的数值：" +
                        ", ".join(sorted(old_numbers - new_numbers))}
        if state == "include" and len(pieces) == 1 and isinstance(pieces[0], dict):
            text = str(pieces[0].get("text", ""))
            action_groups = [name for name, cue in ACTION_CUES.items() if cue.search(text)]
            if len(action_groups) > 1 and re.search(r"并|然后|随后|再|同时|之后", text):
                state, pieces = "needs_review", []
                item = {**item, "reason": "规则检查：仍含多个不同类别的动作，需继续拆分"}
        if state == "include":
            for ordinal, piece in enumerate(pieces, 1):
                if not isinstance(piece, dict) or piece.get("category") not in {
                        "acquisition", "perception", "interaction", "computation"}:
                    raise ValueError(f"{original['id']}: invalid atomic category")
                text = re.sub(r"\s+", " ", str(piece.get("text", ""))).strip()
                if len(text) < 4 or len(text) > 600:
                    raise ValueError(f"{original['id']}: invalid atomic text")
                sid = original["id"] if len(pieces) == 1 else f"{original['id']}-{ordinal:02d}"
                produced.append(sid)
                reviewed_steps.append({"id": sid, "text": text,
                                       "paragraph": original.get("paragraph"),
                                       "source_step_id": original["id"],
                                       "source_text": original["text"],
                                       "category": piece["category"]})
        log_steps.append({"source_id": original["id"], "source_text": original["text"],
                          "decision": state, "reason": str(item.get("reason", "")),
                          "produced_ids": produced})
    if decision["decision"] == "include" and not reviewed_steps:
        decision = {**decision, "decision": "needs_review",
                    "reason": str(decision.get("reason", "")) + "；功能描述可编码但尚无合规原子步骤"}
    reviewed = {**req, "steps": reviewed_steps, "reviewed_input": True}
    log = {"requirement_id": req["id"], "title": req.get("title", ""),
           "decision": decision["decision"], "reason": str(decision.get("reason", "")),
           "uncovered_obligations": decision.get("uncovered_obligations", []),
           "steps": log_steps}
    return reviewed, log, int(usage.get("total_tokens", 0))


def _recover_description(req: dict[str, Any], reviewed: dict[str, Any],
                         log: dict[str, Any], config: dict[str, str]) -> int:
    """Make missing obligations explicit rather than silently dropping a requirement."""
    if not req.get("description") or not (
            (log["decision"] == "include" and log.get("uncovered_obligations")) or
            (log["decision"] in {"exclude", "needs_review"} and
             ("无合规可匹配步骤" in log["reason"] or
              "功能描述可编码但尚无合规原子步骤" in log["reason"]))):
        return 0
    answer, usage = _chat(config, DESCRIPTION_PROMPT,
                          {"requirement_id": req["id"],
                           "description": req["description"],
                           "uncovered_obligations": log.get("uncovered_obligations", []),
                           "selected_steps": [s["text"] for s in reviewed["steps"]]}, 6000)
    raw = answer.get("atomic_steps", []) if isinstance(answer, dict) else []
    if not isinstance(raw, list) or len(raw) > 30:
        raise ValueError(f"{req['id']}: invalid description-step review")
    new_steps = []
    origin_numbers = set(NUMBER.findall(req["description"]))
    for item in raw:
        if not isinstance(item, dict) or item.get("category") not in ACTION_CUES:
            raise ValueError(f"{req['id']}: invalid description-step category")
        text = re.sub(r"\s+", " ", str(item.get("text", ""))).strip()
        if len(text) < 4 or len(text) > 600:
            raise ValueError(f"{req['id']}: invalid description-step text")
        if not set(NUMBER.findall(text)).issubset(origin_numbers):
            log.setdefault("description_warnings", []).append("描述补充步骤出现原文没有的数值")
            continue
        if DIRTY_STEP.match(text):
            continue
        if len([name for name, cue in ACTION_CUES.items() if cue.search(text)]) > 1 and re.search(
                r"并|然后|随后|再|同时|之后", text):
            log.setdefault("description_warnings", []).append("描述补充步骤仍有复合动作")
            continue
        sid = f"{req['id']}/DESC-{len(new_steps) + 1:02d}"
        new_steps.append({"id": sid, "text": text, "paragraph": req.get("heading_paragraph"),
                          "source_step_id": f"{req['id']}/DESC",
                          "source_text": req["description"], "category": item["category"]})
    if new_steps:
        reviewed["steps"].extend(new_steps)
        log["steps"].append({"source_id": f"{req['id']}/DESC",
                             "source_text": req["description"], "decision": "include",
                             "reason": "功能描述中存在处理步骤未覆盖的可编码行为；" +
                                       str(answer.get("reason", "")),
                             "produced_ids": [s["id"] for s in new_steps]})
        log["decision"] = "include"
        log["reason"] = (str(log["reason"]).replace("；无合规可匹配步骤", "")
                         .replace("；功能描述可编码但尚无合规原子步骤", ""))
    return int(usage.get("total_tokens", 0))


def review_document(document: Path, config: dict[str, str], output: Path) -> dict[str, Any]:
    extracted = extract_requirements(document)
    selected, log = [], []
    tokens = 0
    cache_dir = output.parent / "review_checkpoints"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for req in extracted["requirements"]:
        if "-PREQ" in req["id"] or "-SREQ" in req["id"]:
            log.append({"requirement_id": req["id"], "title": req.get("title", ""),
                        "decision": "exclude", "reason": "本轮只匹配功能需求；非功能需求不进入分母",
                        "uncovered_obligations": [],
                        "steps": [{"source_id": s["id"], "source_text": s["text"],
                                   "decision": "exclude", "reason": "非功能需求，不进入本轮匹配",
                                   "produced_ids": []} for s in req["steps"]]})
            print(f"[review] {req['id']} exclude nonfunctional", flush=True)
            continue
        semantic_req = {k: v for k, v in req.items() if k not in {"heading_paragraph", "steps"}}
        semantic_req["steps"] = [{"id": s["id"], "text": s["text"]} for s in req["steps"]]
        fingerprint = hashlib.sha256(json.dumps({"requirement": semantic_req,
                                                 "model": config["model"],
                                                 "base_url": config.get("base_url", ""),
                                                 "prompt": REVIEW_PROMPT},
                                                ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        cache_path = cache_dir / (re.sub(r"[^A-Za-z0-9_-]", "_", req["id"]) + ".json")
        cached = None
        if cache_path.exists():
            try:
                candidate = json.loads(cache_path.read_text(encoding="utf-8"))
                if candidate.get("fingerprint") == fingerprint:
                    cached = candidate
            except (ValueError, OSError):
                pass
        if cached:
            reviewed, entry, used = cached["reviewed"], cached["entry"], 0
            if not reviewed["steps"] and "无合规可匹配步骤" in entry["reason"]:
                entry["decision"] = "needs_review"
                entry["reason"] = entry["reason"].replace(
                    "无合规可匹配步骤", "功能描述可编码但尚无合规原子步骤")
            current_paragraphs = {s["id"]: s.get("paragraph") for s in req["steps"]}
            for step in reviewed["steps"]:
                step["paragraph"] = current_paragraphs.get(
                    step["source_step_id"], req.get("heading_paragraph"))
        else:
            reviewed, entry, used = _review_one(req, config)
        if not cached or not cached.get("description_reviewed"):
            used += _recover_description(req, reviewed, entry, config)
            cache_path.write_text(json.dumps({"fingerprint": fingerprint,
                                              "reviewed": reviewed, "entry": entry,
                                              "description_reviewed": True},
                                             ensure_ascii=False, indent=2), encoding="utf-8")
        log.append(entry)
        tokens += used
        if entry["decision"] == "include":
            selected.append(reviewed)
        print(f"[review] {req['id']} {entry['decision']} "
              f"{len(reviewed['steps'])} atomic steps", flush=True)
    result = {"document": str(document.resolve()), "document_sha256": extracted["sha256"],
              "model": config["model"],
              "review_prompt_sha256": hashlib.sha256(REVIEW_PROMPT.encode("utf-8")).hexdigest(),
              "original_requirement_count": len(extracted["requirements"]),
              "original_step_count": sum(len(r["steps"]) for r in extracted["requirements"]),
              "selected_requirement_count": len(selected),
              "selected_step_count": sum(len(r["steps"]) for r in selected),
              "usage_tokens": tokens, "requirements": selected, "review": log}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    render_review(output.with_suffix(".html"), result)
    if not selected:
        raise ValueError(f"No code-verifiable requirements remained; see {output.with_suffix('.html')}")
    return result


def render_review(path: Path, result: dict[str, Any]) -> None:
    esc = lambda x: html.escape(str(x), quote=True)
    rows = []
    for req in result["review"]:
        for step in req["steps"]:
            rows.append(f"<tr class='{esc(step['decision'])}'><td>{esc(req['requirement_id'])}</td>"
                        f"<td>{esc(req['decision'])}<br>{esc(req['reason'])}"
                        f"<br>{esc(req.get('uncovered_obligations', []))}</td><td>{esc(step['source_id'])}</td>"
                        f"<td>{esc(step['source_text'])}</td><td>{esc(step['decision'])}</td>"
                        f"<td>{esc(', '.join(step['produced_ids']))}</td>"
                        f"<td>{esc(step['reason'])}</td></tr>")
    page = ("<!doctype html><html lang='zh-CN'><meta charset='utf-8'>"
            "<title>需求与步骤入模审查</title><style>body{font:14px/1.5 system-ui,'Microsoft YaHei';"
            "max-width:1400px;margin:24px auto;color:#19334a}table{width:100%;border-collapse:collapse}"
            "td,th{padding:9px;border-bottom:1px solid #ddd;text-align:left;vertical-align:top}"
            "tr.exclude,tr.needs_review{background:#fff3ee}tr.include{background:#f3fbf6}"
            "th{position:sticky;top:0;background:#eaf1f7}</style>"
            f"<h1>需求与步骤入模审查</h1><p>原始需求 {result['original_requirement_count']} 条，"
            f"原始步骤 {result['original_step_count']} 个；入模需求 {result['selected_requirement_count']} 条，"
            f"入模原子步骤 {result['selected_step_count']} 个。"
            f"<a href='{esc(path.with_suffix('.json').name)}'>查看完整 JSON 与拆分文本</a></p>"
            "<p>排除项和待人工复核项不进入代码匹配；本页保存原始步骤与每个新步骤的编号映射。</p>"
            "<table><thead><tr><th>需求</th><th>需求决定</th><th>原步骤</th><th>原文</th>"
            "<th>步骤决定</th><th>新步骤编号</th><th>原因</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table></html>")
    path.write_text(page, encoding="utf-8")


def load_review(path: Path, document: Path) -> dict[str, Any]:
    result = json.loads(path.read_text(encoding="utf-8"))
    actual = hashlib.sha256(document.read_bytes()).hexdigest()
    if result.get("document_sha256") != actual:
        raise ValueError("Review artifact belongs to a different Word document")
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Review Word requirements for atomic code matching")
    ap.add_argument("--document", type=Path, required=True)
    ap.add_argument("--model-env", type=Path, required=True)
    ap.add_argument("--model", default="")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    config = load_model_config(args.model_env, args.model)
    review_document(args.document, config, args.output)


if __name__ == "__main__":
    main()
