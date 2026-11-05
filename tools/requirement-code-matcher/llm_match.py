"""Evidence-bound LLM matching without an explicit data dictionary."""
from __future__ import annotations

import json
import hashlib
import os
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from candidate_index import CandidateIndex


def load_model_config(path: Path | None, model: str) -> dict[str, str]:
    values: dict[str, str] = {}
    if path:
        if not path.is_file():
            raise ValueError(f"模型配置文件不存在: {path}")
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    key = values.get("LLM_API_KEY") or values.get("OPENAI_API_KEY") or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY") or ""
    base_url = values.get("LLM_BASE_URL") or values.get("OPENAI_BASE_URL") or os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL") or ""
    selected_model = model or values.get("LLM_MODEL") or values.get("OPENAI_MODEL") or os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL") or ""
    if not key or not base_url or not selected_model:
        raise ValueError("模型调用需要 API key、base URL 和模型名；通过 --model-env 或环境变量提供")
    if not base_url.startswith("https://"):
        raise ValueError("外部模型服务地址必须使用 HTTPS")
    return {"api_key": key, "base_url": base_url.rstrip("/"), "model": selected_model}


def _json_answer(value: str) -> dict[str, Any]:
    text = value.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I).strip()
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("模型未返回 JSON 对象")
        result = json.loads(text[start:end + 1])
    if not isinstance(result, dict):
        raise ValueError("模型输出必须是 JSON 对象")
    return result


def _chat(config: dict[str, str], system: str, payload: dict[str, Any], max_tokens: int) -> tuple[dict[str, Any], dict[str, Any]]:
    body = json.dumps({"model": config["model"], "temperature": 0,
                       "thinking": {"type": "disabled"},
                       "response_format": {"type": "json_object"}, "max_tokens": max_tokens,
                       "messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}]},
                      ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(config["base_url"] + "/chat/completions", body,
                                     headers={"Authorization": "Bearer " + config["api_key"],
                                              "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                raw = json.load(response)
            content = raw["choices"][0]["message"]["content"] or ""
            if raw["choices"][0].get("finish_reason") == "length":
                raise ValueError("模型输出达到 max_tokens，JSON 可能不完整")
            return _json_answer(content), raw.get("usage") or {}
        except urllib.error.HTTPError as exc:
            if exc.code in {401, 402, 403}:
                raise RuntimeError(f"模型服务拒绝请求: HTTP {exc.code}") from exc
            if attempt == 2:
                raise RuntimeError(f"模型调用失败: HTTP {exc.code}") from exc
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError, ValueError) as exc:
            if attempt == 2:
                raise RuntimeError(f"模型调用或 JSON 解析失败: {type(exc).__name__}: {exc}") from exc
            time.sleep(2 ** attempt)
    raise AssertionError("unreachable")


def _requirement_card(req: dict[str, Any], scope_note: str = "") -> dict[str, Any]:
    return {key: req.get(key, "") for key in ("id", "title", "description", "condition", "inputs", "outputs")} | {
        "steps": [{"id": step["id"], "text": step["text"]} for step in req["steps"]],
        "document_scope": scope_note}


def _unit_card(unit: dict[str, Any], *, detailed: bool) -> dict[str, Any]:
    card = {key: unit.get(key) for key in ("id", "name", "file", "line_start", "line_end")}
    card["description"] = unit["summary"][:900 if detailed else 350]
    if detailed:
        numbered = "\n".join(f"{int(unit['line_start']) + offset}: {line}"
                              for offset, line in enumerate(unit.get("code_excerpt", "").splitlines()))
        card.update({"conditions": unit.get("conditions", []), "numbered_source": numbered})
    return card


SELECT_PROMPT = """你是需求到源码函数的候选检索器。输入是一条需求和本地检索初筛出的函数摘要；初筛可能遗漏实现。
依据行为、条件、结果及文档适用配置选择最多 8 个可能实现该需求的函数，尽量保证召回；不要依赖变量名与业务术语的字面相同。注意工程中可能同时存在未启用的替代实现，不要将它们当成当前配置的实现。
不能凭空捏造函数 ID。若没有合理候选，返回空数组。只输出 JSON：{"unit_ids":["..."]}。"""

JUDGE_PROMPT = """你是需求与代码证据的审查员。只用提供的函数描述、条件和源码片段判断各需求步骤。
本轮不提供术语数据字典，不要仅凭变量名相似或不同断定行为一致或冲突。只针对文档适用范围和条件判定；未启用的替代实现不能证明当前需求已实现，也不能直接证明冲突。
对每个 step_id 返回一个结论：supported（行为有明确代码证据）、partial（部分实现）、conflict（代码证据明确相反）、unresolved（证据不足）。
每个非 unresolved 结论必须引用一个或多个输入函数 ID，并给出直接包含所述行为的实际源码行号；行号必须在 numbered_source 中可见，不得只引用相邻的注释或控制结构来替代关键语句，不得杜撰代码。
一条步骤可对应多个函数。不能找到实现时用 unresolved，不能把缺少候选直接断定为冲突。
严格输出 JSON：{"decisions":[{"step_id":"...","verdict":"supported|partial|conflict|unresolved","unit_ids":["..."],"evidence":[{"unit_id":"...","line_start":1,"line_end":2,"observation":"..."}],"reason":"简短解释"}]}。"""


def _normalize_decisions(answer: dict[str, Any], steps: list[dict[str, Any]],
                         units: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {step["id"]: step for step in steps}
    result: dict[str, dict[str, Any]] = {}
    for item in answer.get("decisions", []):
        if not isinstance(item, dict) or item.get("step_id") not in by_id:
            continue
        sid = item["step_id"]
        verdict = item.get("verdict", "unresolved")
        if verdict not in {"supported", "partial", "conflict", "unresolved"}:
            verdict = "unresolved"
        evidence = []
        for ref in item.get("evidence", []):
            if not isinstance(ref, dict) or ref.get("unit_id") not in units:
                continue
            unit = units[ref["unit_id"]]
            try:
                start, end = int(ref["line_start"]), int(ref["line_end"])
            except (KeyError, TypeError, ValueError):
                continue
            if not (int(unit["line_start"]) <= start <= end <= int(unit["line_end"])):
                continue
            source_lines = unit.get("code_excerpt", "").splitlines()
            first = start - int(unit["line_start"])
            last = end - int(unit["line_start"])
            if first < 0 or last >= len(source_lines):
                continue
            snippet = "\n".join(f"{int(unit['line_start']) + index}: {source_lines[index]}"
                                for index in range(first, last + 1))
            evidence.append({"unit_id": unit["id"], "file": unit["file"],
                             "line_start": start, "line_end": end,
                             "observation": str(ref.get("observation", ""))[:500],
                             "snippet": snippet[:3000]})
        invalidated = verdict != "unresolved" and not evidence
        if invalidated:
            verdict = "unresolved"
        unit_ids = sorted({ref["unit_id"] for ref in evidence})
        result[sid] = {"step_id": sid, "verdict": verdict, "unit_ids": unit_ids,
                       "evidence": evidence,
                       "reason": (("模型未给出有效源码行号，原结论未采纳。" if invalidated else "")
                                  + str(item.get("reason", "")))[:1000]}
    return [result.get(step["id"], {"step_id": step["id"], "verdict": "unresolved",
                                     "unit_ids": [], "evidence": [], "reason": "模型未返回有效结论"}) for step in steps]


def match_requirement(req: dict[str, Any], units: list[dict[str, Any]],
                      config: dict[str, str], scope_note: str = "") -> dict[str, Any]:
    available = {unit["id"]: unit for unit in units}
    selected, first_usage = _chat(config, SELECT_PROMPT,
                                  {"requirement": _requirement_card(req, scope_note),
                                   "functions": [_unit_card(unit, detailed=False) for unit in units]}, 1500)
    ids = list(dict.fromkeys(value for value in selected.get("unit_ids", [])
                             if isinstance(value, str) and value in available))[:8]
    decisions: list[dict[str, Any]] = []
    usages = [first_usage]
    raw_judgments = []
    for offset in range(0, len(req["steps"]), 4):
        batch = req["steps"][offset:offset + 4]
        if not ids:
            decisions.extend(_normalize_decisions({}, batch, {}))
            continue
        selected_units = {uid: available[uid] for uid in ids}
        answer, usage = _chat(config, JUDGE_PROMPT,
                              {"requirement": _requirement_card(req, scope_note) | {
                                  "steps": [{"id": step["id"], "text": step["text"]} for step in batch]},
                               "functions": [_unit_card(selected_units[uid], detailed=True) for uid in ids]}, 3500)
        usages.append(usage)
        raw_judgments.append(answer)
        decisions.extend(_normalize_decisions(answer, batch, selected_units))
    return {"requirement_id": req["id"], "retrieval_pool": [unit["id"] for unit in units],
            "shortlist": ids, "decisions": decisions,
            "raw_judgments": raw_judgments, "usage": usages}


def match_project(requirements: list[dict[str, Any]], units: list[dict[str, Any]],
                  config: dict[str, str], output: Path, workers: int = 3,
                  scope_note: str = "") -> dict[str, Any]:
    checkpoints = output / "llm_checkpoints"
    checkpoints.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict[str, Any]] = {}
    pending = []
    index = CandidateIndex(units) if len(units) > 96 else None
    unit_digest = hashlib.sha256(json.dumps(units, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    prompt_digest = hashlib.sha256((SELECT_PROMPT + JUDGE_PROMPT).encode("utf-8")).hexdigest()
    for req in requirements:
        pool = index.preselect(req) if index else units
        fingerprint = hashlib.sha256((unit_digest + json.dumps(req, ensure_ascii=False, sort_keys=True)
                                      + config["model"] + config["base_url"] + prompt_digest
                                      + json.dumps([unit["id"] for unit in pool]) + scope_note).encode("utf-8")).hexdigest()
        path = checkpoints / (re.sub(r"[^A-Za-z0-9_-]", "_", req["id"]) + ".json")
        if path.is_file():
            saved = json.loads(path.read_text(encoding="utf-8"))
            if saved.get("fingerprint") == fingerprint and saved.get("requirement_id") == req["id"]:
                results[req["id"]] = saved
                continue
        pending.append((req, pool, path, fingerprint))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(match_requirement, req, pool, config, scope_note): (req, path, fingerprint)
                   for req, pool, path, fingerprint in pending}
        for future in as_completed(futures):
            req, path, fingerprint = futures[future]
            result = future.result()
            result["model"] = config["model"]
            result["fingerprint"] = fingerprint
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            results[req["id"]] = result
            print(f"[match] {len(results)}/{len(requirements)} {req['id']}", flush=True)
    ordered = [results[req["id"]] for req in requirements]
    return {"model": config["model"], "mode": "llm_no_dictionary", "prompt_digest": prompt_digest,
            "requirements": ordered,
            "decisions": [decision for item in ordered for decision in item["decisions"]]}
