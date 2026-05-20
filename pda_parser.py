"""Text parser for pushdown automata."""

from __future__ import annotations

import re
from typing import Optional

from pda import PDA


EPSILON_WORDS = {"", "epsilon", "eps", "e", "lambda", "empty", "\u03b5"}
EMPTY_SET_WORDS = {"empty", "empty_stack", "phi", "\u03a6", "{}"}


def parse_pda(text: str) -> PDA:
    normalized = _normalize(text)
    lines = _clean_lines(normalized)
    if _looks_like_block_format(lines):
        return _parse_block_format(lines)

    header = _find_header(lines)
    states, inputs, stack_symbols, initial_state, initial_stack, final_states = _parse_header(header)
    pda = PDA(
        states=states,
        input_symbols=inputs,
        stack_symbols=stack_symbols,
        initial_state=initial_state,
        initial_stack_symbol=initial_stack,
        final_states=final_states,
    )

    for line in lines:
        if not line.startswith("delta"):
            continue
        state, input_symbol, stack_top, actions = _parse_transition_line(line, pda.stack_symbols)
        for next_state, push_symbols in actions:
            pda.add_transition(state, input_symbol, stack_top, next_state, push_symbols)

    return pda


def _normalize(text: str) -> str:
    replacements = {
        "\uff1d": "=",
        "\uff08": "(",
        "\uff09": ")",
        "\uff0c": ",",
        "\u03b4": "delta",
        "\u03a6": "empty",
        "\u2205": "empty",
        "\u03b5": "epsilon",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def _looks_like_block_format(lines: list[str]) -> bool:
    return any(line.lower().startswith("states:") for line in lines)


def _parse_block_format(lines: list[str]) -> PDA:
    fields: dict[str, str] = {}
    transition_lines: list[str] = []
    in_transitions = False

    for line in lines:
        lower_line = line.lower()
        if lower_line == "transitions:":
            in_transitions = True
            continue
        if in_transitions:
            transition_lines.append(line)
            continue
        if ":" not in line:
            raise ValueError(f"Invalid PDA block line: {line!r}")
        key, value = line.split(":", maxsplit=1)
        fields[key.strip().lower()] = value.strip()

    required = {"states", "input_symbols", "stack_symbols", "start_state", "start_stack", "accept"}
    missing = required - set(fields)
    if missing:
        raise ValueError(f"PDA block input is missing fields: {sorted(missing)}")

    states = _parse_space_list(fields["states"])
    input_symbols = _parse_space_list(fields["input_symbols"])
    stack_symbols = _parse_space_list(fields["stack_symbols"])
    accept = fields["accept"].lower()
    final_states = set() if accept in EMPTY_SET_WORDS else _parse_space_list(fields["accept"])
    pda = PDA(
        states=states,
        input_symbols=input_symbols,
        stack_symbols=stack_symbols,
        initial_state=fields["start_state"],
        initial_stack_symbol=fields["start_stack"],
        final_states=final_states,
    )

    for line in transition_lines:
        state, input_symbol, stack_top, next_state, push_symbols = _parse_block_transition(
            line,
            pda.stack_symbols,
        )
        pda.add_transition(state, input_symbol, stack_top, next_state, push_symbols)

    return pda


def _parse_block_transition(
    line: str,
    stack_symbols: set[str],
) -> tuple[str, Optional[str], str, str, tuple[str, ...]]:
    if "->" not in line:
        raise ValueError(f"Invalid PDA transition line: {line!r}")
    left_text, right_text = [part.strip() for part in line.split("->", maxsplit=1)]
    left_parts = [part.strip() for part in left_text.split(",")]
    right_parts = [part.strip() for part in right_text.split(",", maxsplit=1)]
    if len(left_parts) != 3 or len(right_parts) != 2:
        raise ValueError(f"Invalid PDA transition line: {line!r}")
    state, input_text, stack_top = left_parts
    next_state, push_text = right_parts
    return (
        state,
        _parse_input_symbol(input_text),
        stack_top,
        next_state,
        _tokenize_stack_string(push_text, stack_symbols),
    )


def _parse_space_list(text: str) -> set[str]:
    return {part for part in re.split(r"[\s,]+", text.strip()) if part}


def _clean_lines(text: str) -> list[str]:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.split("#", maxsplit=1)[0].strip()
        if line:
            lines.append(line)
    return lines


def _find_header(lines: list[str]) -> str:
    for line in lines:
        if "=" in line and "{" in line and "delta" in line:
            return line
    raise ValueError("PDA input must contain a machine header.")


def _parse_header(header: str) -> tuple[set[str], set[str], set[str], str, str, set[str]]:
    _, right = header.split("=", maxsplit=1)
    body = right.strip()
    if not (body.startswith("(") and body.endswith(")")):
        raise ValueError(f"Invalid PDA header: {header!r}")
    parts = _split_top_level_commas(body[1:-1])
    if len(parts) != 7:
        raise ValueError(f"PDA header must contain 7 fields: {header!r}")

    states = _parse_set(parts[0])
    inputs = _parse_set(parts[1])
    stack_symbols = _parse_set(parts[2])
    initial_state = parts[4].strip()
    initial_stack = parts[5].strip()
    final_states = _parse_final_states(parts[6])
    return states, inputs, stack_symbols, initial_state, initial_stack, final_states


def _parse_transition_line(
    line: str,
    stack_symbols: set[str],
) -> tuple[str, Optional[str], str, list[tuple[str, tuple[str, ...]]]]:
    pattern = re.compile(r"delta\(([^,]+),([^,]+),([^)]+)\)\s*=\s*\{(.+)\}\s*$")
    match = pattern.match(line)
    if not match:
        raise ValueError(f"Invalid PDA transition line: {line!r}")

    state = match.group(1).strip()
    input_symbol = _parse_input_symbol(match.group(2).strip())
    stack_top = match.group(3).strip()
    actions_text = match.group(4).strip()
    actions = []
    for action_text in re.findall(r"\(([^()]*)\)", actions_text):
        next_state, push_text = [part.strip() for part in action_text.split(",", maxsplit=1)]
        actions.append((next_state, _tokenize_stack_string(push_text, stack_symbols)))
    if not actions:
        raise ValueError(f"Transition line has no target action: {line!r}")
    return state, input_symbol, stack_top, actions


def _parse_input_symbol(text: str) -> Optional[str]:
    return None if text.lower() in EPSILON_WORDS else text


def _tokenize_stack_string(text: str, stack_symbols: set[str]) -> tuple[str, ...]:
    if text.lower() in EPSILON_WORDS:
        return ()
    if re.search(r"\s", text):
        return tuple(part for part in re.split(r"\s+", text) if part)

    symbols = sorted(stack_symbols, key=len, reverse=True)
    tokens: list[str] = []
    index = 0
    while index < len(text):
        matched = None
        for symbol in symbols:
            if text.startswith(symbol, index):
                matched = symbol
                break
        if matched is None:
            raise ValueError(f"Cannot split stack string {text!r} using stack symbols {stack_symbols!r}")
        tokens.append(matched)
        index += len(matched)
    return tuple(tokens)


def _parse_set(text: str) -> set[str]:
    value = text.strip()
    if not (value.startswith("{") and value.endswith("}")):
        raise ValueError(f"Expected a set, got {text!r}")
    body = value[1:-1].strip()
    if not body:
        return set()
    return {item.strip() for item in body.split(",") if item.strip()}


def _parse_final_states(text: str) -> set[str]:
    value = text.strip()
    if value.lower() in EMPTY_SET_WORDS:
        return set()
    return _parse_set(value)


def _split_top_level_commas(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    brace_depth = 0
    for index, char in enumerate(text):
        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
        elif char == "," and brace_depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts
