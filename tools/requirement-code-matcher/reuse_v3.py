"""Reuse already verified evidence for equivalent claims in the same project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from candidate_index import CandidateIndex
from codecomp_bridge import adapt_graph
from llm_match import _chat, _unit_card, load_model_config
from main import extract_requirements
from match_v3 import JUDGE_PROMPT, aggregate_v3, claim_verdicts, step_label
from report_v2 import render_report

EQUIVALENCE_PROMPT = """判断两条需求原子事实是否表达同一可由相同源码证据验证的命题。严格保留数值、单位、触发条件、量词和否定；仅当 donor 完整蕴含 target 时回答 true。不要重新判断代码。输出 JSON：{"entails":true|false,"reason":"..."}。"""


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
    config = load_model_config(args.model_env, args.model)
    used = {}
    for path in (args.input.parent / "checkpoints").glob("*.json"):
        checkpoint = json.loads(path.read_text(encoding="utf-8"))
        used.update({u["id"]: u for u in checkpoint.get("units", [])})
    memory = [(step, claim) for step in payload["steps"] for claim in step["claims"]
              if claim["kind"] == "code" and claim["status"] == "supported" and claim["evidence"]]
    index = CandidateIndex([{"id": f"{s['step_id']}/{c['id']}", "name": c["text"],
                             "summary": c["text"], "file": ""} for s, c in memory])
    reuse_log = []
    tokens = 0
    for step in payload["steps"]:
        unresolved = [c for c in step["claims"] if c["kind"] == "code" and c["status"] == "unresolved"]
        if step["verdict"] != "not_matched" or not unresolved:
            continue
        unit_ids = []
        donor_ids = []
        for claim in unresolved:
            for pos, score in index.rank(claim["text"])[:4]:
                if score < 0.13:
                    continue
                donor_step, donor_claim = memory[pos]
                donor_ids.append(f"{donor_step['step_id']}/{donor_claim['id']}")
                for e in donor_claim["evidence"]:
                    if e["unit_id"] in used and e["unit_id"] not in unit_ids:
                        unit_ids.append(e["unit_id"])
        units = [used[uid] for uid in unit_ids[:16]]
        if not units:
            continue
        req = by_req[step["step_id"].split("/")[0]]
        answer, usage = _chat(config, JUDGE_PROMPT,
                              {"requirement": {"id": req["id"], "title": req["title"],
                                               "description": req["description"], "condition": req["condition"]},
                               "step": step["text"], "claims": step["claims"],
                               "previous_evidence": step["evidence"],
                               "previous_decisions": step["claims"],
                               "code_units": [_unit_card(u, detailed=True) for u in units]}, 3200)
        tokens += usage.get("total_tokens", 0)
        visible = {u["id"]: u for u in units}
        new_decisions = {c["id"]: c for c in claim_verdicts(step["claims"], answer, visible)}
        for claim in step["claims"]:
            new = new_decisions[claim["id"]]
            if claim["kind"] == "code" and claim["status"] == "unresolved" and new["status"] == "supported":
                claim.update(new)
        for claim in unresolved:
            if claim["status"] != "unresolved":
                continue
            for pos, score in index.rank(claim["text"])[:2]:
                if score < 0.40:
                    continue
                donor_step, donor_claim = memory[pos]
                equivalent, equiv_usage = _chat(config, EQUIVALENCE_PROMPT,
                                                 {"donor": donor_claim["text"],
                                                  "target": claim["text"]}, 350)
                tokens += equiv_usage.get("total_tokens", 0)
                if equivalent.get("entails") is True:
                    claim["status"] = "supported"
                    claim["evidence"] = donor_claim["evidence"]
                    claim["reason"] = ("项目内同义事实证据复用：" + donor_step["step_id"] +
                                       "/" + donor_claim["id"] + "；" + str(equivalent.get("reason", ""))[:300])
                    break
        step["verdict"], step["reason_kind"] = step_label(step["claims"])
        step["evidence"] = list({(e["unit_id"], e["line_start"], e["line_end"]): e
                                 for c in step["claims"] for e in c["evidence"]}.values())
        step["missing"] = "；".join(c["id"] + " " + c["text"] for c in step["claims"]
                                     if c["kind"] == "code" and c["status"] == "unresolved")[:900]
        step["inspected_ids"] = list(dict.fromkeys(step["inspected_ids"] + list(visible)))
        step["inspected_count"] = len(step["inspected_ids"])
        reuse_log.append({"step_id": step["step_id"], "donors": donor_ids[:8],
                          "new_verdict": step["verdict"]})
        print(f"[reuse] {step['step_id']} {step['verdict']}", flush=True)
    payload["requirements"] = aggregate_v3(extracted["requirements"], payload["steps"])
    payload["reuse"] = {"model": config["model"], "tokens": tokens, "log": reuse_log}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "matches_v3_final.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    graph = adapt_graph(args.graph, args.source)
    for unit in graph["units"]:
        unit["kind"] = "function"
    graph_ids = {u["id"] for u in graph["units"]}
    render_report(args.output / "report_v3_final.html", payload["requirements"], payload["steps"],
                  graph["units"] + [u for uid, u in used.items() if uid not in graph_ids],
                  scope_note="逐事实源码补证 V3 · 冲突复核 · 同项目证据复用",
                  json_name="matches_v3_final.json", metadata=payload)
    print(json.dumps({"requirements": {label: sum(r["verdict"] == label for r in payload["requirements"])
                                              for label in ("matched", "partial", "unmatched")},
                      "reuse_tokens": tokens}, ensure_ascii=False))


if __name__ == "__main__":
    main()
