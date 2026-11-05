"""Bounded, source-graph-based candidate expansion; never uses Word trace fields."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from candidate_index import tokens


def expand_functions(functions: list[dict[str, Any]], all_units: list[dict[str, Any]],
                     query: str, *, first_batch: int = 8, total: int = 18,
                     budget: int = 2,
                     ranked_ids: dict[str, int] | None = None,
                     by_file: dict[str, list[int]] | None = None) -> list[dict[str, Any]]:
    """Preserve the first model batch and reserve later slots for graph neighbors."""
    if not functions or budget <= 0:
        return functions[:total]
    by_id = {unit["id"]: unit for unit in all_units}
    selected = {unit["id"] for unit in functions}
    seed = functions[:first_batch]
    cues = set(tokens(query))
    proposals: dict[str, tuple[float, str]] = {}
    if by_file is None:
        by_file = {}
        for index, unit in enumerate(all_units):
            by_file.setdefault(str(unit.get("file", "")), []).append(index)
    for position, unit in enumerate(seed[:4]):
        seed_weight = max(0.0, 2.0 - position * 0.15)
        for relation, weight in (("callees", 5.0), ("callers", 4.5)):
            # Large orchestrators reach many unrelated components.
            if len(unit.get(relation, [])) > 12:
                continue
            for uid in unit.get(relation, []):
                neighbor = by_id.get(uid)
                if neighbor is None or uid in selected:
                    continue
                rank = (ranked_ids or {}).get(uid, len(all_units) + 1)
                if ranked_ids is not None and rank > 80:
                    continue
                overlap = len(cues & set(tokens(str(neighbor.get("name", "")) + " " +
                                                str(neighbor.get("summary", ""))[:450])))
                same_file = neighbor.get("file") == unit.get("file")
                if overlap < 2:
                    continue
                score = (weight + seed_weight + min(overlap, 6) * 0.5 +
                         (1 if same_file else 0) + (1.0 - min(rank, 80) / 80))
                if score > proposals.get(uid, (-1, ""))[0]:
                    proposals[uid] = (score, relation)
        # Same-file siblings can implement the next stage without a direct call.
        for index in by_file.get(str(unit.get("file", "")), []):
            neighbor = all_units[index]
            uid = neighbor["id"]
            if uid in selected or neighbor.get("file") != unit.get("file"):
                continue
            rank = (ranked_ids or {}).get(uid, len(all_units) + 1)
            if ranked_ids is not None and rank > 80:
                continue
            start = neighbor.get("line_start")
            origin = unit.get("line_start")
            if not isinstance(start, int) or not isinstance(origin, int):
                continue
            distance = abs(start - origin)
            if distance > 250:
                continue
            overlap = len(cues & set(tokens(str(neighbor.get("name", "")) + " " +
                                            str(neighbor.get("summary", ""))[:450])))
            if overlap < 2:
                continue
            score = (1.5 + seed_weight + min(overlap, 6) * 0.5 +
                     (1 if distance <= 70 else 0) + (1.0 - min(rank, 80) / 80))
            if score > proposals.get(uid, (-1, ""))[0]:
                proposals[uid] = (score, "same_file")
    ranked = sorted(proposals, key=lambda uid: (-proposals[uid][0],
                                                by_id[uid].get("file", ""),
                                                by_id[uid].get("line_start", 0), uid))
    added = [{**by_id[uid], "retrieval_origin": "structure:" + proposals[uid][1]}
             for uid in ranked[:budget]]
    protected = functions[:first_batch]
    seen = {u["id"] for u in protected + added}
    return (protected + added + [u for u in functions[first_batch:] if u["id"] not in seen])[:total]


def expand_macros(functions: list[dict[str, Any]], source_units: list[dict[str, Any]],
                  query: str, *, budget: int = 2) -> list[dict[str, Any]]:
    """Find exact macro names referenced by the selected functions."""
    if budget <= 0:
        return []
    code = "\n".join(str(u.get("code_excerpt", "")) for u in functions[:12])
    symbols = set(re.findall(r"\b[A-Z][A-Z0-9_]{4,}\b", code))
    cues = set(tokens(query))
    files = {Path(str(u.get("file", ""))).stem.lower() for u in functions[:12]}
    found = []
    for unit in source_units:
        name = str(unit.get("name", ""))
        if unit.get("kind") != "macro" or name not in symbols:
            continue
        overlap = len(cues & set(tokens(name + " " + str(unit.get("summary", ""))[:200])))
        same_module = Path(str(unit.get("file", ""))).stem.lower() in files
        score = overlap * 2 + (1 if same_module else 0)
        if overlap >= 2:
            found.append((score, unit))
    found.sort(key=lambda pair: (-pair[0], pair[1]["file"], pair[1]["line_start"]))
    return [{**unit, "retrieval_origin": "structure:macro"} for _, unit in found[:budget]]
