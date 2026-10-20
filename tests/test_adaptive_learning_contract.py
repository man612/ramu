#!/usr/bin/env python3
"""Regression contract untuk fallback format belajar dan evidence kemajuan."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMON_MARKER = "Saat format visual atau interaktif benar-benar membantu"

INSTRUCTIONS = [
    "starter/PROJECT-INSTRUCTIONS.md",
    "packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-01/PROJECT-INSTRUCTIONS.md",
    "packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/PROJECT-INSTRUCTIONS.md",
    "packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-03/PROJECT-INSTRUCTIONS.md",
]


def require(path: str, expected: str) -> None:
    content = (ROOT / path).read_text(encoding="utf-8")
    if expected not in content:
        raise AssertionError(f"{path} kehilangan kontrak {expected!r}")


def main() -> int:
    for path in INSTRUCTIONS:
        require(path, COMMON_MARKER)
        require(path, "Jangan memaksa format interaktif")
        require(path, "jika tidak, jelaskan lewat teks")
    require("protocols/belajar.md", "Latihan interaktif atau flashcard")
    require("protocols/belajar.md", "fitur tersedia pada percakapan")
    require("learning/learner-state.template.md", "Bukti (mandiri / setelah bantuan)")
    require("learning/mastery-map.template.md", "Bukti setelah petunjuk")
    print("Adaptive presentation + learner evidence contract — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
