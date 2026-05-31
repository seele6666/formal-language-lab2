import unittest

from pda import PDAAction
from pda_convert import convert_final_to_empty_stack
from pda_parser import parse_pda
from pda_to_cfg import pda_to_cfg


FINAL_STATE_PDA = """
M = ({q0,q1}, {a}, {A,z0}, delta, q0, z0, {q1})
delta(q0,a,A) = {(q1,epsilon)}
delta(q0,a,z0) = {(q0,A)}
"""


class PDAConvertTests(unittest.TestCase):
    def test_convert_final_state_pda_adds_epsilon_pops(self):
        pda = parse_pda(FINAL_STATE_PDA)
        converted = convert_final_to_empty_stack(pda)

        self.assertTrue(converted.accepts_by_empty_stack)
        self.assertIn(("q1", None, "A"), converted.transitions)
        self.assertIn(("q1", None, "z0"), converted.transitions)
        self.assertEqual(
            converted.transitions[("q1", None, "A")],
            {PDAAction("q1", ())},
        )

    def test_auto_convert_allows_final_state_pda_to_cfg(self):
        pda = parse_pda(FINAL_STATE_PDA)
        grammar = pda_to_cfg(pda)

        self.assertIn("a", grammar.terminals)
        self.assertTrue(grammar.productions["S"])

    def test_no_auto_convert_raises_for_final_state_pda(self):
        pda = parse_pda(FINAL_STATE_PDA)
        with self.assertRaises(NotImplementedError):
            pda_to_cfg(pda, auto_convert=False)


if __name__ == "__main__":
    unittest.main()
