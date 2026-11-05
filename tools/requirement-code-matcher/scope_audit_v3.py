"""Audit whether supposedly out-of-scope facts actually assert code behavior."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from codecomp_bridge import adapt_graph
from llm_match import _chat, load_model_config
from main import extract_requirements
from match_v3 import aggregate_v3, step_label
from report_v2 import render_report


PROMPT = """把需求原子事实分为 code、scope、external、runtime。code 是能由源码行为、结构、配置验证的具体事实，包括否定、前提和“可能”表述；scope 仅指不作保证、不扩展结论、不能据此推断等认识边界；external 指部署、硬件验收、文档流程义务；runtime 指需实测的时间/性能上界。
不要因句中有“不能、并非、应、仅”就自动判 scope。逐条输出 JSON：{"items":[{"id":"...","kind":"code|scope|external|runtime","reason":"..."}]}。不得漏项。"""


def main() -> None:
    ap = argparse.ArgumentParser()
    for flag in ("input", "document", "graph", "source", "model-env", "output"):
        ap.add_argument("--" + flag, type=Path, required=True)
    ap.add_argument("--model", default="deepseek-flash")
    args = ap.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    extracted = extract_requirements(args.document)
    extracted["requirements"] = payload.get("input_requirements") or extracted["requirements"]
    originals = {s["id"]: s["text"] for r in extracted["requirements"] for s in r["steps"]}
    config = load_model_config(args.model_env, args.model)
    scope = [(s, c) for s in payload["steps"] for c in s["claims"] if c["kind"] == "scope"]
    changes = []
    tokens = 0
    for start in range(0, len(scope), 16):
        batch = scope[start:start + 16]
        items = [{"id": f"{s['step_id']}/{c['id']}", "original_step": originals[s["step_id"]],
                  "fact": c["text"]} for s, c in batch]
        answer, usage = _chat(config, PROMPT, {"items": items}, 2500)
        tokens += usage.get("total_tokens", 0)
        decisions = {x.get("id"): x for x in answer.get("items", []) if isinstance(x, dict)}
        for s, c in batch:
            key = f"{s['step_id']}/{c['id']}"
            item = decisions.get(key, {})
            kind = item.get("kind", "scope")
            if kind not in {"code", "scope", "external", "runtime"}:
                kind = "scope"
            if kind != "scope":
                changes.append({"id": key, "from": "scope", "to": kind,
                                "reason": str(item.get("reason", ""))[:300]})
                c["kind"] = kind
                if kind == "code":
                    c["status"] = "unresolved"
                    c["reason"] += "；分类复核：此项是可由源码检验的事实，需进一步核验现有引用。"
        print(f"[scope] {min(start + 16, len(scope))}/{len(scope)}", flush=True)
    for step in payload["steps"]:
        step["verdict"], step["reason_kind"] = step_label(step["claims"])
        step["missing"] = "；".join(c["id"] + " " + c["text"] for c in step["claims"]
                                     if c["kind"] == "code" and c["status"] == "unresolved")[:900]
    payload["requirements"] = aggregate_v3(extracted["requirements"], payload["steps"])
    payload["scope_audit"] = {"model": config["model"], "tokens": tokens, "changes": changes}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "matches_v3_scope_audited.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    graph = adapt_graph(args.graph, args.source)
    for unit in graph["units"]:
        unit["kind"] = "function"
    used = {}
    for path in (args.input.parent / "checkpoints").glob("*.json"):
        checkpoint = json.loads(path.read_text(encoding="utf-8"))
        used.update({u["id"]: u for u in checkpoint.get("units", [])})
    graph_ids = {u["id"] for u in graph["units"]}
    render_report(args.output / "report_v3_scope_audited.html", payload["requirements"],
                  payload["steps"], graph["units"] + [u for uid, u in used.items() if uid not in graph_ids],
                  scope_note="逐事实源码补证 V3 · 冲突复核 · 同项目证据复用 · 事实分类复核",
                  json_name="matches_v3_scope_audited.json", metadata=payload)
    print(json.dumps({"changes": len(changes), "tokens": tokens,
                      "requirements": {label: sum(r["verdict"] == label for r in payload["requirements"])
                                       for label in ("matched", "partial", "unmatched")}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
