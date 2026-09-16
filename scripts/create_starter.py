#!/usr/bin/env python3
"""Buat personal Ramu Starter tanpa API dan tanpa mendaftarkannya sebagai public pack."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from ramu_repo import ROOT

TEMPLATE = ROOT / "starter" / "PROJECT-INSTRUCTIONS.md"
OWNED_FILES = ("PROJECT-INSTRUCTIONS.md", "COURSE-PACK.txt", "START-HERE.md", "starter.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Buat workspace Ramu personal untuk satu mata kuliah. Tidak membutuhkan OpenAI API."
    )
    parser.add_argument("--course", help="Nama mata kuliah. Bila kosong, akan ditanyakan secara interaktif.")
    parser.add_argument("--institution", default="", help="Nama institusi/kampus (opsional).")
    parser.add_argument("--period", default="", help="Periode manusiawi, misalnya Semester 4 (opsional).")
    parser.add_argument("--project-name", default="", help="Nama ChatGPT Project; default diturunkan dari periode + mata kuliah.")
    parser.add_argument("--goal", action="append", default=[], help="Tujuan belajar; dapat diulang.")
    parser.add_argument("--source", action="append", default=[], help="Source/file utama yang dimiliki; dapat diulang.")
    parser.add_argument("--rule", action="append", default=[], help="Aturan tutor/dosen/kampus yang perlu diingat; dapat diulang.")
    parser.add_argument("--output", help="Folder output. Default: ./ramu-starter-<mata-kuliah>.")
    parser.add_argument("--force", action="store_true", help="Izinkan mengganti empat file Starter milik generator di folder output.")
    return parser.parse_args()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "course"


def clean(value: str) -> str:
    return " ".join(str(value).strip().split())


def bullet_lines(items: list[str], empty: str) -> str:
    normalized = [clean(item) for item in items if clean(item)]
    if not normalized:
        return f"- {empty}"
    return "\n".join(f"- {item}" for item in normalized)


def resolve_course(raw: str | None) -> str:
    value = clean(raw or "")
    if value:
        return value
    if not sys.stdin.isatty():
        raise ValueError("--course wajib bila command dijalankan non-interaktif.")
    value = clean(input("Nama mata kuliah: "))
    if not value:
        raise ValueError("Nama mata kuliah tidak boleh kosong.")
    return value


def ensure_output(path: Path, force: bool) -> None:
    path.mkdir(parents=True, exist_ok=True)
    conflicts = [name for name in OWNED_FILES if (path / name).exists()]
    if conflicts and not force:
        joined = ", ".join(conflicts)
        raise FileExistsError(f"Folder output sudah punya file Starter ({joined}). Gunakan --force bila memang ingin menggantinya.")


def render_course_pack(
    *,
    course: str,
    institution: str,
    period: str,
    project_name: str,
    goals: list[str],
    sources: list[str],
    rules: list[str],
) -> str:
    return f"""# Ramu Starter — {course}

**Status:** personal starter / belum diverifikasi maintainer Ramu  
**Dibuat:** {date.today().isoformat()}  
**Project:** {project_name}  
**Institusi:** {institution or 'belum diisi'}  
**Periode:** {period or 'belum diisi'}

## Batas konteks

File ini merangkum konteks yang diberikan pengguna. Jangan memperlakukan metadata di sini sebagai fakta resmi bila belum didukung source yang sesuai. Materi, syllabus, rubrik, screenshot, dan file resmi tetap perlu ditambahkan ke Project Sources ketika relevan.

## Tujuan belajar

{bullet_lines(goals, 'belum ditentukan; tanyakan tujuan sebelum menyusun rencana jangka panjang')}

## Source/file yang tersedia

{bullet_lines(sources, 'belum dicatat; minta pengguna menambahkan syllabus, materi, atau source resmi yang relevan')}

## Aturan tutor/dosen/kampus

{bullet_lines(rules, 'belum dicatat; jangan mengarang kebijakan penggunaan AI atau aturan tugas')}

## Workflow penggunaan

- Bedakan sesi belajar, tugas, review, riset, dan latihan ujian.
- Gunakan source sesuai fungsi dan otoritasnya; current rule perlu current source.
- Jangan menebak isi file/data yang tidak tersedia atau tidak terbaca.
- Untuk graded work, ikuti rubrik dan batas penggunaan AI yang benar-benar diberikan.
- Simpan learner state hanya bila ada evidence dari sesi belajar, bukan dari asumsi kemampuan pengguna.
- Bila konteks mata kuliah berubah secara material, perbarui file Starter ini atau buat Catatan Belajar Terbaru yang jelas tanggalnya.
"""


def render_start_here(*, project_name: str, course: str) -> str:
    return f"""# Mulai Ramu Starter

Starter ini untuk penggunaan personal dan **bukan public/maintained pack Ramu**.

1. Buat satu ChatGPT Project bernama **{project_name}**.
2. Gunakan Project-only memory bila opsi tersebut tersedia untuk Project yang dibuat.
3. Tempel isi `PROJECT-INSTRUCTIONS.md` ke Project Instructions.
4. Unggah `COURSE-PACK.txt` ke Project Sources.
5. Tambahkan syllabus, materi, rubrik, atau source resmi untuk **{course}** saat dibutuhkan.
6. Mulai dari satu kebutuhan nyata: memahami topik, mengerjakan latihan, membaca feedback, atau menyiapkan tugas.

Jangan memasukkan credential, data pribadi yang tidak perlu, atau materi berhak cipta ke repository publik. File personal ini boleh tetap lokal.
"""


def main() -> int:
    args = parse_args()
    try:
        course = resolve_course(args.course)
        institution = clean(args.institution)
        period = clean(args.period)
        project_name = clean(args.project_name) or (f"{period} • {course}" if period else course)
        output = Path(args.output).expanduser() if args.output else Path.cwd() / f"ramu-starter-{slugify(course)}"
        ensure_output(output, args.force)

        instructions = TEMPLATE.read_text(encoding="utf-8")
        (output / "PROJECT-INSTRUCTIONS.md").write_text(instructions, encoding="utf-8")
        (output / "COURSE-PACK.txt").write_text(
            render_course_pack(
                course=course,
                institution=institution,
                period=period,
                project_name=project_name,
                goals=args.goal,
                sources=args.source,
                rules=args.rule,
            ),
            encoding="utf-8",
        )
        (output / "START-HERE.md").write_text(
            render_start_here(project_name=project_name, course=course), encoding="utf-8"
        )
        metadata = {
            "format": "ramu-personal-starter",
            "version": 1,
            "generated_at": date.today().isoformat(),
            "course": course,
            "institution": institution or None,
            "period": period or None,
            "project_name": project_name,
            "goals": [clean(item) for item in args.goal if clean(item)],
            "sources": [clean(item) for item in args.source if clean(item)],
            "rules": [clean(item) for item in args.rule if clean(item)],
            "public_pack": False,
            "source_verified": False,
        }
        (output / "starter.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Ramu Starter siap: {output.resolve()}")
    print("Artefak: PROJECT-INSTRUCTIONS.md, COURSE-PACK.txt, START-HERE.md, starter.json")
    print("Status: personal starter; tidak otomatis menjadi public/community pack.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
