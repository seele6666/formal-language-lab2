import json
import unittest

from cfg_parser import parse_cfg
from cfg_format import to_json, to_latex


class CFGFormatTests(unittest.TestCase):
    def test_json_format_output(self):
        grammar = parse_cfg("S -> a | epsilon")
        payload = json.loads(to_json(grammar))

        self.assertEqual(payload["start_symbol"], "S")
        self.assertEqual(payload["variables"], ["S"])
        self.assertIn({"left": "S", "right": ["a"], "symbols": ["a"]}, payload["productions"])

    def test_latex_format_output(self):
        grammar = parse_cfg("S -> a | epsilon")
        latex = to_latex(grammar)

        self.assertIn("\\begin{align*}", latex)
        self.assertIn("S &\\rightarrow", latex)
        self.assertIn("\\varepsilon", latex)


if __name__ == "__main__":
    unittest.main()
