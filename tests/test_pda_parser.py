import unittest

from pda import PDAAction
from pda_parser import parse_pda


SPECIFIED_PDA = """
M = ({q0,q1}, {a,b}, {B,z0}, delta, q0, z0, empty)
delta(q0,b,z0) = {(q0,Bz0)}
delta(q0,b,B) = {(q0,BB)}
delta(q0,a,B) = {(q1,epsilon)}
delta(q1,a,B) = {(q1,epsilon)}
delta(q1,epsilon,B) = {(q1,epsilon)}
delta(q1,epsilon,z0) = {(q1,epsilon)}
"""

BLOCK_PDA = """
states: q0 q1
input_symbols: a b
stack_symbols: B z0
start_state: q0
start_stack: z0
accept: empty_stack
transitions:
q0,b,z0 -> q0,B z0
q0,b,B -> q0,B B
q0,a,B -> q1,eps
q1,a,B -> q1,eps
q1,eps,B -> q1,eps
q1,eps,z0 -> q1,eps
"""


class PDAParserTests(unittest.TestCase):
    def test_parse_specified_pda(self):
        pda = parse_pda(SPECIFIED_PDA)

        self.assertEqual(pda.states, {"q0", "q1"})
        self.assertEqual(pda.input_symbols, {"a", "b"})
        self.assertEqual(pda.stack_symbols, {"B", "z0"})
        self.assertEqual(pda.initial_state, "q0")
        self.assertEqual(pda.initial_stack_symbol, "z0")
        self.assertTrue(pda.accepts_by_empty_stack)
        self.assertEqual(
            pda.transitions[("q0", "b", "z0")],
            {PDAAction("q0", ("B", "z0"))},
        )
        self.assertEqual(
            pda.transitions[("q1", None, "B")],
            {PDAAction("q1", ())},
        )
        self.assertEqual(sum(len(actions) for actions in pda.transitions.values()), 6)

    def test_parse_block_pda(self):
        pda = parse_pda(BLOCK_PDA)

        self.assertEqual(pda.states, {"q0", "q1"})
        self.assertEqual(pda.input_symbols, {"a", "b"})
        self.assertEqual(pda.stack_symbols, {"B", "z0"})
        self.assertTrue(pda.accepts_by_empty_stack)
        self.assertEqual(sum(len(actions) for actions in pda.transitions.values()), 6)


if __name__ == "__main__":
    unittest.main()
