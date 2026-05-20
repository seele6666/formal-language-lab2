import unittest
from collections import deque

from cfg_simplifier import (
    find_generating_variables,
    find_reachable_variables,
    has_epsilon_productions,
    has_unit_productions,
    simplify_cfg,
)
from pda_parser import parse_pda
from pda_to_cfg import pda_to_cfg, variable_name


SPECIFIED_PDA = """
M = ({q0,q1}, {a,b}, {B,z0}, delta, q0, z0, empty)
delta(q0,b,z0) = {(q0,Bz0)}
delta(q0,b,B) = {(q0,BB)}
delta(q0,a,B) = {(q1,epsilon)}
delta(q1,a,B) = {(q1,epsilon)}
delta(q1,epsilon,B) = {(q1,epsilon)}
delta(q1,epsilon,z0) = {(q1,epsilon)}
"""


class PDAToCFGTests(unittest.TestCase):
    def test_constructs_standard_variables_and_start_productions(self):
        pda = parse_pda(SPECIFIED_PDA)
        grammar = pda_to_cfg(pda)

        self.assertIn(variable_name("q0", "z0", "q1"), grammar.variables)
        self.assertEqual(
            grammar.productions["S"],
            {
                (variable_name("q0", "z0", "q0"),),
                (variable_name("q0", "z0", "q1"),),
            },
        )
        self.assertIn(
            (
                "b",
                variable_name("q0", "B", "q0"),
                variable_name("q0", "z0", "q1"),
            ),
            grammar.productions[variable_name("q0", "z0", "q1")],
        )

    def test_simplified_cfg_matches_specified_pda_examples(self):
        pda = parse_pda(SPECIFIED_PDA)
        simplified = simplify_cfg(pda_to_cfg(pda))
        generated = _generate_terminal_strings(simplified, max_len=6, max_steps=16)

        self.assertFalse(has_epsilon_productions(simplified))
        self.assertFalse(has_unit_productions(simplified))
        self.assertEqual(find_generating_variables(simplified), simplified.variables)
        self.assertEqual(find_reachable_variables(simplified), simplified.variables)
        self.assertIn("ba", generated)
        self.assertIn("bba", generated)
        self.assertIn("bbaa", generated)
        self.assertIn("bbbaaa", generated)
        self.assertNotIn("", generated)
        self.assertNotIn("b", generated)
        self.assertNotIn("a", generated)
        self.assertNotIn("baa", generated)

    def test_push_lengths_zero_one_two_and_more_are_supported(self):
        pda = parse_pda(
            """
            M = ({p,q}, {a}, {A,B,C,D}, delta, p, A, empty)
            delta(p,a,A) = {(q,epsilon)}
            delta(p,a,B) = {(q,C)}
            delta(p,a,C) = {(q,CD)}
            delta(p,a,D) = {(q,BCD)}
            """
        )

        grammar = pda_to_cfg(pda)

        self.assertIn(("a",), grammar.productions[variable_name("p", "A", "q")])
        self.assertIn(("a", variable_name("q", "C", "q")), grammar.productions[variable_name("p", "B", "q")])
        self.assertTrue(
            any(len(rhs) == 3 and rhs[0] == "a" for rhs in grammar.productions[variable_name("p", "C", "q")])
        )
        self.assertTrue(
            any(len(rhs) == 4 and rhs[0] == "a" for rhs in grammar.productions[variable_name("p", "D", "q")])
        )


def _generate_terminal_strings(grammar, max_len: int, max_steps: int) -> set[str]:
    results: set[str] = set()
    start = (grammar.start_symbol,)
    agenda = deque([(start, 0)])
    seen = {start}

    while agenda:
        form, steps = agenda.popleft()
        terminal_prefix_len = sum(1 for symbol in form if symbol not in grammar.variables)
        if terminal_prefix_len > max_len or steps > max_steps:
            continue
        if all(symbol not in grammar.variables for symbol in form):
            word = "".join(form)
            if len(word) <= max_len:
                results.add(word)
            continue

        first_variable_index = next(
            index for index, symbol in enumerate(form) if symbol in grammar.variables
        )
        variable = form[first_variable_index]
        for rhs in grammar.productions.get(variable, set()):
            next_form = (
                form[:first_variable_index]
                + rhs
                + form[first_variable_index + 1 :]
            )
            if len(next_form) <= max_len + 4 and next_form not in seen:
                seen.add(next_form)
                agenda.append((next_form, steps + 1))

    return results


if __name__ == "__main__":
    unittest.main()
