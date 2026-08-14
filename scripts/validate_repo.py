#!/usr/bin/env python3
"""Validasi struktur Ramu tanpa dependency eksternal."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02"
MANIFEST = PACK / "manifest.json"
REGISTRY = ROOT / "sources/registry.json"
EVALS = ROOT / "evals/cases/semester-02.json"

errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"File tidak ditemukan: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"JSON tidak valid: {path.relative_to(ROOT)}:{exc.lineno}:{exc.colno} — {exc.msg}")
    return None


def contains_casefold(path: Path, needle: str) -> bool:
    try:
        haystack = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return False
    return needle.casefold() in haystack.casefold()


manifest = load_json(MANIFEST)
if manifest:
    required = ["id", "academic_year", "semester", "total_sks", "project_instructions", "courses"]
    for key in required:
        if key not in manifest:
            fail(f"manifest.json kehilangan field `{key}`")

    courses = manifest.get("courses", [])
    codes = [course.get("code") for course in courses]
    if len(codes) != len(set(codes)):
        fail("Kode mata kuliah di manifest harus unik.")

    calculated_sks = sum(int(course.get("sks", 0)) for course in courses)
    if calculated_sks != manifest.get("total_sks"):
        fail(f"Total SKS manifest {manifest.get('total_sks')} tidak sama dengan jumlah course {calculated_sks}.")

    instructions = PACK / manifest.get("project_instructions", "")
    if not instructions.is_file():
        fail(f"Project Instructions tidak ditemukan: {instructions.relative_to(ROOT)}")

    for course in courses:
        course_file = PACK / course.get("file", "")
        if not course_file.is_file():
            fail(f"Course file tidak ditemukan untuk {course.get('code')}: {course_file.relative_to(ROOT)}")

registry = load_json(REGISTRY)
if registry:
    source_ids: list[str] = []
    allowed_status = {"active", "secondary", "signal-only"}
    for source in registry.get("sources", []):
        sid = source.get("id")
        source_ids.append(sid)
        for key in (
            "id", "name", "kind", "authority", "url", "canonical_for",
            "freshness_class", "verified_at", "review_interval_days", "watch", "status"
        ):
            if key not in source:
                fail(f"Sumber {sid or '<tanpa-id>'} kehilangan field `{key}`")
        if not str(source.get("url", "")).startswith("https://"):
            fail(f"Sumber {sid} harus memakai HTTPS.")
        if source.get("status") not in allowed_status:
            fail(f"Status sumber {sid} tidak dikenal: {source.get('status')}")
        if not isinstance(source.get("review_interval_days"), int) or source.get("review_interval_days", 0) < 1:
            fail(f"review_interval_days sumber {sid} harus integer positif.")
    if len(source_ids) != len(set(source_ids)):
        fail("ID pada source registry harus unik.")

evals = load_json(EVALS)
if evals:
    case_ids: list[str] = []
    for case in evals.get("cases", []):
        cid = case.get("id", "<tanpa-id>")
        case_ids.append(cid)
        for key in ("title", "intent", "scenario", "expected_behaviors", "forbidden_behaviors", "contracts"):
            if not case.get(key):
                fail(f"Eval {cid} kehilangan/empty field `{key}`")
        for contract in case.get("contracts", []):
            target = ROOT / contract.get("file", "")
            marker = contract.get("contains", "")
            if not target.is_file():
                fail(f"Eval {cid}: contract file tidak ditemukan: {contract.get('file')}")
                continue
            if not marker:
                fail(f"Eval {cid}: contract marker kosong untuk {contract.get('file')}")
                continue
            if not contains_casefold(target, marker):
                fail(f"Eval {cid}: marker tidak ditemukan di {contract.get('file')}: {marker!r}")
    if len(case_ids) != len(set(case_ids)):
        fail("ID eval harus unik.")

for template in (
    "learning/learner-state.template.md",
    "learning/review-queue.template.md",
    "learning/misconception-log.template.md",
    "learning/mastery-map.template.md",
):
    if not (ROOT / template).is_file():
        fail(f"Template belajar tidak ditemukan: {template}")

for protocol in (
    "protocols/belajar.md",
    "protocols/tugas.md",
    "protocols/review.md",
    "protocols/latihan-ujian.md",
):
    if not (ROOT / protocol).is_file():
        fail(f"Protokol tidak ditemukan: {protocol}")

print(f"Ramu validation — {len(errors)} error, {len(warnings)} warning")
for warning in warnings:
    print(f"WARNING: {warning}")
for error in errors:
    print(f"ERROR: {error}")

if errors:
    sys.exit(1)

print(
    f"OK: {len(manifest.get('courses', [])) if manifest else 0} course, "
    f"{len(registry.get('sources', [])) if registry else 0} source, "
    f"{len(evals.get('cases', [])) if evals else 0} eval contract."
)
