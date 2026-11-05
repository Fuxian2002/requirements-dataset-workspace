import unittest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from match_v3 import applicable_variant, audit_periodic_counters, can_endianness_windows, can_id_definition_windows, checkpoint_key, claim_input_text, claim_source_windows, claim_verdicts, evidence_valid, explicit_source_symbols, hint_functions, hint_source_windows, judge, limit_config_windows, macro_context_windows, normalize_claims, pulse_scale_windows, requirement_anchor_ids, source_digest, step_label
from llm_match import load_model_config
from codecomp_bridge import verify_graph_source
from source_units_v3 import SourceUnits


class V3EvidenceTests(unittest.TestCase):
    def test_conditional_module_indexes_public_and_lowercase_function_bodies(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "MatrixPilot" / "service.c"
            path.parent.mkdir(parents=True)
            path.write_text("#if ENABLE_SERVICE\n"
                            "void preflight(void);\n"
                            "void preflight(void)\n{\n  USBDeviceInit();\n}\n"
                            "static inline void MissionCount(int value)\n"
                            "{\n  send_count(value);\n}\n#endif\n", encoding="utf-8")
            functions = [u for u in SourceUnits(Path(folder)).units
                         if u["kind"] == "source_function"]
            self.assertEqual([u["name"] for u in functions], ["preflight", "MissionCount"])
            self.assertIn("USBDeviceInit", functions[0]["code_excerpt"])

    def test_non_src_project_indexes_main_configuration_macros(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Config" / "options.h"
            path.parent.mkdir(parents=True)
            path.write_text("#define MODE_SWITCH_THRESHOLD_HIGH 3400\n", encoding="utf-8")
            units = SourceUnits(Path(folder))
            found = units.by_symbol["MODE_SWITCH_THRESHOLD_HIGH"]
            self.assertEqual(found[0]["kind"], "macro")
            self.assertEqual(found[0]["file"], "Config/options.h")

    def test_macro_context_exposes_adjacent_channel_definitions(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Config" / "options.h"
            path.parent.mkdir(parents=True)
            path.write_text("\n".join([
                "#define THROTTLE_INPUT_CHANNEL CHANNEL_3",
                "#define AILERON_INPUT_CHANNEL CHANNEL_1",
                "#define ELEVATOR_INPUT_CHANNEL CHANNEL_2",
                "#define RUDDER_INPUT_CHANNEL CHANNEL_5",
                "#define MODE_SWITCH_INPUT_CHANNEL CHANNEL_4"]), encoding="utf-8")
            units = SourceUnits(Path(folder))
            selected = units.by_symbol["AILERON_INPUT_CHANNEL"]
            windows = macro_context_windows("默认输入通道", selected, units)
            self.assertEqual(len(windows), 1)
            self.assertIn("RUDDER_INPUT_CHANNEL CHANNEL_5", windows[0]["code_excerpt"])
            self.assertIn("MODE_SWITCH_INPUT_CHANNEL CHANNEL_4", windows[0]["code_excerpt"])

    def test_macro_context_finds_symbols_touching_chinese_text(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Config" / "options.h"
            path.parent.mkdir(parents=True)
            path.write_text("#define SERVOSAT 1.0\n", encoding="utf-8")
            windows = macro_context_windows("按SERVOSAT=1.0限幅", [], SourceUnits(Path(folder)))
            self.assertEqual(len(windows), 1)
            self.assertIn("SERVOSAT 1.0", windows[0]["code_excerpt"])

    def test_pulse_scale_windows_include_conversion_and_timer_use(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "libUDB" / "servoOut.c"
            path.parent.mkdir(parents=True)
            path.write_text("#define SCALE_FOR_PWM_OUT(x) (x/2)\n" +
                            "int unused;\n" * 12 +
                            "PR4 = SCALE_FOR_PWM_OUT(200); // 0.1ms\n" +
                            "PR4 = SCALE_FOR_PWM_OUT(udb_pwOut[channel]);\n",
                            encoding="utf-8")
            windows = pulse_scale_windows("2000 对应 1000 μs", SourceUnits(Path(folder)))
            self.assertTrue(any("0.1ms" in u["code_excerpt"] for u in windows))
            self.assertTrue(any("x/2" in u["code_excerpt"] for u in windows))

    def test_requirement_anchor_uses_distinct_matched_steps_only(self):
        req = {"steps": [{"id": f"R/S{i}"} for i in range(1, 6)]}
        baseline = {f"R/S{i}": {"verdict": "matched", "evidence": [
            {"unit_id": "func:a.c:10:Work#L20"},
            {"unit_id": "func:a.c:10:Work#L30"}]}
            for i in range(1, 4)}
        baseline["R/S4"] = {"verdict": "not_matched", "evidence": [
            {"unit_id": "func:b.c:10:Other"}]}
        self.assertEqual(requirement_anchor_ids(req, baseline), ["func:a.c:10:Work"])

    def test_non_src_project_indexes_desktop_tool_and_project_xml(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            tool = root / "Tools" / "analyzer" / "analyze.pyw"
            tool.parent.mkdir(parents=True)
            tool.write_text("def export_kml():\n    return 'flight.kml'\n", encoding="utf-8")
            config = root / "Config" / "project.xml"
            config.parent.mkdir(parents=True)
            config.write_text("<targetDevice>dsPIC33</targetDevice>\n", encoding="utf-8")
            source = SourceUnits(root)
            self.assertTrue(any(u["file"] == "Tools/analyzer/analyze.pyw" for u in source.units))
            self.assertTrue(any(u["file"] == "Config/project.xml" for u in source.units))

    def test_checkpoint_key_ignores_other_document_edits_and_paragraph_shifts(self):
        inputs = {"document_sha256": "old", "graph_sha256": "g", "source_sha256": "s",
                  "prompt_hash": "p", "model": "m", "max_rounds": 2}
        step = {"id": "R/S01", "text": "perform action", "paragraph": 12}
        req = {"id": "R", "description": "action", "heading_paragraph": 6, "steps": [step]}
        key = checkpoint_key(inputs, req, step)
        changed = {**inputs, "document_sha256": "new"}
        shifted_step = {**step, "paragraph": 120}
        shifted_req = {**req, "heading_paragraph": 114, "steps": [shifted_step]}
        self.assertEqual(key, checkpoint_key(changed, shifted_req, shifted_step))
        self.assertNotEqual(key, checkpoint_key(changed, {**shifted_req, "description": "changed"}, shifted_step))

    def test_explicit_symbols_find_conditional_static_body_and_default(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            c_file = root / "src" / "app" / "values.c"
            c_file.parent.mkdir(parents=True)
            c_file.write_text("#if (ENABLED == 0)\n"
                              "static void BMSVL_CopyBaseMeasurementsToValidatedMeasurements(void);\n"
                              "static void BMSVL_CopyBaseMeasurementsToValidatedMeasurements(void) {\n"
                              "  if (updated) copy_values();\n"
                              "}\n#endif\n", encoding="utf-8")
            py_file = root / "tools" / "waf_tools" / "bms_config_model.py"
            py_file.parent.mkdir(parents=True)
            py_file.write_text("redundant_v_t_measurement: bool = False\n", encoding="utf-8")
            source = SourceUnits(root)
            found = explicit_source_symbols("redundant_v_t_measurement "
                                            "BMSVL_CopyBaseMeasurementsToValidatedMeasurements", source)
            self.assertEqual({u["kind"] for u in found}, {"source_function", "default_config"})
            self.assertIn("if (updated)", found[0]["code_excerpt"])

    def test_bootloader_endianness_windows_select_message_tables(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "src" / "bootloader" / "driver" / "config" / "can_cfg.c"
            path.parent.mkdir(parents=True)
            path.write_text("const CAN_RX_MESSAGE_TYPE_s can_rxMessages[] = {CAN_LITTLE_ENDIAN};\n"
                            "const CAN_TX_MESSAGE_TYPE_s can_txMessages[] = {CAN_LITTLE_ENDIAN};\n",
                            encoding="utf-8")
            source = SourceUnits(Path(folder))
            windows = can_endianness_windows("引导程序消息 CAN_LITTLE_ENDIAN", source)
            self.assertTrue(windows)
            self.assertIn("can_txMessages", windows[0]["code_excerpt"])

    def test_limit_table_window_keeps_three_threshold_values(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "conf" / "bms" / "battery_cell_cfg.json"
            path.parent.mkdir(parents=True)
            path.write_text("\n".join(
                f'{{"name": "BC_CURRENT_MAX_CHARGE_{level}_mA", "value": {value}}}'
                for level, value in (("MSL", 180000), ("RSL", 175000), ("MOL", 170000))), encoding="utf-8")
            source = SourceUnits(Path(folder))
            windows = limit_config_windows("表格参数：电流 MOL 170 RSL 175 MSL 180", source)
            self.assertEqual(len(windows), 1)
            self.assertIn("180000", windows[0]["code_excerpt"])
            self.assertIn("170000", windows[0]["code_excerpt"])

    def test_can_id_window_preserves_period_and_phase(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "src" / "app" / "driver" / "config" / "can_cfg_tx-cyclic-message-definitions.h"
            path.parent.mkdir(parents=True)
            path.write_text("\n".join([
                "#define CANTX_BMS_STATE_ID (0x220u)",
                "#define CANTX_BMS_STATE_ID_TYPE (CAN_STANDARD_IDENTIFIER_11_BIT)",
                "#define CANTX_BMS_STATE_PERIOD_ms (100u)",
                "#define CANTX_BMS_STATE_PHASE_ms (0u)",
                "#define CANTX_BMS_STATE_ENDIANNESS (CAN_BIG_ENDIAN)",
                "#define CANTX_BMS_STATE_DLC (CAN_DEFAULT_DLC)",
            ]), encoding="utf-8")
            source = SourceUnits(Path(folder))
            windows = can_id_definition_windows("报文 0x220 周期 100 相位 0", source)
            self.assertEqual(len(windows), 1)
            self.assertIn("CANTX_BMS_STATE_PERIOD_ms (100u)", windows[0]["code_excerpt"])
            self.assertIn("CANTX_BMS_STATE_PHASE_ms (0u)", windows[0]["code_excerpt"])
            self.assertEqual(can_id_definition_windows("报文 0x221", source), [])

    def test_claim_window_finds_action_inside_large_function(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "src" / "app" / "sys.c"
            path.parent.mkdir(parents=True)
            lines = ["void Process(void) {"] + ["tick();"] * 100 + ["SE_InitializeSoc(true, s);"] + ["}"]
            path.write_text("\n".join(lines), encoding="utf-8")
            function = {"id": "f", "name": "Process", "file": "app/sys.c",
                        "line_start": 1, "line_end": len(lines)}
            windows = claim_source_windows([{"text": "初始化 SOC。"}], [function], Path(folder))
            self.assertIn("SE_InitializeSoc", windows[0]["code_excerpt"])

    def test_local_c_macro_is_citable(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "src" / "app" / "rx.c"
            path.parent.mkdir(parents=True)
            path.write_text("#define CAN_SIGNAL_START_BIT (23u)\n", encoding="utf-8")
            source = SourceUnits(Path(folder))
            self.assertEqual(source.by_symbol["CAN_SIGNAL_START_BIT"][0]["line_start"], 1)

    def test_supported_action_with_unverified_condition_stays_unresolved(self):
        unit = {"id": "f", "file": "f.c", "line_start": 1, "line_end": 1,
                "code_excerpt": "do_work();"}
        result = claim_verdicts([{"id": "C1", "text": "仅在静置时执行", "kind": "code"}],
                                {"decisions": [{"claim_id": "C1", "status": "supported",
                                 "evidence": [{"unit_id": "f", "line_start": 1, "line_end": 1}],
                                 "reason": "动作受证，但 AT_REST 触发条件未受证。"}]}, {"f": unit})
        self.assertEqual(result[0]["status"], "unresolved")

    def test_named_afe_variant_rejects_sibling_driver(self):
        req = {"description": "LTC6813-1 状态机执行唤醒"}
        self.assertFalse(applicable_variant(req, {"file": "app/driver/afe/ltc/6806/ltc_6806.c"}))
        self.assertTrue(applicable_variant(req, {"file": "app/driver/afe/ltc/6813-1/ltc_6813-1.c"}))
        self.assertTrue(applicable_variant(req, {"file": "app/driver/afe/ltc/common/ltc.c"}))

    def test_original_function_id_resolves_only_within_visible_window(self):
        visible = {"func:f:10:Work#L20": {"id": "func:f:10:Work#L20", "file": "f.c",
                   "line_start": 20, "line_end": 21, "code_excerpt": "a();\nb();"}}
        self.assertEqual(len(evidence_valid([{"unit_id": "func:f:10:Work",
                                             "line_start": 21, "line_end": 21}], visible)), 1)
        self.assertEqual(evidence_valid([{"unit_id": "func:f:10:Work",
                                          "line_start": 22, "line_end": 22}], visible), [])

    def test_second_round_uses_newly_discovered_symbol(self):
        units = [{"id": "f1", "name": "Run", "file": "app/a.c", "line_start": 1,
                  "line_end": 1, "kind": "function", "summary": "Run", "code_excerpt": "Run();"},
                 {"id": "f2", "name": "Initialize", "file": "app/b.c", "line_start": 1,
                  "line_end": 1, "kind": "function", "summary": "Initialize", "code_excerpt": "Initialize();"}]
        seen = []

        def answer(_config, _prompt, payload, _limit):
            seen.append([unit["id"] for unit in payload["code_units"]])
            if "f2" in seen[-1]:
                return {"decisions": [{"claim_id": "C1", "status": "supported",
                         "evidence": [{"unit_id": "f2", "line_start": 1, "line_end": 1}],
                         "reason": "调用初始化函数"}]}, {}
            return {"decisions": [{"claim_id": "C1", "status": "unresolved"}],
                    "search_hints": ["Initialize"]}, {}

        with patch("match_v3._chat", side_effect=answer):
            result, _ = judge({"id": "R", "title": "", "description": "", "condition": ""},
                              {"id": "R/S01", "text": "初始化"},
                              [{"id": "C1", "text": "初始化", "kind": "code"}],
                              units[:1], {}, 2, units)
        self.assertEqual(seen, [["f1"], ["f2"]])
        self.assertEqual(result["verdict"], "matched")

    def test_economy_stops_after_small_supported_batch(self):
        functions = [{"id": f"f{i}", "name": f"Function{i}", "file": "f.c",
                      "line_start": i, "line_end": i, "kind": "function",
                      "summary": "work", "code_excerpt": "work();"} for i in range(5)]
        sources = [{"id": f"m{i}", "name": f"MACRO{i}", "file": "m.h",
                    "line_start": i, "line_end": i, "kind": "macro",
                    "summary": "value", "code_excerpt": "#define VALUE 1"} for i in range(7)]
        inspected = []
        def answer(_config, _prompt, payload, _limit):
            inspected.append([u["id"] for u in payload["code_units"]])
            return {"decisions": [{"claim_id": "C1", "status": "supported",
                    "evidence": [{"unit_id": "f0", "line_start": 0, "line_end": 0}]}]}, {}
        with patch("match_v3._chat", side_effect=answer):
            result, _ = judge({"id": "R", "title": "", "description": "", "condition": ""},
                              {"id": "R/S01", "text": "work"},
                              [{"id": "C1", "text": "work", "kind": "code"}],
                              functions + sources, {}, 2, economy=True)
        self.assertEqual(result["verdict"], "matched")
        self.assertEqual(len(inspected), 1)
        self.assertEqual(len(inspected[0]), 10)

    def test_exact_search_hint_recovers_missing_function(self):
        units = [{"id": "f1", "name": "FTSK_RunUserCodeEngine"},
                 {"id": "f2", "name": "FTSK_InitializeUserCodeEngine"}]
        hits = hint_functions(["FTSK_InitializeUserCodeEngine"], units, {"f1"})
        self.assertEqual([x["id"] for x in hits], ["f2"])

    def test_search_hint_exposes_line_inside_large_function(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "src" / "app" / "state.c"
            path.parent.mkdir(parents=True)
            path.write_text("\n".join(["void State(void) {"] + ["tick();"] * 30 +
                                      ["LTC_TRANSMIT_WAKE_UP(bus);", "if (BMS_AT_REST) run();"] + ["}"]), encoding="utf-8")
            function = {"name": "State", "file": "app/state.c", "line_start": 1, "line_end": 34}
            hits = hint_source_windows(["LTC_TRANSMIT_WAKE_UP"], [function], Path(folder))
            self.assertEqual(len(hits), 1)
            self.assertIn("LTC_TRANSMIT_WAKE_UP(bus)", hits[0]["code_excerpt"])
            rest = hint_source_windows(["AT_REST"], [function], Path(folder))
            self.assertIn("BMS_AT_REST", rest[0]["code_excerpt"])

    def test_search_hint_exposes_line_in_flat_repository(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "MatrixPilot" / "mode_switch.c"
            path.parent.mkdir(parents=True)
            path.write_text("\n".join(["void Check(void) {"] + ["tick();"] * 25 +
                                      ["if (radio_on) home_req = 1;", "}"]), encoding="utf-8")
            function = {"name": "Check", "file": "MatrixPilot/mode_switch.c",
                        "line_start": 1, "line_end": 28}
            hits = hint_source_windows(["home_req"], [function], Path(folder))
            self.assertEqual(len(hits), 1)
            self.assertIn("home_req = 1", hits[0]["code_excerpt"])

    def test_description_is_reviewed_once(self):
        req = {"description": "启动时建立数据库。", "steps": [
            {"id": "R/S01", "text": "初始化端口扩展器。"},
            {"id": "R/S02", "text": "随后启动任务。"}]}
        self.assertEqual(claim_input_text(req, req["steps"][0]),
                         "启动时建立数据库。\n初始化端口扩展器。")
        self.assertEqual(claim_input_text(req, req["steps"][1]), "随后启动任务。")

    def test_claim_extraction_drops_requirement_restating_metadata(self):
        claims, _ = normalize_claims({"claims": [
            {"text": "需求为计算两个整数的和。", "kind": "code"},
            {"text": "返回 a 与 b 的和。", "kind": "code"}]},
            {"text": "返回 a 与 b 的和。"})
        self.assertEqual([c["text"] for c in claims], ["返回 a 与 b 的和。"])

    def test_source_hash_changes_when_config_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "conf" / "values.json"
            path.parent.mkdir()
            path.write_text('{"threshold": 5}', encoding="utf-8")
            before = source_digest(Path(folder))
            path.write_text('{"threshold": 6}', encoding="utf-8")
            self.assertNotEqual(before, source_digest(Path(folder)))

    def test_reused_graph_must_match_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "simple.c").write_text("int add(void) { return 1; }", encoding="utf-8")
            graph = root / "graph.json"
            graph.write_text('{"nodes":[{"evidence":{"file":"simple.c",'
                             '"start_line":1,"end_line":1,'
                             '"code":"int add(void) { return 2; }"}}]}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                verify_graph_source(graph, root)

    def test_explicit_model_file_overrides_host_environment(self):
        with tempfile.TemporaryDirectory() as folder:
            config_file = Path(folder) / "model.env"
            config_file.write_text("LLM_BASE_URL=https://example.org/v1\nLLM_API_KEY=file-key\nLLM_MODEL=file-model\n")
            with patch.dict(os.environ, {"LLM_BASE_URL": "https://host.example/v1",
                                      "LLM_API_KEY": "host-key", "LLM_MODEL": "host-model"}):
                config = load_model_config(config_file, "")
        self.assertEqual(config, {"base_url": "https://example.org/v1",
                                  "api_key": "file-key", "model": "file-model"})

    def test_missing_evidence_is_not_a_counterexample(self):
        claim = {"id": "C1", "text": "阈值来自配置", "kind": "code"}
        result = claim_verdicts([claim], {"decisions": [{"claim_id": "C1",
            "status": "contradicted", "evidence": [], "reason": "未找到配置"}]}, {})
        self.assertEqual(result[0]["status"], "unresolved")
        self.assertEqual(step_label(result), ("not_matched", "not_found"))

    def test_reset_then_increment_counter_period(self):
        function = {"id": "f", "kind": "function", "name": "RunCyclic100ms",
                    "file": "task.c", "line_start": 1, "line_end": 8,
                    "code_excerpt": "static uint8_t sampleCounter = 0;\n"
                    "if (sampleCounter == PERIOD_1S) {\nrun();\n"
                    "sampleCounter = 0;\n}\nother();\nsampleCounter++;\n}"}
        macro = {"id": "m", "kind": "macro", "name": "PERIOD_1S", "file": "task.h",
                 "line_start": 1, "line_end": 1, "code_excerpt": "#define PERIOD_1S (10u)"}
        claims = [{"id": "C1", "kind": "code", "text": "稳态间隔约 1 s。",
                   "status": "contradicted", "reason": "误算为 11 次", "evidence": []}]
        audit_periodic_counters(claims, {"f": function, "m": macro})
        self.assertEqual(claims[0]["status"], "supported")
        self.assertIn("1000 ms", claims[0]["reason"])
        self.assertEqual(len(claims[0]["evidence"]), 2)


if __name__ == "__main__":
    unittest.main()
