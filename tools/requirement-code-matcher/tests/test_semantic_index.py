import tempfile
import unittest
from pathlib import Path

from candidate_index import CandidateIndex
from semantic_index import HybridIndex


class FakeEmbedder:
    def encode(self, texts):
        return [[1.0, 0.0] if "测速" in text or "rotor" in text else [0.0, 1.0]
                for text in texts]


class HybridIndexTests(unittest.TestCase):
    def test_semantic_recalls_function_without_shared_words_and_reuses_disk_cache(self):
        units = [
            {"id": "f1", "name": "generic", "file": "a.c", "summary": "rotor measurement"},
            {"id": "f2", "name": "other", "file": "b.c", "summary": "serial output"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "vectors.json"
            index = HybridIndex(CandidateIndex(units), FakeEmbedder(), Path(directory), cache)
            self.assertEqual(index.units[index.rank("测速")[0][0]]["id"], "f1")
            self.assertTrue(cache.exists())
            second = HybridIndex(CandidateIndex(units), FakeEmbedder(), Path(directory), cache)
            self.assertEqual(second.identity, index.identity)

    def test_first_lexical_batch_is_preserved(self):
        units = [{"id": str(i), "name": f"symbol{i}", "file": "x.c",
                  "summary": "rotor measurement" if i == 8 else f"ordinary {i}"}
                 for i in range(10)]
        with tempfile.TemporaryDirectory() as directory:
            lexical = CandidateIndex(units)
            hybrid = HybridIndex(lexical, FakeEmbedder(), Path(directory),
                                 Path(directory) / "vectors.json")
            query = "symbol0"
            lexical_first = [i for i, _ in lexical.rank(query)[:8]]
            self.assertEqual([i for i, _ in hybrid.rank(query)[:len(lexical_first)]],
                             lexical_first)


if __name__ == "__main__":
    unittest.main()
