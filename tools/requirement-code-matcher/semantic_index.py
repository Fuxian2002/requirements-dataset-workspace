"""Optional local embedding retrieval fused with the existing lexical index.

Embedding scores only rank candidates. They never count as source evidence.
"""
from __future__ import annotations

import hashlib
import json
import threading
from pathlib import Path
from typing import Any

from candidate_index import CandidateIndex


def unit_text(unit: dict[str, Any]) -> str:
    return "\n".join(str(unit.get(key, "")) for key in
                     ("name", "file", "summary", "conditions", "inputs", "outputs"))[:2600]


class LocalEmbedder:
    def __init__(self, model_path: Path):
        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("本地 embedding 需要安装 requirements-embedding.txt") from exc
        if not model_path.is_dir():
            raise FileNotFoundError(f"embedding 模型目录不存在: {model_path}")
        self.torch = torch
        torch.set_num_threads(min(4, torch.get_num_threads()))
        self.tokenizer = AutoTokenizer.from_pretrained(str(model_path), local_files_only=True)
        self.model = AutoModel.from_pretrained(str(model_path), local_files_only=True).eval()
        self.lock = threading.Lock()

    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        with self.lock, self.torch.no_grad():
            for offset in range(0, len(texts), 16):
                batch = self.tokenizer(texts[offset:offset + 16], padding=True,
                                       truncation=True, max_length=512, return_tensors="pt")
                hidden = self.model(**batch).last_hidden_state
                mask = batch["attention_mask"].unsqueeze(-1)
                pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1)
                pooled = self.torch.nn.functional.normalize(pooled, p=2, dim=1)
                vectors.extend(pooled.cpu().tolist())
        return vectors


class HybridIndex:
    """Reciprocal-rank fusion; lexical and semantic channels each keep a vote."""

    def __init__(self, lexical: CandidateIndex, embedder: LocalEmbedder,
                 model_path: Path, cache_path: Path, semantic_weight: float = 1.0):
        self.lexical = lexical
        self.units = lexical.units
        self.by_file = lexical.by_file
        self.embedder = embedder
        self.semantic_weight = semantic_weight
        self.query_cache: dict[str, list[float]] = {}
        self.query_lock = threading.Lock()
        identity = hashlib.sha256(json.dumps({"model": str(model_path.resolve()),
                                                "units": [(u["id"], unit_text(u)) for u in self.units]},
                                               ensure_ascii=False).encode("utf-8")).hexdigest()
        self.identity = identity
        if cache_path.exists():
            try:
                cached = json.loads(cache_path.read_text(encoding="utf-8"))
                if cached.get("identity") == identity and len(cached.get("vectors", [])) == len(self.units):
                    self.vectors = cached["vectors"]
                    return
            except (ValueError, OSError):
                pass
        self.vectors = embedder.encode([unit_text(u) for u in self.units])
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({"identity": identity, "vectors": self.vectors}), encoding="utf-8")

    def rank(self, query: str) -> list[tuple[int, float]]:
        lexical = self.lexical.rank(query)
        with self.query_lock:
            vector = self.query_cache.get(query)
            if vector is None:
                vector = self.embedder.encode([query])[0]
                self.query_cache[query] = vector
        semantic = sorted(range(len(self.units)),
                          key=lambda i: (-sum(x * y for x, y in zip(vector, self.vectors[i])),
                                         self.units[i]["id"]))
        scores: dict[int, float] = {}
        for position, (index, _) in enumerate(lexical):
            scores[index] = scores.get(index, 0.0) + 1.0 / (60 + position + 1)
        for position, index in enumerate(semantic):
            scores[index] = scores.get(index, 0.0) + self.semantic_weight / (60 + position + 1)
        # Exact names and identifiers are unusually valuable for source search.
        # Preserve their first batch and use semantics to diversify later rounds.
        protected = [index for index, _ in lexical[:8]]
        protected_set = set(protected)
        rest = sorted(((index, score) for index, score in scores.items()
                       if index not in protected_set),
                      key=lambda item: (-item[1], self.units[item[0]]["id"]))
        return [(index, scores[index]) for index in protected] + rest
