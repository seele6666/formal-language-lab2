"""Simplification algorithms for context-free grammars."""

from __future__ import annotations

from itertools import combinations

from cfg import CFG, ProductionRhs


def simplify_cfg(grammar: CFG) -> CFG:
    """Run the complete simplification pipeline required by the experiment."""

    no_epsilon = eliminate_epsilon_productions(grammar)
    no_units = eliminate_unit_productions(no_epsilon)
    generating_only = remove_non_generating_symbols(no_units)
    return remove_unreachable_symbols(generating_only)


def eliminate_epsilon_productions(grammar: CFG, keep_start_epsilon: bool = False) -> CFG:
    """Remove epsilon productions by expanding nullable variables.

    ``keep_start_epsilon`` is available for textbook variants that preserve the
    empty word when the start symbol is nullable. The experiment asks for output
    without epsilon productions, so the simplification pipeline keeps it false.
    """

    nullable = find_nullable_variables(grammar)
    result = CFG(start_symbol=grammar.start_symbol, variables=set(grammar.variables))

    for left, rights in grammar.productions.items():
        for rhs in rights:
            if not rhs:
                continue
            for expanded_rhs in _expand_nullable_rhs(rhs, nullable):
                if expanded_rhs or (keep_start_epsilon and left == grammar.start_symbol):
                    result.add_production(left, expanded_rhs)

    result.terminals = _infer_terminals(result)
    return result


def find_nullable_variables(grammar: CFG) -> set[str]:
    nullable: set[str] = set()
    changed = True
    while changed:
        changed = False
        for left, rights in grammar.productions.items():
            if left in nullable:
                continue
            for rhs in rights:
                if not rhs or all(symbol in nullable for symbol in rhs):
                    nullable.add(left)
                    changed = True
                    break
    return nullable


def eliminate_unit_productions(grammar: CFG) -> CFG:
    """Remove productions of the form A -> B where both sides are variables."""

    unit_closure = {
        variable: _unit_reachable_variables(grammar, variable)
        for variable in grammar.variables
    }
    result = CFG(start_symbol=grammar.start_symbol, variables=set(grammar.variables))

    for left, reachable in unit_closure.items():
        for variable in reachable:
            for rhs in grammar.productions.get(variable, set()):
                if not _is_unit_production(grammar, rhs):
                    result.add_production(left, rhs)

    result.terminals = _infer_terminals(result)
    return result


def remove_non_generating_symbols(grammar: CFG) -> CFG:
    """Remove variables that cannot derive a terminal string."""

    generating = find_generating_variables(grammar)
    result = CFG(start_symbol=grammar.start_symbol, variables=generating)

    for left, rights in grammar.productions.items():
        if left not in generating:
            continue
        for rhs in rights:
            if all(symbol not in grammar.variables or symbol in generating for symbol in rhs):
                result.add_production(left, rhs)

    result.terminals = _infer_terminals(result)
    return result


def find_generating_variables(grammar: CFG) -> set[str]:
    generating: set[str] = set()
    changed = True
    while changed:
        changed = False
        for left, rights in grammar.productions.items():
            if left in generating:
                continue
            for rhs in rights:
                if all(symbol not in grammar.variables or symbol in generating for symbol in rhs):
                    generating.add(left)
                    changed = True
                    break
    return generating


def remove_unreachable_symbols(grammar: CFG) -> CFG:
    """Remove variables that are not reachable from the start symbol."""

    reachable = find_reachable_variables(grammar)
    result = CFG(start_symbol=grammar.start_symbol, variables=reachable)

    for left, rights in grammar.productions.items():
        if left not in reachable:
            continue
        for rhs in rights:
            if all(symbol not in grammar.variables or symbol in reachable for symbol in rhs):
                result.add_production(left, rhs)

    result.terminals = _infer_terminals(result)
    return result


def find_reachable_variables(grammar: CFG) -> set[str]:
    reachable = {grammar.start_symbol}
    changed = True
    while changed:
        changed = False
        for left in list(reachable):
            for rhs in grammar.productions.get(left, set()):
                for symbol in rhs:
                    if symbol in grammar.variables and symbol not in reachable:
                        reachable.add(symbol)
                        changed = True
    return reachable


def has_epsilon_productions(grammar: CFG) -> bool:
    return any(not rhs for rights in grammar.productions.values() for rhs in rights)


def has_unit_productions(grammar: CFG) -> bool:
    return any(
        _is_unit_production(grammar, rhs)
        for rights in grammar.productions.values()
        for rhs in rights
    )


def _expand_nullable_rhs(rhs: ProductionRhs, nullable: set[str]) -> set[ProductionRhs]:
    nullable_positions = [
        index for index, symbol in enumerate(rhs) if symbol in nullable
    ]
    expanded: set[ProductionRhs] = set()

    for count in range(len(nullable_positions) + 1):
        for omitted in combinations(nullable_positions, count):
            omitted_set = set(omitted)
            expanded.add(
                tuple(symbol for index, symbol in enumerate(rhs) if index not in omitted_set)
            )

    return expanded


def _unit_reachable_variables(grammar: CFG, start: str) -> set[str]:
    reachable = {start}
    agenda = [start]
    while agenda:
        current = agenda.pop()
        for rhs in grammar.productions.get(current, set()):
            if _is_unit_production(grammar, rhs) and rhs[0] not in reachable:
                reachable.add(rhs[0])
                agenda.append(rhs[0])
    return reachable


def _is_unit_production(grammar: CFG, rhs: ProductionRhs) -> bool:
    return len(rhs) == 1 and rhs[0] in grammar.variables


def _infer_terminals(grammar: CFG) -> set[str]:
    terminals = set()
    for rights in grammar.productions.values():
        for rhs in rights:
            terminals.update(symbol for symbol in rhs if symbol not in grammar.variables)
    return terminals
