"""Construction of an equivalent CFG from an empty-stack PDA."""

from __future__ import annotations

from itertools import product
from typing import Optional

from cfg import CFG
from pda import PDA, PDAAction
from pda_convert import convert_final_to_empty_stack


START_SYMBOL = "S"


def pda_to_cfg(pda: PDA, *, auto_convert: bool = True) -> CFG:
    """Convert an empty-stack PDA to an equivalent CFG.

    The variable [p,A,q] generates exactly the strings that move the PDA from
    state p with A on top of the stack to state q after A has been removed.
    Push strings of length 0, 1, 2, and larger finite lengths are handled by
    enumerating the intermediate states between the pushed stack symbols.

    When ``auto_convert`` is true, final-state PDAs are converted to empty-stack
    form before construction.
    """

    if not pda.accepts_by_empty_stack:
        if auto_convert:
            pda = convert_final_to_empty_stack(pda)
        else:
            raise NotImplementedError("Only empty-stack PDA acceptance is supported.")

    states = pda.ordered_states()
    stack_symbols = pda.ordered_stack_symbols()
    variables = {START_SYMBOL}
    variables.update(
        variable_name(start, stack_top, end)
        for start in states
        for stack_top in stack_symbols
        for end in states
    )
    grammar = CFG(
        start_symbol=START_SYMBOL,
        variables=variables,
        terminals=set(pda.input_symbols),
    )

    for end_state in states:
        grammar.add_production(
            START_SYMBOL,
            (variable_name(pda.initial_state, pda.initial_stack_symbol, end_state),),
        )

    for (state, input_symbol, stack_top), actions in pda.transitions.items():
        for action in actions:
            _add_transition_productions(
                grammar,
                states,
                state,
                input_symbol,
                stack_top,
                action,
            )

    grammar.terminals = set(pda.input_symbols)
    return grammar


def variable_name(start_state: str, stack_symbol: str, end_state: str) -> str:
    return f"[{start_state},{stack_symbol},{end_state}]"


def _add_transition_productions(
    grammar: CFG,
    states: list[str],
    state: str,
    input_symbol: Optional[str],
    stack_top: str,
    action: PDAAction,
) -> None:
    terminal_prefix = () if input_symbol is None else (input_symbol,)

    if not action.push:
        grammar.add_production(
            variable_name(state, stack_top, action.next_state),
            terminal_prefix,
        )
        return

    push_length = len(action.push)
    for end_state in states:
        for middle_states in product(states, repeat=push_length - 1):
            chain_states = (action.next_state, *middle_states, end_state)
            generated_variables = tuple(
                variable_name(chain_states[index], stack_symbol, chain_states[index + 1])
                for index, stack_symbol in enumerate(action.push)
            )
            grammar.add_production(
                variable_name(state, stack_top, end_state),
                (*terminal_prefix, *generated_variables),
            )
