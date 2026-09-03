#!/usr/bin/env python3
"""Jaga urutan lima lapisan utama yang ditampilkan di README."""

from __future__ import annotations

import sys

from ramu_repo import ROOT

README = ROOT / "README.md"
MARKERS = [
    "| **Referensi** |",
    "| **Instruksi** |",
    "| **Zona konteks** |",
    "| **Materi** |",
    "| **Asesmen** |",
]


def main() -> int:
    if not README.is_file():
        print("README layer-order validation — ERROR: README.md tidak ditemukan.")
        return 1

    text = README.read_text(encoding="utf-8")
    positions: list[int] = []
    for marker in MARKERS:
        position = text.find(marker)
        if position < 0:
            print(f"README layer-order validation — ERROR: marker hilang: {marker}")
            return 1
        positions.append(position)

    if positions != sorted(positions):
        print("README layer-order validation — ERROR: urutan lima lapisan README berubah.")
        return 1

    print("README layer-order validation — OK: lima lapisan utama tetap dalam urutan yang diharapkan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
