"""Core data structures for context-free grammars.

The algorithms in this project represent an epsilon production as an empty
tuple. For example, A -> epsilon is stored as ("A", ()).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


EPSILON_TEXT = "epsilon"

Symbol = str
ProductionRhs = tuple[Symbol, ...]


@dataclass
class CFG:
    """A small, explicit representation of a context-free grammar."""

    start_symbol: Symbol
    variables: set[Symbol] = field(default_factory=set)
    terminals: set[Symbol] = field(default_factory=set)
    productions: dict[Symbol, set[ProductionRhs]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.variables.add(self.start_symbol)
        for left in list(self.productions):
            self.variables.add(left)
        self._refresh_terminals_from_productions()

    def copy(self) -> "CFG":
        return CFG(
            start_symbol=self.start_symbol,
            variables=set(self.variables),
            terminals=set(self.terminals),
            productions={left: set(rights) for left, rights in self.productions.items()},
        )

    def add_production(self, left: Symbol, right: Iterable[Symbol]) -> None:
        rhs = tuple(right)
        self.variables.add(left)
        self.productions.setdefault(left, set()).add(rhs)
        for symbol in rhs:
            if symbol not in self.variables:
                self.terminals.add(symbol)

    def without_empty_left_sides(self) -> "CFG":
        """Return a copy whose production map contains every variable key."""

        grammar = self.copy()
        for variable in grammar.variables:
            grammar.productions.setdefault(variable, set())
        return grammar

    def ordered_variables(self) -> list[Symbol]:
        return sorted(self.variables, key=_symbol_sort_key)

    def ordered_terminals(self) -> list[Symbol]:
        return sorted(self.terminals, key=_symbol_sort_key)

    def ordered_productions(self) -> list[tuple[Symbol, list[ProductionRhs]]]:
        result: list[tuple[Symbol, list[ProductionRhs]]] = []
        for left in self.ordered_variables():
            rights = sorted(self.productions.get(left, set()), key=_rhs_sort_key)
            if rights:
                result.append((left, rights))
        return result

    def to_text(self) -> str:
        lines = []
        for left, rights in self.ordered_productions():
            rhs_text = " | ".join(format_rhs(rhs) for rhs in rights)
            lines.append(f"{left} -> {rhs_text}")
        return "\n".join(lines)

    def _refresh_terminals_from_productions(self) -> None:
        terminals = set(self.terminals)
        for rights in self.productions.values():
            for rhs in rights:
                terminals.update(symbol for symbol in rhs if symbol not in self.variables)
        self.terminals = terminals - self.variables


def format_rhs(rhs: ProductionRhs) -> str:
    if not rhs:
        return EPSILON_TEXT
    if any(len(symbol) > 1 for symbol in rhs):
        return " ".join(rhs)
    return "".join(rhs)


def _symbol_sort_key(symbol: Symbol) -> tuple[int, str]:
    if symbol == "S":
        return (0, symbol)
    return (1, symbol)


def _rhs_sort_key(rhs: ProductionRhs) -> tuple[int, str]:
    if not rhs:
        return (0, "")
    return (1, " ".join(rhs))
