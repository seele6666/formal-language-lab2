import unittest

from cfg_parser import parse_cfg
from cfg_simplifier import (
    find_generating_variables,
    find_nullable_variables,
    find_reachable_variables,
    has_epsilon_productions,
    has_unit_productions,
    simplify_cfg,
    simplify_cfg_verbose,
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

    def test_keep_start_epsilon_preserves_empty_word(self):
        grammar = parse_cfg(
            """
            S -> A
            A -> epsilon
            """
        )

        simplified = simplify_cfg(grammar, keep_start_epsilon=True)

        self.assertIn((), simplified.productions["S"])
        self.assertNotIn("A", simplified.variables)

    def test_pure_epsilon_grammar_becomes_empty_without_keep(self):
        grammar = parse_cfg(
            """
            S -> epsilon
            """
        )

        simplified = simplify_cfg(grammar)

        self.assertEqual(simplified.productions.get("S", set()), set())

    def test_unreachable_variable_removed(self):
        grammar = parse_cfg(
            """
            S -> a
            T -> b U
            U -> c
            """
        )

        simplified = simplify_cfg(grammar)

        self.assertEqual(simplified.variables, {"S"})
        self.assertEqual(simplified.productions["S"], {("a",)})

    def test_verbose_pipeline_has_five_steps(self):
        grammar = parse_cfg(SPECIFIED_CFG)
        _, steps = simplify_cfg_verbose(grammar)

        self.assertEqual(len(steps), 5)
        self.assertEqual(steps[0][0], "input")
        self.assertEqual(steps[-1][0], "(4) remove unreachable symbols")


if __name__ == "__main__":
    unittest.main()
