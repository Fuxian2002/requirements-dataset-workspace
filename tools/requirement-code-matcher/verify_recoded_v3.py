"""Verify facts reclassified from scope to code using already inspected lines."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from codecomp_bridge import adapt_graph
from llm_match import _chat, _unit_card, load_model_config
from main import extract_requirements
from match_v3 import JUDGE_PROMPT, aggregate_v3, claim_verdicts, step_label
from report_v2 import render_report


def main() -> None:
    ap = argparse.ArgumentParser()
    for flag in ("input", "document", "graph", "source", "model-env", "output"):
        ap.add_argument("--" + flag, type=Path, required=True)
    ap.add_argument("--model", default="deepseek-flash")
    args = ap.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    extracted = extract_requirements(args.document)
    extracted["requirements"] = payload.get("input_requirements") or extracted["requirements"]
    by_req = {r["id"]: r for r in extracted["requirements"]}
    changed = {x["id"] for x in payload["scope_audit"]["changes"] if x["to"] == "code"}
    used = {}
    for path in (args.input.parent / "checkpoints").glob("*.json"):
        checkpoint = json.loads(path.read_text(encoding="utf-8"))
        used.update({u["id"]: u for u in checkpoint.get("units", [])})
    config = load_model_config(args.model_env, args.model)
    tokens = 0
    log = []
    for step in payload["steps"]:
        claims = [c for c in step["claims"] if f"{step['step_id']}/{c['id']}" in changed]
        if not claims:
            continue
        unit_ids = list(dict.fromkeys(e["unit_id"] for c in claims for e in c["evidence"]
                                          if e["unit_id"] in used))
        units = [used[uid] for uid in unit_ids[:12]]
        if not units:
            log.append({"step_id": step["step_id"], "facts": len(claims), "verified": 0,
                        "reason": "no previous cited source"})
            continue
        req = by_req[step["step_id"].split("/")[0]]
        answer, usage = _chat(config, JUDGE_PROMPT,
                              {"requirement": {"id": req["id"], "title": req["title"],
                                               "description": req["description"], "condition": req["condition"]},
                               "step": step["text"], "claims": claims,
                               "previous_evidence": [], "previous_decisions": [],
                               "code_units": [_unit_card(u, detailed=True) for u in units]}, 1200)
        tokens += usage.get("total_tokens", 0)
        decisions = {c["id"]: c for c in claim_verdicts(claims, answer, {u["id"]: u for u in units})}
        verified = 0
        for claim in claims:
            new = decisions[claim["id"]]
            if new["status"] == "supported":
                claim.update(new)
                verified += 1
        step["verdict"], step["reason_kind"] = step_label(step["claims"])
        step["evidence"] = list({(e["unit_id"], e["line_start"], e["line_end"]): e
                                 for c in step["claims"] for e in c["evidence"]}.values())
        step["missing"] = "；".join(c["id"] + " " + c["text"] for c in step["claims"]
                                     if c["kind"] == "code" and c["status"] == "unresolved")[:900]
        log.append({"step_id": step["step_id"], "facts": len(claims), "verified": verified})
        print(f"[verify] {step['step_id']} {verified}/{len(claims)} {step['verdict']}", flush=True)
    payload["requirements"] = aggregate_v3(extracted["requirements"], payload["steps"])
    payload["recoded_verification"] = {"model": config["model"], "tokens": tokens, "log": log}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "matches_v3_reviewed.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    graph = adapt_graph(args.graph, args.source)
    for unit in graph["units"]:
        unit["kind"] = "function"
    graph_ids = {u["id"] for u in graph["units"]}
    render_report(args.output / "report_v3_reviewed.html", payload["requirements"], payload["steps"],
                  graph["units"] + [u for uid, u in used.items() if uid not in graph_ids],
                  scope_note="逐事实源码补证 V3 · 冲突复核 · 同项目证据复用 · 范围事实重新核验",
                  json_name="matches_v3_reviewed.json", metadata=payload)
    print(json.dumps({"tokens": tokens, "facts_verified": sum(x["verified"] for x in log),
                      "requirements": {label: sum(r["verdict"] == label for r in payload["requirements"])
                                       for label in ("matched", "partial", "unmatched")}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
