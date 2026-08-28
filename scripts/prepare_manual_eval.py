#!/usr/bin/env python3
"""Buat checklist behavior eval dari merged suite untuk diuji manual tanpa API."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from ramu_repo import ROOT, RepoError, merged_eval_suite, pack_context


def selected(cases: list[dict], only: str) -> list[dict]:
    if not only or only.casefold() == "all":
        return cases
    wanted = {item.strip().upper() for item in only.split(",") if item.strip()}
    result = [case for case in cases if case.get("id", "").upper() in wanted]
    missing = wanted - {case.get("id", "").upper() for case in result}
    if missing:
        raise RepoError(f"Case tidak ditemukan: {', '.join(sorted(missing))}")
    return result


def block(text: str) -> str:
    return "\n".join("> " + line for line in text.splitlines())


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate manual eval checklist tanpa API.")
    parser.add_argument("--pack", default=None, help="Pack id; default memakai default_pack_id.")
    parser.add_argument("--only", default="all", help="all atau E01,E05,E13")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    ctx = pack_context(args.pack)
    contracts, behavior = merged_eval_suite(ctx)
    contract_by_id = {case["id"]: case for case in contracts["cases"]}
    cases = selected(behavior["cases"], args.only)
    suite_order = contracts.get("suite_order", [])

    safe = ctx["id"].replace(".", "-")
    output = Path(args.output) if args.output else ROOT / "evals/manual" / f"{safe}-checklist.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Ramu Manual Behavior Validation",
        "",
        f"- Pack: `{ctx['id']}`",
        f"- Pack version: `{ctx['manifest'].get('pack_version')}`",
        f"- Contract version: `{ctx['manifest'].get('contract_version')}`",
        f"- Eval suites: {' → '.join(f'`{item}`' for item in suite_order)}",
        f"- Checklist dibuat: {date.today().isoformat()}",
        "- Diuji pada tanggal: ____________________",
        "- ChatGPT plan/model yang terlihat: ____________________",
        "- Tester: ____________________",
        "",
        "## Cara pakai",
        "",
        "1. Buat/pakai ChatGPT Project yang sudah dipasang Project Instructions + course pack sesuai konteks case.",
        "2. Untuk tiap case, mulai chat baru agar hasil satu case tidak mencemari case lain.",
        "3. Kirim turn `user` berurutan. Turn `assistant` di checklist adalah konteks simulasi; gunakan hanya bila case memang multi-turn.",
        "4. Nilai perilaku, bukan apakah gaya bahasanya persis sama dengan expected behavior.",
        "5. Jika ada forbidden behavior material, tandai FAIL meski sebagian jawaban lain benar.",
        "6. Catat suite asal case. Failure pada suite institusi/program sebaiknya diperbaiki di scope tersebut, bukan dicopy sebagai patch pack.",
        "7. Simpan hanya hasil/catatan yang aman; jangan menaruh percakapan privat, credential, atau materi berhak cipta ke repo publik.",
        "",
        "> Manual validation menguji ChatGPT Projects asli dan tidak memerlukan OpenAI API. Hasil tetap berupa snapshot perilaku pada tanggal/model/produk tertentu, bukan jaminan permanen.",
        "",
    ]

    for case in cases:
        cid = case["id"]
        contract = contract_by_id[cid]
        suite_id = str(case.get("suite_id") or contract.get("suite_id") or "unknown")
        lines.extend([
            f"## {cid} — {contract['title']}",
            "",
            f"**Suite:** `{suite_id}`",
            "",
            f"**Intent:** {contract['intent']}",
            "",
            "**Percakapan uji**",
            "",
        ])
        for idx, turn in enumerate(case.get("turns", []), start=1):
            lines.append(f"Turn {idx} — `{turn['role']}`")
            lines.append("")
            lines.append(block(str(turn["content"])))
            lines.append("")
        lines.extend(["**Harus terlihat**", ""])
        lines.extend(f"- {item}" for item in contract.get("expected_behaviors", []))
        lines.extend(["", "**Tidak boleh terjadi**", ""])
        lines.extend(f"- {item}" for item in contract.get("forbidden_behaviors", []))
        if case.get("judge_notes"):
            lines.extend(["", f"**Catatan reviewer:** {case['judge_notes']}"])
        lines.extend([
            "",
            "**Hasil:** ☐ PASS  ☐ PARTIAL  ☐ FAIL",
            "",
            "**Catatan:**",
            "",
            "________________________________________________________________________",
            "",
        ])

    lines.extend([
        "## Ringkasan",
        "",
        "- PASS: ____",
        "- PARTIAL: ____",
        "- FAIL: ____",
        "- Failure yang perlu dijadikan regression case/perbaikan: ____________________",
        "- Scope/suite tempat fix seharusnya dilakukan: ____________________",
        "",
    ])
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Manual eval kit: {output.relative_to(ROOT)}")
    print(f"Pack {ctx['id']}: {len(cases)} case dari {len(suite_order)} suite ({' -> '.join(suite_order)})")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RepoError as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(2)
