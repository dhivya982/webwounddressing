import unittest

from levels import LEVELS
from runner import ERROR_TIPS, check_level


class RunnerTests(unittest.TestCase):
    def test_solutions_pass_and_starters_are_rejected(self):
        self.assertEqual(len(LEVELS), 8)
        for level in LEVELS:
            with self.subTest(level=level["number"], code="solution"):
                passed, message, output = check_level(level, level["solution"])
                self.assertTrue(passed, message)
                self.assertIsInstance(output, str)

            with self.subTest(level=level["number"], code="starter"):
                passed, message, output = check_level(level, level["starter"])
                self.assertFalse(passed)
                self.assertTrue(message)
                self.assertEqual(output, "")

            bonus = level.get("bonus")
            if bonus is not None:
                with self.subTest(level=level["number"], code="bonus solution"):
                    passed, message, output = check_level(bonus, bonus["solution"])
                    self.assertTrue(passed, message)
                    self.assertIsInstance(output, str)

                with self.subTest(level=level["number"], code="bonus starter"):
                    passed, message, output = check_level(bonus, bonus["starter"])
                    self.assertFalse(passed)
                    self.assertTrue(message)
                    self.assertEqual(output, "")

    def test_common_error_tips_exist(self):
        self.assertIn("NameError", ERROR_TIPS)
        self.assertIn("KeyError", ERROR_TIPS)
        self.assertIn("IndentationError", ERROR_TIPS)
        self.assertTrue(ERROR_TIPS["NameError"])
        self.assertTrue(ERROR_TIPS["KeyError"])
        self.assertTrue(ERROR_TIPS["IndentationError"])

    def test_debugging_level_reports_syntax_error_line(self):
        debugging_level = LEVELS[6]
        passed, message, output = check_level(debugging_level, debugging_level["starter"])
        self.assertFalse(passed)
        self.assertIn("SyntaxError on line 4", message)
        self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()