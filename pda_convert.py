"""Convert final-state PDAs to equivalent empty-stack PDAs."""

from __future__ import annotations

from pda import PDA


def convert_final_to_empty_stack(pda: PDA) -> PDA:
    """Return an empty-stack PDA that accepts the same language.

    For each former final state, add epsilon transitions that pop every stack
    symbol until the stack becomes empty.
    """

    if pda.accepts_by_empty_stack:
        return pda.copy()

    converted = pda.copy()
    converted.final_states = set()
    for final_state in pda.final_states:
        for stack_symbol in converted.stack_symbols:
            converted.add_transition(final_state, None, stack_symbol, final_state, ())
    return converted
