"""Capture terminal screenshots for the experiment report."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "screenshots"

SHOTS = [
    (
        "6-1-cfg-simplify.png",
        ["py", "main.py", "simplify", r"examples\grammar_sample.txt"],
    ),
    (
        "6-2-pda2cfg-simplify.png",
        ["py", "main.py", "pda2cfg", r"examples\pda_sample.txt", "--simplify"],
    ),
    (
        "6-3-unittest.png",
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
    ),
    (
        "6-4-epsilon.png",
        ["py", "main.py", "simplify", r"examples\case_epsilon.txt"],
    ),
    (
        "6-5-unit-cycle.png",
        ["py", "main.py", "simplify", r"examples\case_unit_cycle.txt"],
    ),
    (
        "6-6-unreachable.png",
        ["py", "main.py", "simplify", r"examples\case_unreachable.txt"],
    ),
    (
        "6-7-push3.png",
        ["py", "main.py", "pda2cfg", r"examples\case_push3.txt"],
    ),
]

BG = (12, 12, 12)
FG = (204, 204, 204)
PROMPT = (204, 204, 204)
PATH_COLOR = (111, 207, 151)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\consola.ttf"),
        Path(r"C:\Windows\Fonts\cour.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def run_command(command: list[str]) -> tuple[str, str]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    stdout = completed.stdout.strip("\n")
    stderr = completed.stderr.strip("\n")
    return stdout, stderr


def render_terminal(command: list[str], stdout: str, stderr: str) -> Image.Image:
    font = load_font(16)
    cwd = f"C:\\projects\\formal-language-lab2>"
    prompt_line = f"PS {cwd} {' '.join(command)}"
    lines = [prompt_line]
    if stdout:
        lines.extend(stdout.splitlines())
    if stderr:
        lines.extend(stderr.splitlines())
    lines.append(f"PS {cwd}")

    padding = 16
    line_height = 22
    width = max(font.getlength(line) for line in lines) + padding * 2
    width = max(int(width) + 20, 900)
    height = padding * 2 + line_height * len(lines)

    image = Image.new("RGB", (int(width), int(height)), BG)
    draw = ImageDraw.Draw(image)
    y = padding
    for index, line in enumerate(lines):
        color = FG
        if index == 0 or index == len(lines) - 1:
            draw.text((padding, y), "PS ", font=font, fill=PROMPT)
            draw.text((padding + font.getlength("PS "), y), cwd, font=font, fill=PATH_COLOR)
            rest = line.split(cwd, 1)[1] if cwd in line else ""
            draw.text(
                (padding + font.getlength(f"PS {cwd}"), y),
                rest,
                font=font,
                fill=FG,
            )
        else:
            draw.text((padding, y), line, font=font, fill=FG)
        y += line_height
    return image


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, command in SHOTS:
        stdout, stderr = run_command(command)
        image = render_terminal(command, stdout, stderr)
        image.save(OUT_DIR / filename)
        print(f"saved {OUT_DIR / filename}")


if __name__ == "__main__":
    main()
