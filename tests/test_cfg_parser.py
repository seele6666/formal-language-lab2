import unittest

from cfg_parser import parse_cfg


SPECIFIED_CFG = """
S -> a | bA | B | ccD
A -> abB | epsilon
B -> aA
C -> ddC
D -> ddd
"""


class CFGParserTests(unittest.TestCase):
    def test_parse_specified_cfg(self):
        grammar = parse_cfg(SPECIFIED_CFG)

        self.assertEqual(grammar.start_symbol, "S")
        self.assertEqual(grammar.variables, {"S", "A", "B", "C", "D"})
        self.assertEqual(grammar.terminals, {"a", "b", "c", "d"})
        self.assertEqual(
            grammar.productions["S"],
            {("a",), ("b", "A"), ("B",), ("c", "c", "D")},
        )
        self.assertIn((), grammar.productions["A"])

    def test_parse_whitespace_separated_symbols(self):
        grammar = parse_cfg("[q0,B,q1] -> a [q1,B,q1] | epsilon")

        self.assertEqual(grammar.variables, {"[q0,B,q1]"})
        self.assertEqual(
            grammar.productions["[q0,B,q1]"],
            {("a", "[q1,B,q1]"), ()},
        )


if __name__ == "__main__":
    unittest.main()
