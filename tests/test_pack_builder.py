#!/usr/bin/env python3
"""Regression test untuk scaffold community pack Ramu."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/create_pack.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def replace_value(args: list[str], flag: str, value: str) -> list[str]:
    result = args.copy()
    result[result.index(flag) + 1] = value
    return result


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ramu-pack-builder-") as tmp:
        output_root = Path(tmp) / "packs"
        common = [
            "--institution", "Kampus Contoh",
            "--institution-id", "kampus-contoh",
            "--program", "S1 Manajemen",
            "--program-id", "kampus-contoh.s1-manajemen",
            "--academic-year", "2026/2027",
            "--period-id", "trimester-01",
            "--period-label", "Trimester 1",
            "--pack-id", "id.community.kampus-contoh.management-s1.2026-2027.t1",
            "--course", "MAN101|Pengantar Manajemen|Pengantar Manajemen|3|organisasi dan fungsi manajemen",
            "--course", "ECO101|Pengantar Ekonomi|Pengantar Ekonomi|2|konsep ekonomi untuk keputusan bisnis",
            "--source-url", "https://example.edu/catalog",
            "--source-name", "Katalog Akademik 2026/2027",
            "--source-authority", "Kampus Contoh",
            "--reviewed-at", "2026-09-16",
            "--output-root", str(output_root),
        ]
        result = run(*common)
        if result.returncode != 0:
            raise AssertionError(f"Pack builder gagal: {result.stderr}\n{result.stdout}")

        target = output_root / "kampus-contoh/s1-manajemen/2026-2027/trimester-01"
        for relative in (
            "manifest.json",
            "PROJECT-INSTRUCTIONS.md",
            "source-registry.json",
            "evals/contracts.json",
            "evals/behavior.json",
            "README.md",
            "catalog-entry.example.json",
            "courses/MAN101-pengantar-manajemen.md",
            "courses/ECO101-pengantar-ekonomi.md",
        ):
            if not (target / relative).is_file():
                raise AssertionError(f"Scaffold kehilangan {relative}")

        manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
        if manifest["status"] != "experimental" or manifest["maintainer"] != "community":
            raise AssertionError("Generator tidak boleh mengklaim draft sebagai maintained/verified pack.")
        if manifest["total_sks"] != 5:
            raise AssertionError(f"Total SKS salah: {manifest['total_sks']}")
        if manifest["period_label"] != "Trimester 1":
            raise AssertionError("Builder kembali mengasumsikan semester.")
        if [suite["scope"] for suite in manifest["eval_suites"]] != ["core", "pack"]:
            raise AssertionError("Eval scaffold minimal harus core → pack.")

        contracts = json.loads((target / "evals/contracts.json").read_text(encoding="utf-8"))
        behavior = json.loads((target / "evals/behavior.json").read_text(encoding="utf-8"))
        if contracts["cases"] or behavior["cases"]:
            raise AssertionError("Builder tidak boleh mengarang regression case.")

        registry = json.loads((target / "source-registry.json").read_text(encoding="utf-8"))
        if registry["scope"] != "pack" or registry["pack_id"] != manifest["id"]:
            raise AssertionError("Pack registry identity tidak konsisten dengan manifest.")

        catalog = json.loads((target / "catalog-entry.example.json").read_text(encoding="utf-8"))
        if catalog["manifest"] != "kampus-contoh/s1-manajemen/2026-2027/trimester-01/manifest.json":
            raise AssertionError(f"Catalog manifest path salah: {catalog['manifest']}")

        second = run(*common)
        if second.returncode == 0:
            raise AssertionError("Builder tidak boleh overwrite scaffold tanpa --force.")
        forced = run(*common, "--force")
        if forced.returncode != 0:
            raise AssertionError(f"Builder --force gagal: {forced.stderr}")

        bad_url = run(*replace_value(common, "--source-url", "http://example.edu/catalog"), "--force")
        if bad_url.returncode == 0:
            raise AssertionError("Source URL non-HTTPS harus ditolak.")

        bad_id = run(*replace_value(common, "--pack-id", "ID WITH SPACE"), "--force")
        if bad_id.returncode == 0:
            raise AssertionError("Pack ID non-machine-safe harus ditolak.")

        future_date = run(*replace_value(common, "--reviewed-at", "2999-01-01"), "--force")
        if future_date.returncode == 0:
            raise AssertionError("Tanggal review masa depan harus ditolak.")

    print("Community pack builder regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
