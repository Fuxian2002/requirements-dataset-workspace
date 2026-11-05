import unittest

from report_v2 import requirement_kind


class ReportV2Tests(unittest.TestCase):
    def test_requirement_categories(self):
        self.assertEqual(requirement_kind("FBMS-FREQ12"), ("functional", "功能需求"))
        self.assertEqual(requirement_kind("FBMS-PREQ01"), ("nonfunctional", "性能需求"))
        self.assertEqual(requirement_kind("FBMS-SREQ06"), ("nonfunctional", "安全需求"))


if __name__ == "__main__":
    unittest.main()
