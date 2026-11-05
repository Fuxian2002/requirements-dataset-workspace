"""Keep interpretation caveats and preconditions out of code obligations."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from codecomp_bridge import adapt_graph
from main import extract_requirements
from match_v3 import aggregate_v3, step_label
from report_v2 import render_report


INTERPRETATION = re.compile(
    r"^(?:不得将|不能将|不能把|不能写成|不能解释为|不能声称|不能宣称|不能承诺|"
    r"不能仅|不能依据|不应理解为|不应把|不等同|不代表|不是.*证据|不提供|"
    r"不保证|不自动将|没有源码依据|源码未提供|本文不|成功入队不等同|"
    r"CRC64\s*不构成|CRC64\s*不提供|(?:平均值|极值哨兵).*不代表|"
    r"(?:Open/Close).*不等同|回调断言不能作为|次数不得直接换算|"
    r"1\s*ms\s*是触发节拍)")
CONDITION = re.compile(
    r"^(?:前提条件|条件为|触发条件为|该(?:流程|要求|约束|步骤)的前提|"
    r"该流程适用于|上述行为的前提|上述.*以.*为前提|以上行为.*适用|"
    r"默认启动顺序由图)")


def is_boundary(text: str) -> bool:
    value = text.strip()
    return bool(INTERPRETATION.search(value) or CONDITION.search(value))


def main() -> None:
    ap = argparse.ArgumentParser()
    for flag in ("input", "document", "graph", "source", "output"):
        ap.add_argument("--" + flag, type=Path, required=True)
    args = ap.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    extracted = extract_requirements(args.document)
    extracted["requirements"] = payload.get("input_requirements") or extracted["requirements"]
    recoded = {x["id"] for x in payload["scope_audit"]["changes"] if x["to"] == "code"}
    reverted = []
    for step in payload["steps"]:
        for claim in step["claims"]:
            cid = f"{step['step_id']}/{claim['id']}"
            if cid in recoded and claim["kind"] == "code" and is_boundary(claim["text"]):
                claim["kind"] = "scope"
                claim["status"] = "unresolved"
                claim["reason"] += "；解释边界或适用前提，不单列为实现义务。"
                reverted.append(cid)
        step["verdict"], step["reason_kind"] = step_label(step["claims"])
        step["missing"] = "；".join(c["id"] + " " + c["text"] for c in step["claims"]
                                     if c["kind"] == "code" and c["status"] == "unresolved")[:900]
    payload["requirements"] = aggregate_v3(extracted["requirements"], payload["steps"])
    payload["scope_guard"] = {"reverted": reverted, "rule": "interpretation or precondition"}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "matches_v3_guarded.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    graph = adapt_graph(args.graph, args.source)
    for unit in graph["units"]:
        unit["kind"] = "function"
    used = {}
    for path in (args.input.parent / "checkpoints").glob("*.json"):
        checkpoint = json.loads(path.read_text(encoding="utf-8"))
        used.update({u["id"]: u for u in checkpoint.get("units", [])})
    graph_ids = {u["id"] for u in graph["units"]}
    render_report(args.output / "report_v3_guarded.html", payload["requirements"], payload["steps"],
                  graph["units"] + [u for uid, u in used.items() if uid not in graph_ids],
                  scope_note="逐事实源码补证 V3 · 冲突复核 · 同项目证据复用 · 解释边界校正",
                  json_name="matches_v3_guarded.json", metadata=payload)
    print(json.dumps({"reverted": len(reverted),
                      "requirements": {label: sum(r["verdict"] == label for r in payload["requirements"])
                                       for label in ("matched", "partial", "unmatched")}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
