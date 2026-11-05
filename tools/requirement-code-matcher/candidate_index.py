"""High-recall local preselection for large code-understanding graphs.

This stage is deliberately independent of requirement trace appendices and data
dictionaries. It only limits the amount of function text sent to the LLM.
"""
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from typing import Any


def tokens(value: str) -> Counter[str]:
    result: Counter[str] = Counter()
    for run in re.findall(r"[\u4e00-\u9fff]+", value):
        for size in (2, 3):
            result.update(run[index:index + size] for index in range(len(run) - size + 1))
    for run in re.findall(r"[A-Za-z][A-Za-z0-9_]*", value):
        parts = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", run).replace("_", " ").split()
        result.update(part.lower() for part in parts if len(part) > 1)
        if len(run) > 3:
            result[run.lower()] += 1
    return result


class CandidateIndex:
    def __init__(self, units: list[dict[str, Any]]):
        self.units = units
        self.postings: dict[str, list[tuple[int, float]]] = defaultdict(list)
        self.by_file: dict[str, list[int]] = defaultdict(list)
        frequencies = []
        df: Counter[str] = Counter()
        for unit in units:
            text = " ".join([unit.get("name", ""), unit.get("file", ""), unit.get("summary", "")[:1000]])
            term_counts = tokens(text)
            frequencies.append(term_counts)
            df.update(term_counts.keys())
        self.idf = {term: math.log((len(units) + 1) / (count + 1)) + 1 for term, count in df.items()}
        for index, counts in enumerate(frequencies):
            self.by_file[units[index].get("file", "")].append(index)
            norm = math.sqrt(sum(((1 + math.log(value)) * self.idf[term]) ** 2
                                 for term, value in counts.items())) or 1
            for term, value in counts.items():
                self.postings[term].append((index, (1 + math.log(value)) * self.idf[term] / norm))

    def rank(self, query: str) -> list[tuple[int, float]]:
        counts = tokens(query)
        norm = math.sqrt(sum(((1 + math.log(value)) * self.idf[term]) ** 2
                             for term, value in counts.items() if term in self.idf)) or 1
        scores: dict[int, float] = defaultdict(float)
        for term, value in counts.items():
            if term not in self.idf:
                continue
            weight = (1 + math.log(value)) * self.idf[term] / norm
            for index, code_weight in self.postings[term]:
                scores[index] += weight * code_weight
        return sorted(scores.items(), key=lambda item: (-item[1], self.units[item[0]]["id"]))

    def preselect(self, requirement: dict[str, Any], limit: int = 96) -> list[dict[str, Any]]:
        if len(self.units) <= limit:
            return self.units
        context = " ".join(str(requirement.get(key, "")) for key in
                           ("title", "description", "condition", "inputs", "outputs"))
        ranks: dict[int, float] = {}
        for step in requirement["steps"]:
            for index, score in self.rank(context + " " + step["text"])[:max(20, limit // 2)]:
                ranks[index] = max(score, ranks.get(index, 0))
        per_file: Counter[str] = Counter()
        selected = []
        ranked = sorted(ranks.items(), key=lambda item: (-item[1], self.units[item[0]]["id"]))
        primary_limit = max(1, limit - min(32, limit // 3))
        for index, _ in ranked:
            unit = self.units[index]
            file_path = unit.get("file", "")
            if per_file[file_path] >= 12:
                continue
            selected.append(unit)
            per_file[file_path] += 1
            if len(selected) >= primary_limit:
                break
        already = {unit["id"] for unit in selected}
        neighbors: list[tuple[int, int, int]] = []
        for rank_position, (index, _) in enumerate(ranked[:32]):
            unit = self.units[index]
            start = unit.get("line_start")
            if not isinstance(start, int):
                continue
            for other in self.by_file[unit.get("file", "")]:
                other_start = self.units[other].get("line_start")
                if isinstance(other_start, int) and 0 < abs(other_start - start) <= 70:
                    neighbors.append((rank_position, abs(other_start - start), other))
        for _, _, index in sorted(set(neighbors), key=lambda item: (item[0], item[1],
                                                                     self.units[item[2]]["id"])):
            unit = self.units[index]
            if unit["id"] not in already:
                selected.append(unit)
                already.add(unit["id"])
                if len(selected) >= limit:
                    break
        if len(selected) < limit:
            for index, _ in self.rank(context):
                if self.units[index]["id"] not in already:
                    selected.append(self.units[index])
                    already.add(self.units[index]["id"])
                    if len(selected) >= limit:
                        break
        return selected
