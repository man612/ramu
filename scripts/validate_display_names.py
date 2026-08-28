#!/usr/bin/env python3
"""Pastikan label yang dilihat pengguna tidak memakai singkatan periode yang ambigu."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_INDEX = ROOT / "packs/index.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    index = load_json(PACK_INDEX)
    index_by_id = {entry["id"]: entry for entry in index.get("packs", [])}

    for manifest_path in sorted((ROOT / "packs").glob("**/manifest.json")):
        manifest = load_json(manifest_path)
        pack_id = str(manifest.get("id", "<tanpa-id>"))
        period_label = str(manifest.get("period_label", "")).strip()

        if not period_label:
            errors.append(f"{pack_id}: manifest harus punya period_label yang jelas untuk pengguna.")
            continue

        entry = index_by_id.get(pack_id)
        if not entry:
            errors.append(f"{pack_id}: tidak ditemukan di packs/index.json.")
        elif str(entry.get("period_label", "")).strip() != period_label:
            errors.append(f"{pack_id}: period_label katalog berbeda dari manifest.")

        expected_prefix = f"{period_label} • "
        for course in manifest.get("courses", []):
            code = course.get("code", "<tanpa-kode>")
            project_name = str(course.get("project_name", "")).strip()
            if not project_name.startswith(expected_prefix):
                errors.append(
                    f"{pack_id} {code}: project_name harus diawali {expected_prefix!r}; "
                    f"sekarang {project_name!r}. Gunakan label periode eksplisit, bukan S2/S3 yang ambigu."
                )

    if errors:
        print(f"Display-name validation — {len(errors)} error")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Display-name validation — OK: semua nama Project memakai period_label eksplisit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
