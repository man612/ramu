#!/usr/bin/env python3
"""Scaffold community pack Ramu yang tetap berstatus experimental sampai direview."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from ramu_repo import ROOT

MACHINE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]+$")
COURSE_CODE = re.compile(r"^[A-Za-z0-9._-]{2,32}$")
TEMPLATE = ROOT / "starter" / "PROJECT-INSTRUCTIONS.md"


@dataclass(frozen=True)
class Course:
    code: str
    name: str
    short_name: str
    sks: int
    focus: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Buat scaffold community pack Ramu. Hasil tetap experimental dan belum otomatis masuk katalog."
    )
    parser.add_argument("--institution", required=True)
    parser.add_argument("--institution-id", required=True)
    parser.add_argument("--program", required=True)
    parser.add_argument("--program-id", required=True)
    parser.add_argument("--academic-year", required=True)
    parser.add_argument("--period-id", required=True)
    parser.add_argument("--period-label", required=True)
    parser.add_argument("--pack-id", required=True)
    parser.add_argument(
        "--course",
        action="append",
        required=True,
        metavar="CODE|NAME|SHORT|SKS|FOCUS",
        help="Mata kuliah; ulangi flag untuk course lain.",
    )
    parser.add_argument("--source-url", required=True, help="Minimal satu source HTTPS yang direview contributor.")
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--source-authority", default="", help="Default: nama institusi.")
    parser.add_argument("--source-kind", default="official-source")
    parser.add_argument("--reviewed-at", default=date.today().isoformat(), help="Tanggal contributor membaca source, YYYY-MM-DD.")
    parser.add_argument("--review-interval-days", type=int, default=60)
    parser.add_argument("--pack-version", default="draft.1")
    parser.add_argument("--output-root", help="Root fisik pengganti packs/; berguna untuk dry-run/test.")
    parser.add_argument("--force", action="store_true", help="Izinkan overwrite scaffold pada path yang sama.")
    return parser.parse_args()


def clean(value: str) -> str:
    return " ".join(str(value).strip().split())


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "item"


def require_machine_id(label: str, value: str) -> str:
    normalized = clean(value)
    if not MACHINE_ID.fullmatch(normalized):
        raise ValueError(f"{label} harus machine-safe sesuai pola {MACHINE_ID.pattern}: {value!r}")
    return normalized


def parse_review_date(value: str) -> str:
    normalized = clean(value)
    try:
        datetime.strptime(normalized, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("--reviewed-at harus YYYY-MM-DD.") from exc
    return normalized


def parse_course(raw: str) -> Course:
    parts = [clean(part) for part in raw.split("|", 4)]
    if len(parts) != 5 or any(not part for part in parts):
        raise ValueError(f"Format --course harus CODE|NAME|SHORT|SKS|FOCUS: {raw!r}")
    code, name, short_name, raw_sks, focus = parts
    if not COURSE_CODE.fullmatch(code):
        raise ValueError(f"Course code tidak machine-safe: {code!r}")
    try:
        sks = int(raw_sks)
    except ValueError as exc:
        raise ValueError(f"SKS harus integer: {raw_sks!r}") from exc
    if sks < 0:
        raise ValueError("SKS tidak boleh negatif.")
    return Course(code=code, name=name, short_name=short_name, sks=sks, focus=focus)


def json_write(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pack_relative_path(institution_id: str, program: str, academic_year: str, period_id: str) -> Path:
    return Path("packs") / institution_id / slugify(program) / slugify(academic_year) / period_id


def ensure_target(target: Path, force: bool) -> None:
    owned = [
        target / "manifest.json",
        target / "PROJECT-INSTRUCTIONS.md",
        target / "source-registry.json",
        target / "evals/contracts.json",
        target / "evals/behavior.json",
    ]
    conflicts = [path for path in owned if path.exists()]
    if conflicts and not force:
        raise FileExistsError(
            "Scaffold sudah ada: " + ", ".join(str(path) for path in conflicts) + ". Gunakan --force bila sengaja mengganti draft."
        )
    (target / "courses").mkdir(parents=True, exist_ok=True)
    (target / "evals").mkdir(parents=True, exist_ok=True)


def render_course_file(course: Course, *, period_label: str, pack_version: str, reviewed_at: str) -> str:
    return f"""# {course.code} — {course.name}

**Status:** community pack draft / experimental  
**Periode:** {period_label}  
**SKS:** {course.sks}  
**Versi paket:** {pack_version}  
**Tanggal review contributor:** {reviewed_at}

## Fokus

{course.focus}

## Source dan konteks

Scaffold ini tidak mengarang outline, capaian pembelajaran, aturan tugas, atau isi materi. Tambahkan hanya informasi yang benar-benar didukung syllabus, katalog, handbook, regulator, atau source lain yang sesuai fungsi dan otoritasnya.

## Workflow mata kuliah

- baca soal/rubrik/material yang relevan sebelum menjawab;
- bedakan fakta course dengan aturan yang sensitif waktu;
- tampilkan asumsi bila data pengguna belum lengkap;
- tambahkan verifier khusus hanya untuk failure mode yang benar-benar penting pada course ini;
- jangan menyalin materi berhak cipta ke repository.

## TODO sebelum diajukan sebagai public pack

- isi konteks course dari source yang boleh dipublikasikan;
- catat source/claim penting pada registry dengan locator/evidence bila diperlukan;
- tambahkan eval pack-specific bila ada failure mode yang perlu direproduksi;
- review Project Instructions terhadap kebijakan institusi/tutor yang benar-benar berlaku.
"""


def render_readme(*, pack_id: str, relative_path: Path, source_id: str) -> str:
    manifest_path = (relative_path / "manifest.json").as_posix().removeprefix("packs/")
    return f"""# Community pack draft

Scaffold ini dibuat oleh `scripts/create_pack.py` dan **belum otomatis menjadi pack publik**.

Status awal sengaja `experimental` + `maintainer: community`. Tanggal pada `source_verified_at` berarti contributor menyatakan telah membaca source input pada tanggal tersebut; itu **bukan endorsement atau verifikasi maintainer Ramu**.

Sebelum mendaftarkan `{pack_id}` ke `packs/index.json`:

1. review setiap metadata course terhadap source yang tepat;
2. pastikan source `{source_id}` benar-benar mendukung klaim yang dipakai;
3. tambahkan source/claim lain jika satu source tidak cukup;
4. isi course pack tanpa menyalin materi berhak cipta;
5. tambahkan eval khusus bila ada failure mode pack-specific;
6. review identity (`institution_id`, `program_id`, pack `id`) karena ID yang sudah dipublish sebaiknya stabil;
7. tambahkan entry katalog dengan `manifest: {manifest_path}`;
8. jalankan seluruh validation stack sebelum membuka PR.

`evals/contracts.json` dan `evals/behavior.json` sengaja mulai dengan `cases: []`. Jangan membuat regression case palsu hanya agar file terlihat penuh.
"""


def main() -> int:
    args = parse_args()
    try:
        institution = clean(args.institution)
        program = clean(args.program)
        academic_year = clean(args.academic_year)
        period_label = clean(args.period_label)
        if len(institution) < 2 or len(program) < 2 or len(period_label) < 2 or len(academic_year) < 4:
            raise ValueError("Label institusi/program/tahun/periode terlalu pendek.")

        institution_id = require_machine_id("institution_id", args.institution_id)
        program_id = require_machine_id("program_id", args.program_id)
        period_id = require_machine_id("period_id", args.period_id)
        pack_id = require_machine_id("pack_id", args.pack_id)
        reviewed_at = parse_review_date(args.reviewed_at)
        pack_version = clean(args.pack_version)
        if not pack_version:
            raise ValueError("pack_version tidak boleh kosong.")
        if args.review_interval_days < 1:
            raise ValueError("review_interval_days harus >= 1.")
        if not args.source_url.startswith("https://"):
            raise ValueError("--source-url harus memakai HTTPS.")

        courses = [parse_course(raw) for raw in args.course]
        codes = [course.code for course in courses]
        if len(codes) != len(set(codes)):
            raise ValueError("Course code duplikat pada input.")

        relative_path = pack_relative_path(institution_id, program, academic_year, period_id)
        output_root = Path(args.output_root).expanduser() if args.output_root else ROOT / "packs"
        target = output_root / Path(*relative_path.parts[1:])
        ensure_target(target, args.force)

        source_id = f"{slugify(institution_id)}-{slugify(period_id)}-primary"
        source_name = clean(args.source_name)
        authority = clean(args.source_authority) or institution
        source_registry_rel = (relative_path / "source-registry.json").as_posix()
        contracts_rel = (relative_path / "evals/contracts.json").as_posix()
        behavior_rel = (relative_path / "evals/behavior.json").as_posix()
        instructions_rel = "PROJECT-INSTRUCTIONS.md"

        course_entries = []
        for course in courses:
            filename = f"courses/{course.code}-{slugify(course.short_name)}.md"
            course_entries.append(
                {
                    "code": course.code,
                    "name": course.name,
                    "short_name": course.short_name,
                    "project_name": f"{period_label} • {course.short_name}",
                    "sks": course.sks,
                    "focus": course.focus,
                    "file": filename,
                }
            )
            course_path = target / filename
            course_path.parent.mkdir(parents=True, exist_ok=True)
            course_path.write_text(
                render_course_file(course, period_label=period_label, pack_version=pack_version, reviewed_at=reviewed_at),
                encoding="utf-8",
            )

        manifest = {
            "schema_version": 4,
            "id": pack_id,
            "name": f"{institution} {program} — {period_label}",
            "institution_id": institution_id,
            "institution": institution,
            "program_id": program_id,
            "program": program,
            "academic_year": academic_year,
            "period_id": period_id,
            "period_label": period_label,
            "total_sks": sum(course.sks for course in courses),
            "status": "experimental",
            "maintainer": "community",
            "pack_version": pack_version,
            "contract_version": "1.1",
            "project_instructions": instructions_rel,
            "learning_protocols": ["belajar", "tugas", "review", "latihan-ujian"],
            "courses": course_entries,
            "sources": [
                {
                    "type": clean(args.source_kind),
                    "name": source_name,
                    "url": args.source_url,
                    "registry_id": source_id,
                }
            ],
            "source_registries": ["sources/registry.json", source_registry_rel],
            "eval_suites": [
                {
                    "id": "core",
                    "scope": "core",
                    "contracts": "evals/core/contracts.json",
                    "behavior": "evals/core/behavior.json",
                },
                {
                    "id": pack_id,
                    "scope": "pack",
                    "scope_ref": pack_id,
                    "contracts": contracts_rel,
                    "behavior": behavior_rel,
                },
            ],
            "source_verified_at": reviewed_at,
        }
        json_write(target / "manifest.json", manifest)

        registry = {
            "version": 1,
            "scope": "pack",
            "institution_id": institution_id,
            "institution": institution,
            "program_id": program_id,
            "program": program,
            "pack_id": pack_id,
            "verified_at": reviewed_at,
            "sources": [
                {
                    "id": source_id,
                    "name": source_name,
                    "kind": clean(args.source_kind),
                    "authority": authority,
                    "url": args.source_url,
                    "canonical_for": ["metadata awal community pack yang direview contributor"],
                    "freshness_class": "academic-current",
                    "verified_at": reviewed_at,
                    "review_interval_days": args.review_interval_days,
                    "watch": True,
                    "status": "active",
                    "notes": "Scaffold contributor; review authority/canonical_for kembali sebelum menaikkan status pack.",
                }
            ],
            "claims": [],
        }
        json_write(target / "source-registry.json", registry)

        contracts = {
            "version": 1,
            "suite_id": pack_id,
            "scope": "pack",
            "scope_ref": pack_id,
            "cases": [],
        }
        behavior = {
            "version": 1,
            "suite_id": pack_id,
            "scope": "pack",
            "scope_ref": pack_id,
            "defaults": {"min_score": 0.8, "max_output_tokens": 1400},
            "cases": [],
        }
        json_write(target / "evals/contracts.json", contracts)
        json_write(target / "evals/behavior.json", behavior)

        instructions = TEMPLATE.read_text(encoding="utf-8").replace(
            "# Project Instructions — Ramu Starter", "# Project Instructions — Ramu Community Pack Draft", 1
        )
        (target / "PROJECT-INSTRUCTIONS.md").write_text(instructions, encoding="utf-8")
        (target / "README.md").write_text(
            render_readme(pack_id=pack_id, relative_path=relative_path, source_id=source_id), encoding="utf-8"
        )

        catalog_entry = {
            "id": pack_id,
            "name": manifest["name"],
            "institution_id": institution_id,
            "institution": institution,
            "program_id": program_id,
            "program": program,
            "academic_year": academic_year,
            "period_id": period_id,
            "period_label": period_label,
            "status": "experimental",
            "maintainer": "community",
            "manifest": (relative_path / "manifest.json").as_posix().removeprefix("packs/"),
        }
        json_write(target / "catalog-entry.example.json", catalog_entry)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Community pack scaffold siap: {target.resolve()}")
    print("Status tetap experimental/community dan belum ditambahkan ke packs/index.json.")
    print("Review README.md di folder draft, lalu jalankan validation stack setelah entry katalog ditambahkan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
