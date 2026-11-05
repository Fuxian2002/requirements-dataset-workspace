"""Second-pass audit of claimed contradictions against the original step."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from codecomp_bridge import adapt_graph
from llm_match import _chat, load_model_config
from main import extract_requirements
from match_v3 import aggregate_v3, step_label
from report_v2 import render_report


AUDIT_PROMPT = """独立复核“需求与源码冲突”的判定。逐项先检查提取的原子事实是否忠实于原始步骤；再检查引用源码是否真的给出相反事实。
特别注意：或/且、分频与每次、默认与可选分支、源单位和物理单位换算、> 与 >= 的边界、状态名与状态来源、按配置与运行时行为。
不得把未找到实现当成冲突。若事实改写了原文的数值对应或添加了“每次/只有”等量词，action=drop；若事实忠实但证据不足或不是反例，action=unresolved；只有事实忠实且存在明确相反源码，action=confirm。
输出 JSON：{"audits":[{"claim_id":"C1","action":"confirm|drop|unresolved","reason":"简短具体理由"}]}。"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--document", type=Path, required=True)
    ap.add_argument("--graph", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--model-env", type=Path, required=True)
    ap.add_argument("--model", default="deepseek-flash")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    extracted = extract_requirements(args.document)
    extracted["requirements"] = payload.get("input_requirements") or extracted["requirements"]
    original = {s["id"]: s for r in extracted["requirements"] for s in r["steps"]}
    config = load_model_config(args.model_env, args.model)
    audit_log = []
    audit_tokens = 0
    for step in payload["steps"]:
        conflicts = [c for c in step["claims"] if c["kind"] == "code" and c["status"] == "contradicted"]
        if not conflicts:
            continue
        answer, usage = _chat(config, AUDIT_PROMPT,
                              {"original_step": original[step["step_id"]]["text"],
                               "claims": [{"claim_id": c["id"], "text": c["text"],
                                           "reason": c["reason"], "source_citations": c["evidence"]}
                                          for c in conflicts]}, 1400)
        audit_tokens += usage.get("total_tokens", 0)
        decisions = {a.get("claim_id"): a for a in answer.get("audits", []) if isinstance(a, dict)}
        dropped = set()
        for claim in conflicts:
            decision = decisions.get(claim["id"], {})
            action = decision.get("action", "unresolved")
            if action not in {"confirm", "drop", "unresolved"}:
                action = "unresolved"
            audit_log.append({"step_id": step["step_id"], "claim_id": claim["id"],
                              "original_status": "contradicted", "action": action,
                              "reason": str(decision.get("reason", "模型未返回有效复核"))[:500]})
            if action == "drop":
                dropped.add(claim["id"])
            elif action == "unresolved":
                claim["status"] = "unresolved"
                claim["reason"] += "；冲突复核：" + str(decision.get("reason", "证据不足"))[:350]
        step["claims"] = [c for c in step["claims"] if c["id"] not in dropped]
        step["verdict"], step["reason_kind"] = step_label(step["claims"])
        step["missing"] = "；".join(c["id"] + " " + c["text"] for c in step["claims"]
                                     if c["kind"] == "code" and c["status"] == "unresolved")[:900]
        print(f"[audit] {step['step_id']} {step['verdict']} "
              f"{','.join(a['action'] for a in audit_log if a['step_id'] == step['step_id'])}", flush=True)
    payload["requirements"] = aggregate_v3(extracted["requirements"], payload["steps"])
    payload["audit"] = {"model": config["model"], "tokens": audit_tokens,
                        "decisions": audit_log, "scope": "only initial contradicted claims"}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "matches_v3_audited.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    graph = adapt_graph(args.graph, args.source)
    for unit in graph["units"]:
        unit["kind"] = "function"
    used = {}
    for path in (args.input.parent / "checkpoints").glob("*.json"):
        checkpoint = json.loads(path.read_text(encoding="utf-8"))
        used.update({u["id"]: u for u in checkpoint.get("units", [])})
    graph_ids = {u["id"] for u in graph["units"]}
    render_report(args.output / "report_v3_audited.html", payload["requirements"],
                  payload["steps"], graph["units"] + [u for uid, u in used.items() if uid not in graph_ids],
                  scope_note="逐事实源码补证 V3 · 冲突独立复核", json_name="matches_v3_audited.json",
                  metadata=payload)
    print(json.dumps({"requirements": {label: sum(r["verdict"] == label for r in payload["requirements"])
                                              for label in ("matched", "partial", "unmatched")},
                      "audit_tokens": audit_tokens, "audit_actions":
                      {label: sum(a["action"] == label for a in audit_log)
                       for label in ("confirm", "drop", "unresolved")}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
