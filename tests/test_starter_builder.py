#!/usr/bin/env python3
"""Regression test untuk Ramu Starter generator."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/create_starter.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ramu-starter-test-") as tmp:
        out = Path(tmp) / "starter"
        result = run(
            "--course", "Statistika Bisnis",
            "--institution", "Kampus Contoh",
            "--period", "Semester 2",
            "--goal", "Memahami probabilitas",
            "--source", "Syllabus dosen",
            "--rule", "Jangan membuat submission penuh",
            "--output", str(out),
        )
        if result.returncode != 0:
            raise AssertionError(f"Starter generator gagal: {result.stderr}\n{result.stdout}")

        for name in ("PROJECT-INSTRUCTIONS.md", "COURSE-PACK.txt", "START-HERE.md", "starter.json"):
            if not (out / name).is_file():
                raise AssertionError(f"Starter kehilangan artefak {name}")

        metadata = json.loads((out / "starter.json").read_text(encoding="utf-8"))
        if metadata["course"] != "Statistika Bisnis":
            raise AssertionError("Nama course Starter berubah.")
        if metadata["project_name"] != "Semester 2 • Statistika Bisnis":
            raise AssertionError("Project name default tidak memakai period label lengkap.")
        if metadata["public_pack"] is not False or metadata["source_verified"] is not False:
            raise AssertionError("Starter personal tidak boleh mengklaim status public/source-verified.")

        pack = (out / "COURSE-PACK.txt").read_text(encoding="utf-8")
        for marker in ("personal starter", "Memahami probabilitas", "Syllabus dosen", "Jangan membuat submission penuh"):
            if marker not in pack:
                raise AssertionError(f"COURSE-PACK Starter kehilangan marker {marker!r}")

        second = run("--course", "Statistika Bisnis", "--output", str(out))
        if second.returncode == 0:
            raise AssertionError("Generator tidak boleh overwrite Starter tanpa --force.")

        forced = run("--course", "Statistika Bisnis", "--output", str(out), "--force")
        if forced.returncode != 0:
            raise AssertionError(f"--force gagal mengganti file Starter milik generator: {forced.stderr}")

        noninteractive_missing = run("--output", str(Path(tmp) / "missing-course"))
        if noninteractive_missing.returncode == 0:
            raise AssertionError("Mode non-interaktif tanpa --course harus gagal jelas, bukan hang/input diam-diam.")

    print("Ramu Starter generator regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
