#!/usr/bin/env python3
"""Pastikan label yang dilihat pengguna tidak memakai singkatan periode yang ambigu."""

from __future__ import annotations

import sys

from ramu_repo import ROOT, PACK_INDEX, RepoError, load_json


def main() -> int:
    errors: list[str] = []
    try:
        index = load_json(PACK_INDEX)
    except RepoError as exc:
        print(f"Display-name validation — discovery gagal: {exc}", file=sys.stderr)
        return 2
    index_by_id = {entry["id"]: entry for entry in index.get("packs", [])}

    for manifest_path in sorted((ROOT / "packs").glob("**/manifest.json")):
        try:
            manifest = load_json(manifest_path)
        except RepoError as exc:
            errors.append(str(exc))
            continue
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
