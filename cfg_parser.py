"""Text parser for context-free grammars."""

from __future__ import annotations

import re
from typing import Optional

from cfg import CFG, ProductionRhs


ARROW_RE = re.compile(r"\s*(?:->|=>|:|=|-->|\u2192)\s*")
EPSILON_WORDS = {"", "epsilon", "eps", "e", "lambda", "empty", "\u03b5"}


def parse_cfg(text: str, start_symbol: Optional[str] = None) -> CFG:
    """Parse productions such as ``S -> a | bA`` into a :class:`CFG`.

    The parser accepts compact textbook notation for single-character symbols
    and whitespace-separated notation for multi-character symbols.
    """

    entries: list[tuple[str, str]] = []
    variables: set[str] = set()

    for line in _clean_lines(text):
        parts = ARROW_RE.split(line, maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Invalid production line: {line!r}")
        left, right = parts[0].strip(), parts[1].strip()
        if not left:
            raise ValueError(f"Missing production left side: {line!r}")
        variables.add(left)
        entries.append((left, right))

    if not entries:
        raise ValueError("CFG input does not contain any production.")

    start = start_symbol or entries[0][0]
    grammar = CFG(start_symbol=start, variables=set(variables))

    for left, right_text in entries:
        alternatives = [part.strip() for part in right_text.split("|")]
        for alternative in alternatives:
            grammar.add_production(left, tokenize_rhs(alternative, variables))

    grammar.terminals = _infer_terminals(grammar)
    return grammar


def tokenize_rhs(text: str, variables: set[str]) -> ProductionRhs:
    text = text.strip()
    if text.lower() in EPSILON_WORDS:
        return ()

    if re.search(r"\s", text):
        parts = [part for part in re.split(r"\s+", text) if part]
        if len(parts) == 1 and parts[0].lower() in EPSILON_WORDS:
            return ()
        return tuple(parts)

    tokens: list[str] = []
    index = 0
    variables_by_length = sorted(variables, key=len, reverse=True)
    while index < len(text):
        if text[index] == "[":
            end = text.find("]", index)
            if end == -1:
                raise ValueError(f"Unclosed bracketed symbol in RHS: {text!r}")
            tokens.append(text[index : end + 1])
            index = end + 1
            continue

        matched_variable = None
        for variable in variables_by_length:
            if text.startswith(variable, index):
                matched_variable = variable
                break
        if matched_variable is not None:
            tokens.append(matched_variable)
            index += len(matched_variable)
        else:
            tokens.append(text[index])
            index += 1

    return tuple(tokens)


def _clean_lines(text: str) -> list[str]:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.split("#", maxsplit=1)[0].strip()
        if line:
            lines.append(line)
    return lines


def _infer_terminals(grammar: CFG) -> set[str]:
    terminals = set()
    for rights in grammar.productions.values():
        for rhs in rights:
            terminals.update(symbol for symbol in rhs if symbol not in grammar.variables)
    return terminals
