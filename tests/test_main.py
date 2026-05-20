import io
from pathlib import Path
import unittest
from contextlib import redirect_stdout

import main


class MainCliTests(unittest.TestCase):
    def test_demo_prints_both_required_examples(self):
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main.main(["demo"])

        text = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("Specified CFG simplified:", text)
        self.assertIn("Specified PDA converted and simplified:", text)
        self.assertIn("S ->", text)
        self.assertNotIn("epsilon", text)

    def test_required_cli_aliases(self):
        root = Path(__file__).resolve().parents[1]
        cfg_output = io.StringIO()
        pda_output = io.StringIO()

        with redirect_stdout(cfg_output):
            self.assertEqual(main.main(["simplify", str(root / "examples" / "grammar_sample.txt")]), 0)
        with redirect_stdout(pda_output):
            self.assertEqual(
                main.main(["pda2cfg", str(root / "examples" / "pda_sample.txt"), "--simplify"]),
                0,
            )

        self.assertIn("S -> a | aA | b | bA | ccD", cfg_output.getvalue())
        self.assertIn("Simplified CFG:", pda_output.getvalue())


if __name__ == "__main__":
    unittest.main()
