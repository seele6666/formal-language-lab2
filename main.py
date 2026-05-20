"""Command line entry point for the CFG and PDA experiment."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from cfg_parser import parse_cfg
from cfg_simplifier import simplify_cfg
from pda_parser import parse_pda
from pda_to_cfg import pda_to_cfg


SPECIFIED_CFG = """\
S -> a | bA | B | ccD
A -> abB | epsilon
B -> aA
C -> ddC
D -> ddd
"""

SPECIFIED_PDA = """\
M = ({q0,q1}, {a,b}, {B,z0}, delta, q0, z0, empty)
delta(q0,b,z0) = {(q0,Bz0)}
delta(q0,b,B) = {(q0,BB)}
delta(q0,a,B) = {(q1,epsilon)}
delta(q1,a,B) = {(q1,epsilon)}
delta(q1,epsilon,B) = {(q1,epsilon)}
delta(q1,epsilon,z0) = {(q1,epsilon)}
"""


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    args.handler(args)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simplify CFGs and convert empty-stack PDAs to CFGs."
    )
    subparsers = parser.add_subparsers(required=True)

    cfg_parser = subparsers.add_parser(
        "simplify-cfg",
        aliases=["simplify"],
        help="simplify a CFG",
    )
    cfg_parser.add_argument("file", nargs="?", default="-", help="CFG input file, or stdin")
    cfg_parser.set_defaults(handler=_handle_simplify_cfg)

    pda_parser = subparsers.add_parser(
        "pda-to-cfg",
        aliases=["pda2cfg"],
        help="convert a PDA to a CFG",
    )
    pda_parser.add_argument("file", nargs="?", default="-", help="PDA input file, or stdin")
    pda_parser.add_argument("--simplify", action="store_true", help="print the simplified CFG")
    pda_parser.add_argument("--show-raw", action="store_true", help="also print the raw CFG")
    pda_parser.set_defaults(handler=_handle_pda_to_cfg)

    demo_parser = subparsers.add_parser("demo", help="run the two specified examples")
    demo_parser.set_defaults(handler=_handle_demo)
    return parser


def _handle_simplify_cfg(args: argparse.Namespace) -> None:
    grammar = parse_cfg(_read_input(args.file))
    simplified = simplify_cfg(grammar)
    print(simplified.to_text())


def _handle_pda_to_cfg(args: argparse.Namespace) -> None:
    pda = parse_pda(_read_input(args.file))
    raw_cfg = pda_to_cfg(pda)
    if args.simplify:
        simplified = simplify_cfg(raw_cfg)
        if args.show_raw:
            print("Raw CFG:")
            print(raw_cfg.to_text())
            print()
        print("Simplified CFG:")
        print(simplified.to_text())
    else:
        print("Raw CFG:")
        print(raw_cfg.to_text())


def _handle_demo(args: argparse.Namespace) -> None:
    print("Specified CFG simplified:")
    print(simplify_cfg(parse_cfg(SPECIFIED_CFG)).to_text())
    print()
    print("Specified PDA converted and simplified:")
    print(simplify_cfg(pda_to_cfg(parse_pda(SPECIFIED_PDA))).to_text())


def _read_input(file_name: str) -> str:
    if file_name == "-":
        return sys.stdin.read()
    return Path(file_name).read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
