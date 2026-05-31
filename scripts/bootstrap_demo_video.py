"""Ensure docs/demo.mp4 exists for packaging (minimal placeholder if missing)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "demo.mp4"


def _minimal_mp4() -> bytes:
    def box(tag: bytes, payload: bytes) -> bytes:
        body = tag + payload
        return len(body).to_bytes(4, "big") + body

    ftyp = box(b"ftyp", b"isom" + b"\x00" * 4 + b"isom" + b"iso2" + b"mp41")
    free = box(b"free", b"\x00" * 8)
    mdat = box(b"mdat", b"\x00" * 16)
    moov = box(
        b"moov",
        box(
            b"mvhd",
            b"\x00"
            + b"\x00" * 3
            + (0).to_bytes(4, "big")
            + (0).to_bytes(4, "big")
            + (1000).to_bytes(4, "big")
            + (1).to_bytes(4, "big")
            + b"\x00" * 76,
        ),
    )
    return ftyp + free + mdat + moov


def main() -> None:
    if OUT.exists() and OUT.stat().st_size > 1024:
        print(f"keep existing {OUT} ({OUT.stat().st_size} bytes)")
        return
    data = _minimal_mp4()
    OUT.write_bytes(data)
    print(
        f"created placeholder {OUT} ({len(data)} bytes) — "
        "replace with real demo recording before cloud upload"
    )


if __name__ == "__main__":
    main()
