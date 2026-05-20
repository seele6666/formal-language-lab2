import unittest

from cfg_parser import parse_cfg
from cfg_simplifier import (
    find_generating_variables,
    find_nullable_variables,
    find_reachable_variables,
    has_epsilon_productions,
    has_unit_productions,
    simplify_cfg,
)


SPECIFIED_CFG = """
S -> a | bA | B | ccD
A -> abB | epsilon
B -> aA
C -> ddC
D -> ddd
"""


class CFGSimplifierTests(unittest.TestCase):
    def test_nullable_variables(self):
        grammar = parse_cfg(SPECIFIED_CFG)

        self.assertEqual(find_nullable_variables(grammar), {"A"})

    def test_simplify_specified_cfg(self):
        grammar = parse_cfg(SPECIFIED_CFG)
        simplified = simplify_cfg(grammar)

        self.assertFalse(has_epsilon_productions(simplified))
        self.assertFalse(has_unit_productions(simplified))
        self.assertEqual(simplified.variables, {"S", "A", "B", "D"})
        self.assertEqual(find_generating_variables(simplified), simplified.variables)
        self.assertEqual(find_reachable_variables(simplified), simplified.variables)
        self.assertEqual(
            simplified.productions,
            {
                "S": {("a",), ("a", "A"), ("b",), ("b", "A"), ("c", "c", "D")},
                "A": {("a", "b", "B")},
                "B": {("a",), ("a", "A")},
                "D": {("d", "d", "d")},
            },
        )

    def test_unit_cycle_does_not_loop(self):
        grammar = parse_cfg(
            """
            S -> A | x
            A -> B
            B -> A | b
            """
        )

        simplified = simplify_cfg(grammar)

        self.assertFalse(has_unit_productions(simplified))
        self.assertIn(("b",), simplified.productions["S"])
        self.assertIn(("x",), simplified.productions["S"])


if __name__ == "__main__":
    unittest.main()
