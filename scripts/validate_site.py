#!/usr/bin/env python3
"""Static contract check untuk GitHub Pages Ramu tanpa dependency eksternal."""

from __future__ import annotations

import sys
from pathlib import Path

from ramu_repo import ROOT, RepoError, load_pack_index, pack_context

SITE = ROOT / "site"
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def require_text(path: Path, needles: list[str]) -> None:
    if not path.is_file():
        fail(f"Site file tidak ditemukan: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{path.relative_to(ROOT)} kehilangan marker {needle!r}")


def main() -> int:
    try:
        catalog = load_pack_index()
    except RepoError as exc:
        fail(str(exc))
        catalog = {"packs": []}

    require_text(SITE / "index.html", [
        'id="pack-select"',
        'data-setup-link',
        'href="catalog.css"',
        'id="course-list"',
        'id="pack-title"',
    ])
    require_text(SITE / "setup.html", [
        'id="pack-select"',
        'href="catalog.css"',
        'id="setup-pack-name"',
        'id="setup-courses"',
        'id="copy-instructions"',
        "Project-only memory",
        "Project settings → Memory",
        "Ramu tidak bergantung pada Study Mode",
        "Save to project",
        "Add to project sources",
    ])
    require_text(SITE / "app.js", [
        'const PACK_INDEX_URL = "./packs/index.json"',
        "currentPackEntry(catalog)",
        "manifestUrl(entry)",
        "item.period_label || item.period_id",
        "course.focus",
        "manifest.project_instructions",
    ])
    require_text(SITE / "catalog.css", [".pack-picker-panel", "#setup-pack-count"])

    app_text = (SITE / "app.js").read_text(encoding="utf-8") if (SITE / "app.js").is_file() else ""
    for forbidden in (
        "const PACK_BASE",
        "const COURSE_FOCUS",
        "universitas-terbuka/s1-akuntansi/2026-2027/semester-02",
        "item.semester",
        "manifest.semester",
        "Semester ${",
    ):
        if forbidden in app_text:
            fail(f"site/app.js masih hardcode/asumsi pack-periode: {forbidden!r}")

    setup_text = (SITE / "setup.html").read_text(encoding="utf-8") if (SITE / "setup.html").is_file() else ""
    for forbidden in (
        "kecuali manifest pack menyatakan berbeda",
        "Add from library</strong> juga bisa dipakai",
        "Study Mode wajib",
    ):
        if forbidden in setup_text:
            fail(f"site/setup.html masih punya janji produk/schema yang tidak aman: {forbidden!r}")

    for entry in catalog.get("packs", []):
        try:
            ctx = pack_context(entry.get("id"))
        except RepoError as exc:
            fail(str(exc))
            continue
        manifest = ctx["manifest"]
        if not str(entry.get("period_id", "")).strip() or not str(entry.get("period_label", "")).strip():
            fail(f"Pack catalog {entry.get('id')} harus punya period_id + period_label untuk site.")
        if not str(manifest.get("period_id", "")).strip() or not str(manifest.get("period_label", "")).strip():
            fail(f"Pack {ctx['id']} harus punya period_id + period_label untuk site.")
        for course in manifest.get("courses", []):
            if not str(course.get("focus", "")).strip():
                fail(f"Pack {ctx['id']} course {course.get('code')} tidak punya focus untuk site.")
        if not str(manifest.get("project_instructions", "")).strip():
            fail(f"Pack {ctx['id']} tidak punya project_instructions untuk setup site.")

    print(f"Ramu site validation — {len(errors)} error")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"OK: site catalog-driven untuk {len(catalog.get('packs', []))} pack.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
