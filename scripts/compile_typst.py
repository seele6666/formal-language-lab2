"""Compile docs/实验报告.typ to PDF (UTF-8 safe on Windows)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TYP = DOCS / "实验报告.typ"
PDF = DOCS / "实验报告.pdf"


def main() -> None:
    if not TYP.exists():
        raise SystemExit(f"Missing Typst source: {TYP}")
    subprocess.run(
        ["typst", "compile", str(TYP), str(PDF)],
        check=True,
        cwd=ROOT,
    )
    print(f"compiled {PDF}")


if __name__ == "__main__":
    main()
