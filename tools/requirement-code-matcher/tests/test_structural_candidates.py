import unittest

from structural_candidates import expand_functions, expand_macros


class StructuralCandidatesTests(unittest.TestCase):
    def test_call_graph_neighbor_replaces_tail_without_growing_budget(self):
        units = [{"id": f"f{i}", "name": f"function_{i}", "file": "motor.c" if i < 3 else "other.c",
                  "line_start": i * 100 + 1, "summary": "", "callers": [], "callees": [],
                  "code_excerpt": ""} for i in range(22)]
        units[0]["callees"] = ["f20"]
        units[20]["summary"] = "motor speed calculation"
        ordered = units[:18]
        result = expand_functions(ordered, units, "motor speed", budget=4)
        self.assertEqual([u["id"] for u in result[:8]], [u["id"] for u in ordered[:8]])
        self.assertIn("f20", [u["id"] for u in result[8:12]])
        self.assertEqual(len(result), 18)
        self.assertEqual(next(u for u in result if u["id"] == "f20")["retrieval_origin"],
                         "structure:callees")

    def test_macro_requires_exact_reference_and_respects_limit(self):
        functions = [{"file": "MESCpwm.c", "code_excerpt": "PWM_LIMIT = MOTOR_PWM_LIMIT;"}]
        units = [{"id": "m1", "kind": "macro", "name": "MOTOR_PWM_LIMIT",
                  "file": "MESCpwm.h", "line_start": 4, "summary": ""},
                 {"id": "m2", "kind": "macro", "name": "UNRELATED",
                  "file": "other.h", "line_start": 5, "summary": ""}]
        result = expand_macros(functions, units, "MOTOR_PWM_LIMIT", budget=1)
        self.assertEqual([u["id"] for u in result], ["m1"])


if __name__ == "__main__":
    unittest.main()
