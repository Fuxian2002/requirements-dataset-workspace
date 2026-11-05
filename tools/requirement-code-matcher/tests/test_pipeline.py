import json
import tempfile
import unittest
from pathlib import Path
import sys

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from codecomp_bridge import adapt_graph
from candidate_index import CandidateIndex
from llm_match import _normalize_decisions
from main import extract_requirements, load_decisions, load_dictionary, propose_dictionary, resolve_document, retrieve, split_steps


class PipelineTests(unittest.TestCase):
    def test_functional_table_values_join_caption_step(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "table.docx"
            doc = Document()
            doc.add_heading("DOC-FREQ21 限值", level=3)
            for text in ("a. 需求标识：DOC-FREQ21", "b. 功能描述：验证电压限值",
                         "c. 调用条件：采集完成", "d. 输入：电压", "e. 输出：状态",
                         "f. 处理：比较限值。", "表 3.2-1 电池限值"):
                doc.add_paragraph(text)
            table = doc.add_table(rows=2, cols=2)
            table.cell(0, 0).text, table.cell(0, 1).text = "参数", "MSL"
            table.cell(1, 0).text, table.cell(1, 1).text = "电压下界 mV", "1500"
            doc.save(path)
            output = extract_requirements(path)
        req = output["requirements"][0]
        self.assertIn("参数：电压下界 mV；MSL：1500", req["steps"][1]["text"])
        self.assertEqual(req["context_tables"][0]["rows"][0], ["电压下界 mV", "1500"])

    def test_figure_caption_is_not_a_processing_step(self):
        lines = [{"text": "图 3.2-2 测量数据处理链", "paragraph": 4},
                 {"text": "图 3.2-2 中的数据并非同步采样。", "paragraph": 5}]
        steps = split_steps(lines, "R")
        self.assertEqual([x["text"] for x in steps], ["图 3.2-2 中的数据并非同步采样。"])
        self.assertEqual(steps[0]["id"], "R/S02")

    def test_extracts_paragraph_steps_and_table_requirements(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.docx"
            doc = Document()
            doc.add_heading("功能需求", level=2)
            doc.add_heading("驻留流启动", level=3)
            for text in ("a. 需求标识：MD-FREQ-08", "b. 功能描述：启动驻留流", "c. 调用条件：收到命令",
                         "d. 输入：表选择掩码", "e. 输出：启动事件", "f. 处理：",
                         "（1）读取表选择掩码；", "（2）启动驻留流。"):
                doc.add_paragraph(text)
            table = doc.add_table(rows=1, cols=3)
            for cell, text in zip(table.rows[0].cells, ("序号", "编号", "描述")):
                cell.text = text
            row = table.add_row()
            for cell, text in zip(row.cells, ("1", "MD-SREQ-01", "错误命令不得启动驻留流")):
                cell.text = text
            doc.save(path)
            output = extract_requirements(path)
        self.assertEqual([x["id"] for x in output["requirements"]], ["MD-FREQ-08", "MD-SREQ-01"])
        self.assertEqual(len(output["requirements"][0]["steps"]), 2)
        self.assertEqual(output["requirements"][1]["steps"][0]["text"], "错误命令不得启动驻留流")
        self.assertEqual(output["issues"], [])

    def test_dictionary_is_candidate_until_confirmed(self):
        req = {"id": "R1", "title": "驻留表处理", "description": "启动驻留表",
               "condition": "", "inputs": "驻留表", "outputs": "启动事件", "processing": "读取驻留表",
               "steps": [{"id": "R1/S01", "text": "读取驻留表", "paragraph": 7}]}
        unit = {"id": "U1", "name": "Start", "file": "start.c", "line_start": 1, "line_end": 9,
                "summary": "启动驻留表", "conditions": [], "steps": ["读取配置"],
                "reads": ["MD_DwellTable"], "writes": [], "outputs": ["启动事件"],
                "errors": [], "symbols": ["MD_DwellTable"]}
        proposals = propose_dictionary([req], [unit], [])
        self.assertTrue(any(x["term"] == "驻留表" and x["symbol"] == "MD_DwellTable" for x in proposals))
        before = retrieve([req], [unit], [])
        mapping = {"term": "驻留表", "symbol": "MD_DwellTable", "status": "confirmed",
                   "relation": "same_as", "evidence": "人工复核"}
        after = retrieve([req], [unit], [mapping])
        self.assertGreater(after["steps"][0]["candidates"][0]["score"],
                           before["steps"][0]["candidates"][0]["score"])
        self.assertEqual(after["steps"][0]["candidates"][0]["status"], "candidate_unverified")

    def test_extracts_headed_and_unnumbered_constraints(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "constraints.docx"
            doc = Document()
            doc.add_heading("DOC-FREQ01 功能", level=3)
            doc.add_paragraph("a. 需求标识：DOC-FREQ01")
            doc.add_paragraph("b. 功能描述：执行任务")
            doc.add_paragraph("f. 处理：")
            doc.add_paragraph("（1）执行任务。")
            doc.add_heading("3.3 性能需求", level=2)
            doc.add_heading("DOC-PREQ01 时序", level=3)
            doc.add_paragraph("任务应按下表执行。")
            performance_table = doc.add_table(rows=1, cols=2)
            performance_table.rows[0].cells[0].text = "任务"
            performance_table.rows[0].cells[1].text = "周期"
            performance_row = performance_table.add_row()
            performance_row.cells[0].text = "Engine"
            performance_row.cells[1].text = "10 ms"
            doc.add_heading("3.4 可靠性和安全性需求", level=2)
            doc.add_paragraph("异常时应停止输出。")
            table = doc.add_table(rows=1, cols=2)
            table.rows[0].cells[0].text = "对象"
            table.rows[0].cells[1].text = "规则"
            row = table.add_row()
            row.cells[0].text = "驱动"
            row.cells[1].text = "故障后复位"
            doc.save(path)
            output = extract_requirements(path)
        self.assertEqual(len(output["requirements"]), 4)
        self.assertIn("DOC-PREQ01", {x["id"] for x in output["requirements"]})
        performance = next(x for x in output["requirements"] if x["id"] == "DOC-PREQ01")
        self.assertEqual(len(performance["context_tables"]), 1)
        self.assertIn("任务：Engine；周期：10 ms", performance["steps"][0]["text"])
        self.assertEqual(sum(x["origin_kind"] == "unnumbered_constraint" for x in output["requirements"]
                             if "origin_kind" in x), 2)

    def test_codecomp_graph_adapter_keeps_evidence_and_filters_tests(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            source.mkdir()
            path = Path(directory) / "graph.json"
            graph = {"repo_label": "sample", "schema_version": "0.5",
                     "parser": {"backend": "fallback"},
                     "nodes": [
                         {"id": "U1", "name": "Start", "description": "启动驻留表",
                          "inputs": [{"name": "DwellTable", "comment": "驻留表"}],
                          "outputs": [{"name": "Started", "comment": "启动事件"}],
                          "evidence": {"file": "src/start.c", "start_line": 3,
                                       "end_line": 12, "code": "void Start(void) {}"}},
                         {"id": "T1", "name": "Stub", "description": "测试桩",
                          "evidence": {"file": "unit-test/stubs/start.c"}}],
                     "edges": [{"type": "control", "source": "U1", "condition": "表有效"}],
                     "evidence_index": {"globals": [{"name": "DwellTable", "comment": "驻留表"}]}}
            path.write_text(json.dumps(graph, ensure_ascii=False), encoding="utf-8")
            output = adapt_graph(path, source)
            self.assertEqual(len(output["units"]), 1)
            self.assertEqual(output["graph"]["excluded_test_nodes"], 1)
            self.assertEqual(output["units"][0]["conditions"], ["表有效"])
            self.assertEqual(output["units"][0]["code_excerpt"], "void Start(void) {}")
            self.assertTrue(any(h["symbol"] == "DwellTable" and h["comment"] == "驻留表"
                                for h in output["data_hints"]))

    def test_decision_requires_valid_evidence_and_units(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.json"
            path.write_text(json.dumps({"decisions": [{"step_id": "R1/S01", "unit_ids": ["U1"],
                "overall": "matched", "dimensions": {"action": "supported"}, "evidence": []}]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "需要代码单元与证据"):
                load_decisions(path, {"R1/S01"}, {"U1"})
            path.write_text(json.dumps({"decisions": [{"step_id": "R1/S01", "unit_ids": ["U1"],
                "overall": "matched", "dimensions": {"action": "supported"},
                "evidence": ["U1:10-12"]}]}), encoding="utf-8")
            self.assertEqual(load_decisions(path, {"R1/S01"}, {"U1"})[0]["overall"], "matched")

    def test_online_document_rejects_non_github_host(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "仅接受"):
                resolve_document("https://example.com/file.docx", Path(directory))

    def test_dictionary_cannot_cross_code_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dictionary.json"
            path.write_text(json.dumps({"project": "P", "revision": "old", "configuration": "C",
                "mappings": [{"term": "数据", "symbol": "data", "status": "confirmed",
                              "relation": "same_as", "evidence": "checked"}]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "revision"):
                load_dictionary(path, {"project": "P", "revision": "new", "configuration": "C"})

    def test_llm_decision_requires_in_range_code_evidence(self):
        steps = [{"id": "R1/S01", "text": "启动"}]
        units = {"U1": {"id": "U1", "file": "src/a.c", "line_start": 10, "line_end": 20,
                        "code_excerpt": "\n".join(f"line {i}" for i in range(10, 21))}}
        answer = {"decisions": [{"step_id": "R1/S01", "verdict": "supported",
                                 "evidence": [{"unit_id": "U1", "line_start": 21,
                                               "line_end": 22, "observation": "启动"}]}]}
        self.assertEqual(_normalize_decisions(answer, steps, units)[0]["verdict"], "unresolved")
        answer["decisions"][0]["evidence"][0].update(line_start=12, line_end=14)
        decision = _normalize_decisions(answer, steps, units)[0]
        self.assertEqual(decision["verdict"], "supported")
        self.assertEqual(decision["unit_ids"], ["U1"])
        self.assertIn("12: line 12", decision["evidence"][0]["snippet"])

    def test_large_graph_preselection_uses_behavior_terms(self):
        units = [{"id": f"U{i}", "name": "task", "file": f"f{i}.c",
                  "summary": "电池均衡通道控制" if i == 5 else "遥测通信状态输出"}
                 for i in range(100)]
        req = {"title": "均衡", "description": "控制电池均衡", "condition": "",
               "inputs": "", "outputs": "", "steps": [{"text": "设置均衡通道"}]}
        selected = CandidateIndex(units).preselect(req, limit=20)
        self.assertIn("U5", [unit["id"] for unit in selected])

    def test_preselection_includes_nearby_function_for_inverse_operation(self):
        units = [{"id": f"U{i}", "name": f"helper{i}", "file": f"f{i}.c",
                  "line_start": 10, "summary": "导航状态更新"} for i in range(100)]
        units[4].update(name="absolute_to_relative", file="coords.c", line_start=200,
                        summary="绝对位置转相对位置")
        units[5].update(name="rel2abs", file="coords.c", line_start=225,
                        summary="将 rel.x 乘以 90 加入 lon_origin")
        req = {"title": "坐标", "description": "相对位置与绝对位置转换", "condition": "",
               "inputs": "", "outputs": "", "steps": [{"text": "绝对位置转相对位置"}]}
        selected = CandidateIndex(units).preselect(req, limit=20)
        self.assertIn("U5", [unit["id"] for unit in selected])


if __name__ == "__main__":
    unittest.main()
