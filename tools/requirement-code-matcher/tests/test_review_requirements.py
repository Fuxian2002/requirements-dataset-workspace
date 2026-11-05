import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from docx import Document

from match_v3 import aggregate_v3, step_label
from review_requirements import _recover_description, _review_one, load_review, review_document


class RequirementReviewTests(unittest.TestCase):
    def test_split_and_exclude_preserve_lineage(self):
        req = {"id": "R-FREQ1", "title": "采集并计算", "description": "采集并计算", "steps": [
            {"id": "R-FREQ1/S01", "text": "采集温度并计算平均值", "paragraph": 10},
            {"id": "R-FREQ1/S02", "text": "算法如下", "paragraph": 11}]}
        answer = {"requirement": {"decision": "include", "reason": "源码可核验"}, "steps": [
            {"source_id": "R-FREQ1/S01", "decision": "include", "reason": "两个动作",
             "atomic_steps": [{"text": "采集温度", "category": "acquisition"},
                              {"text": "计算平均值", "category": "computation"}]},
            {"source_id": "R-FREQ1/S02", "decision": "exclude", "reason": "标题",
             "atomic_steps": []}]}
        with patch("review_requirements._chat", return_value=(answer, {"total_tokens": 123})):
            reviewed, log, tokens = _review_one(req, {"model": "test"})
        self.assertEqual(tokens, 123)
        self.assertEqual([s["id"] for s in reviewed["steps"]],
                         ["R-FREQ1/S01-01", "R-FREQ1/S01-02"])
        self.assertEqual(reviewed["steps"][0]["source_step_id"], "R-FREQ1/S01")
        self.assertEqual(log["steps"][1]["decision"], "exclude")

    def test_omitted_source_step_fails_closed(self):
        req = {"id": "R", "steps": [{"id": "R/S01", "text": "读取传感器"}]}
        answer = {"requirement": {"decision": "include"}, "steps": []}
        with patch("review_requirements._chat", return_value=(answer, {})):
            with self.assertRaisesRegex(ValueError, "omitted"):
                _review_one(req, {"model": "test"})

    def test_compound_action_is_held_for_review(self):
        req = {"id": "R", "steps": [{"id": "R/S01", "text": "采集温度并计算平均值"}]}
        answer = {"requirement": {"decision": "include"}, "steps": [
            {"source_id": "R/S01", "decision": "include", "atomic_steps": [
                {"text": "采集温度并计算平均值", "category": "computation"}]}]}
        with patch("review_requirements._chat", return_value=(answer, {})):
            reviewed, log, _ = _review_one(req, {"model": "test"})
        self.assertEqual(reviewed["steps"], [])
        self.assertEqual(log["steps"][0]["decision"], "needs_review")

    def test_description_obligation_rescues_empty_processing_steps(self):
        req = {"id": "R", "description": "每 10 ms 采集电流。"}
        reviewed = {"id": "R", "steps": [], "reviewed_input": True}
        log = {"decision": "exclude", "reason": "无合规可匹配步骤", "steps": [],
               "uncovered_obligations": []}
        answer = {"atomic_steps": [{"text": "每 10 ms 采集电流。", "category": "acquisition"}]}
        with patch("review_requirements._chat", return_value=(answer, {"total_tokens": 12})):
            self.assertEqual(_recover_description(req, reviewed, log, {"model": "test"}), 12)
        self.assertEqual(log["decision"], "include")
        self.assertEqual(reviewed["steps"][0]["id"], "R/DESC-01")

    def test_binary_step_and_three_way_requirement(self):
        claims = [{"kind": "code", "status": "supported"},
                  {"kind": "code", "status": "unresolved"}]
        self.assertEqual(step_label(claims), ("not_matched", "incomplete_evidence"))
        req = [{"id": "R", "title": "", "steps": [{"id": "R/S01"}, {"id": "R/S02"}]}]
        steps = [{"step_id": "R/S01", "verdict": "matched"},
                 {"step_id": "R/S02", "verdict": "not_matched"}]
        self.assertEqual(aggregate_v3(req, steps)[0]["verdict"], "partial")
        steps[0]["verdict"] = "not_matched"
        self.assertEqual(aggregate_v3(req, steps)[0]["verdict"], "unmatched")

    def test_review_cannot_be_reused_for_another_document(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            doc = root / "x.docx"
            doc.write_bytes(b"new word")
            review = root / "review.json"
            review.write_text(json.dumps({"document_sha256": hashlib.sha256(b"old word").hexdigest()}),
                              encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "different Word"):
                load_review(review, doc)

    def test_word_to_review_artifact_excludes_dirty_step(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            doc_path = root / "requirements.docx"
            doc = Document()
            doc.add_heading("测量温度", level=3)
            for line in ("a. 需求标识：X-FREQ1", "b. 功能描述：测量温度",
                         "c. 调用条件：定时触发", "d. 输入：传感器", "e. 输出：温度",
                         "f. 处理：", "（1）采集传感器温度。", "（2）算法如下"):
                doc.add_paragraph(line)
            doc.save(doc_path)
            answer = {"requirement": {"decision": "include", "reason": "功能行为"},
                      "steps": [{"source_id": "X-FREQ1/S01", "decision": "include", "reason": "采集",
                                 "atomic_steps": [{"text": "采集传感器温度。", "category": "acquisition"}]},
                                {"source_id": "X-FREQ1/S02", "decision": "include", "reason": "误判",
                                 "atomic_steps": [{"text": "算法如下", "category": "computation"}]}]}
            output = root / "requirements_review.json"
            with patch("review_requirements._chat", return_value=(answer, {"total_tokens": 7})):
                result = review_document(doc_path, {"model": "test"}, output)
            self.assertEqual(result["selected_step_count"], 1)
            self.assertEqual(result["review"][0]["steps"][1]["decision"], "exclude")
            self.assertTrue(output.with_suffix(".html").exists())
            self.assertEqual(load_review(output, doc_path)["selected_step_count"], 1)
            with patch("review_requirements._chat", side_effect=AssertionError("repeated model call")):
                self.assertEqual(review_document(doc_path, {"model": "test"}, output)[
                    "selected_step_count"], 1)


if __name__ == "__main__":
    unittest.main()
