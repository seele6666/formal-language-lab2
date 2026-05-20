"""Core data structures for pushdown automata."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional


State = str
InputSymbol = str
StackSymbol = str
TransitionKey = tuple[State, Optional[InputSymbol], StackSymbol]


@dataclass(frozen=True)
class PDAAction:
    """One PDA transition target.

    ``push`` stores the replacement stack string from top to bottom. An empty
    tuple means epsilon, so the transition only pops the stack top.
    """

    next_state: State
    push: tuple[StackSymbol, ...]


@dataclass
class PDA:
    states: set[State]
    input_symbols: set[InputSymbol]
    stack_symbols: set[StackSymbol]
    initial_state: State
    initial_stack_symbol: StackSymbol
    final_states: set[State] = field(default_factory=set)
    transitions: dict[TransitionKey, set[PDAAction]] = field(default_factory=dict)

    def add_transition(
        self,
        state: State,
        input_symbol: Optional[InputSymbol],
        stack_top: StackSymbol,
        next_state: State,
        push: Iterable[StackSymbol],
    ) -> None:
        self.states.update({state, next_state})
        if input_symbol is not None:
            self.input_symbols.add(input_symbol)
        self.stack_symbols.add(stack_top)
        push_tuple = tuple(push)
        self.stack_symbols.update(push_tuple)
        key = (state, input_symbol, stack_top)
        self.transitions.setdefault(key, set()).add(PDAAction(next_state, push_tuple))

    @property
    def accepts_by_empty_stack(self) -> bool:
        return not self.final_states

    def ordered_states(self) -> list[State]:
        return sorted(self.states)

    def ordered_input_symbols(self) -> list[InputSymbol]:
        return sorted(self.input_symbols)

    def ordered_stack_symbols(self) -> list[StackSymbol]:
        return sorted(self.stack_symbols)
