#!/usr/bin/env python3
"""Jaga urutan lima lapisan utama dan language entry surface README."""

from __future__ import annotations

import sys

from ramu_repo import ROOT

README = ROOT / "README.md"
README_EN = ROOT / "README.en.md"
CONTRIBUTING_EN = ROOT / "CONTRIBUTING.en.md"
MARKERS = [
    "| **Referensi** |",
    "| **Instruksi** |",
    "| **Zona konteks** |",
    "| **Materi** |",
    "| **Asesmen** |",
]


def main() -> int:
    if not README.is_file():
        print("README validation — ERROR: README.md tidak ditemukan.")
        return 1

    text = README.read_text(encoding="utf-8")
    if 'href="README.en.md"' not in text:
        print("README language-surface validation — ERROR: README.md tidak menautkan README.en.md.")
        return 1

    if not README_EN.is_file() or not CONTRIBUTING_EN.is_file():
        print("README language-surface validation — ERROR: English entry surface tidak lengkap.")
        return 1

    english = README_EN.read_text(encoding="utf-8")
    if 'href="README.md"' not in english or "(CONTRIBUTING.en.md)" not in english:
        print("README language-surface validation — ERROR: cross-link English/Indonesia tidak lengkap.")
        return 1

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

    print("README validation — OK: lima lapisan dan language entry surface valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
