"""Serialize CFG objects to JSON and LaTeX."""

from __future__ import annotations

import json

from cfg import CFG, EPSILON_TEXT, format_rhs


def to_json(grammar: CFG) -> str:
    """Return a JSON document describing the grammar."""

    productions = []
    for left, rights in grammar.ordered_productions():
        for rhs in rights:
            productions.append(
                {
                    "left": left,
                    "right": [format_rhs(rhs) if rhs else EPSILON_TEXT],
                    "symbols": list(rhs),
                }
            )
    payload = {
        "start_symbol": grammar.start_symbol,
        "variables": grammar.ordered_variables(),
        "terminals": grammar.ordered_terminals(),
        "productions": productions,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def to_latex(grammar: CFG) -> str:
    """Return a LaTeX ``align*`` block listing productions."""

    lines = []
    for left, rights in grammar.ordered_productions():
        rhs_parts = " \\mid ".join(_latex_rhs(rhs) for rhs in rights)
        lines.append(f"{_latex_symbol(left)} &\\rightarrow {rhs_parts} \\\\")
    body = "\n".join(lines)
    return f"\\begin{{align*}}\n{body}\n\\end{{align*}}"


def _latex_symbol(symbol: str) -> str:
    if len(symbol) == 1 and symbol.isalpha():
        return symbol
    escaped = symbol.replace("_", "\\_").replace("[", "{[}").replace("]", "{]}")
    return f"\\text{{{escaped}}}"


def _latex_rhs(rhs: tuple[str, ...]) -> str:
    if not rhs:
        return "\\varepsilon"
    parts = []
    for symbol in rhs:
        if len(symbol) == 1 and symbol.isalpha() and symbol.islower():
            parts.append(symbol)
        else:
            parts.append(_latex_symbol(symbol))
    return " ".join(parts)
