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
        'data-pack-picker',
        'data-pack-picker-trigger',
        'data-pack-picker-menu',
        'data-setup-link',
        'href="catalog.css"',
        'id="course-list"',
        'id="pack-title"',
        'rel="canonical" href="https://man612.github.io/ramu/"',
        'property="og:url" content="https://man612.github.io/ramu/"',
        'href="https://github.com/man612/ramu/blob/main/SUPPORT.md"',
    ])
    require_text(SITE / "setup.html", [
        'data-pack-picker',
        'data-pack-picker-trigger',
        'data-pack-picker-menu',
        'href="catalog.css"',
        'id="setup-pack-name"',
        'id="setup-courses"',
        'id="copy-instructions"',
        "Project-only memory",
        "Project settings → Memory",
        "Ramu tidak bergantung pada Study Mode",
        "Save to project",
        "Add to project sources",
        'rel="canonical" href="https://man612.github.io/ramu/setup.html"',
        'property="og:url" content="https://man612.github.io/ramu/setup.html"',
    ])
    require_text(SITE / "app.js", [
        'const PACK_INDEX_URL = "./packs/index.json"',
        "currentPackEntry(catalog)",
        "manifestUrl(entry)",
        "item.period_label || item.period_id",
        "course.focus",
        "manifest.project_instructions",
        "renderPackPickers(catalog, entry)",
        'aria-selected',
        'event.key === "ArrowDown"',
        'event.key === "Escape"',
    ])
    require_text(SITE / "catalog.css", [
        ".pack-picker-panel",
        ".pack-picker-trigger",
        ".pack-picker-menu",
        ".pack-picker-option",
        "#setup-pack-count",
    ])

    app_text = (SITE / "app.js").read_text(encoding="utf-8") if (SITE / "app.js").is_file() else ""
    for forbidden in (
        "const PACK_BASE",
        "const COURSE_FOCUS",
        "universitas-terbuka/s1-akuntansi/2026-2027/semester-02",
        "item.semester",
        "manifest.semester",
        "Semester ${",
        "renderPackSelectors",
        "Add from library",
    ):
        if forbidden in app_text:
            fail(f"site/app.js masih punya hardcode/asumsi/UI contract lama: {forbidden!r}")

    index_text = (SITE / "index.html").read_text(encoding="utf-8") if (SITE / "index.html").is_file() else ""
    setup_text = (SITE / "setup.html").read_text(encoding="utf-8") if (SITE / "setup.html").is_file() else ""

    for path_name, text in (("site/index.html", index_text), ("site/setup.html", setup_text)):
        if "<select" in text.lower():
            fail(f"{path_name} masih memakai native browser select untuk pack picker.")

    for forbidden in (
        "kecuali manifest pack menyatakan berbeda",
        "Add from library</strong> juga bisa dipakai",
        "Study Mode wajib",
    ):
        if forbidden in setup_text:
            fail(f"site/setup.html masih punya janji produk/schema yang tidak aman: {forbidden!r}")

    for stale_copy in (
        "workspace belajar yang sudah diramu",
        "Coba kecil dulu",
        "Kalau sudah terasa berguna",
        "dijaga di belakang layar",
    ):
        if stale_copy.lower() in index_text.lower() or stale_copy.lower() in setup_text.lower():
            fail(f"Site masih memuat marketing copy lama yang sengaja dihapus: {stale_copy!r}")

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
    print(f"OK: site catalog-driven untuk {len(catalog.get('packs', []))} pack dengan custom pack picker.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
