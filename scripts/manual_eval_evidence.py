#!/usr/bin/env python3
"""Siapkan, finalisasi, dan validasi evidence manual ChatGPT Projects tanpa API."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from ramu_repo import ROOT, RepoError, load_json, merged_eval_suite, pack_context

SCHEMA = ROOT / "schemas/manual-eval-result.schema.json"
DEFAULT_FAIL_UNDER = 0.80
CHECK_FIELDS = (
    "project_instructions_confirmed",
    "pack_sources_confirmed",
    "fresh_chat_per_case",
    "protocol_followed_or_deviations_documented",
)
RESULTS = {"PASS", "PARTIAL", "FAIL", "NOT_RUN"}


class EvidenceError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git_revision() -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        value = completed.stdout.strip().lower()
        return value if value else None
    except (OSError, subprocess.CalledProcessError):
        return None


def selected_case_ids(cases: list[dict[str, Any]], only: str) -> list[str]:
    all_ids = [str(case["id"]).upper() for case in cases]
    if not only or only.casefold() == "all":
        return all_ids
    wanted = [item.strip().upper() for item in only.split(",") if item.strip()]
    if not wanted:
        raise EvidenceError("--only kosong. Gunakan all atau daftar seperti E01,E05,E13.")
    duplicates = sorted({cid for cid in wanted if wanted.count(cid) > 1})
    if duplicates:
        raise EvidenceError(f"Case duplikat di --only: {', '.join(duplicates)}")
    unknown = sorted(set(wanted) - set(all_ids))
    if unknown:
        raise EvidenceError(f"Case tidak ditemukan: {', '.join(unknown)}")
    return [cid for cid in all_ids if cid in set(wanted)]


def current_contract(ctx: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    contracts, behavior = merged_eval_suite(ctx)
    contract_by_id = {str(case["id"]).upper(): case for case in contracts.get("cases", [])}
    behavior_by_id = {str(case["id"]).upper(): case for case in behavior.get("cases", [])}
    if set(contract_by_id) != set(behavior_by_id):
        raise EvidenceError("Merged contract/behavior case set tidak sama.")
    return contracts, behavior, contract_by_id, behavior_by_id


def case_record(cid: str, contract: dict[str, Any], behavior: dict[str, Any]) -> dict[str, Any]:
    suite_id = str(behavior.get("suite_id") or contract.get("suite_id") or "unknown")
    return {
        "id": cid,
        "title": str(contract["title"]),
        "suite_id": suite_id,
        "critical": bool(contract.get("critical", False)),
        "result": "NOT_RUN",
        "notes": "",
    }


def compute_overall(data: dict[str, Any], expected_full_ids: set[str]) -> dict[str, Any]:
    cases = data.get("cases", [])
    ids = [str(item.get("id", "")).upper() for item in cases]
    full_case_set = len(ids) == len(expected_full_ids) and set(ids) == expected_full_ids

    counts = {name: 0 for name in RESULTS}
    critical_blockers: list[str] = []
    for item in cases:
        result = str(item.get("result", "NOT_RUN")).upper()
        if result not in RESULTS:
            result = "NOT_RUN"
        counts[result] += 1
        if item.get("critical") and result != "PASS":
            critical_blockers.append(str(item.get("id", "")))

    total = len(cases)
    pass_rate = counts["PASS"] / total if total else 0.0
    validity_blockers: list[str] = []
    if not data.get("tested_at"):
        validity_blockers.append("tested_at_missing")
    setup = data.get("setup_checks") or {}
    for field in CHECK_FIELDS:
        if setup.get(field) is not True:
            validity_blockers.append(field)

    run_scope = str(data.get("run_scope", "subset"))
    fail_under = float((data.get("policy") or {}).get("fail_under", DEFAULT_FAIL_UNDER))

    # Evidence tidak boleh membuat full-validation claim bila harness/setup belum dikonfirmasi,
    # ada case belum dijalankan, atau yang diuji hanya subset.
    if validity_blockers or counts["NOT_RUN"] > 0 or run_scope != "full" or not full_case_set:
        status = "INCOMPLETE"
    elif critical_blockers:
        status = "FAIL"
    elif pass_rate < fail_under:
        status = "FAIL"
    else:
        status = "PASS"

    return {
        "status": status,
        "full_case_set": full_case_set,
        "pass_count": counts["PASS"],
        "partial_count": counts["PARTIAL"],
        "fail_count": counts["FAIL"],
        "not_run_count": counts["NOT_RUN"],
        "pass_rate": round(pass_rate, 6),
        "critical_blockers": sorted(set(critical_blockers)),
        "validity_blockers": sorted(set(validity_blockers)),
    }


def build_template(pack_id: str | None, only: str, fail_under: float) -> dict[str, Any]:
    if not 0 <= fail_under <= 1:
        raise EvidenceError("fail_under harus antara 0 dan 1.")
    ctx = pack_context(pack_id)
    _contracts, behavior, contract_by_id, behavior_by_id = current_contract(ctx)
    all_ids = [str(case["id"]).upper() for case in behavior.get("cases", [])]
    selected = selected_case_ids(behavior.get("cases", []), only)
    run_scope = "full" if selected == all_ids else "subset"

    data: dict[str, Any] = {
        "schema_version": 1,
        "evidence_type": "manual-chatgpt-projects",
        "pack_id": ctx["id"],
        "pack_version": str(ctx["manifest"].get("pack_version", "unknown")),
        "contract_version": str(ctx["manifest"].get("contract_version", "unknown")),
        "ramu_revision": git_revision(),
        "generated_at": now_iso(),
        "tested_at": None,
        "run_scope": run_scope,
        "policy": {
            "fail_under": fail_under,
            "critical_must_pass": True,
            "full_run_required_for_overall_pass": True,
        },
        "runtime": {
            "product": "ChatGPT Projects",
            "plan": "unknown",
            "model_label": "unknown",
            "app_surface": "unknown",
            "app_version": None,
            "project_memory_mode": "unknown",
            "environment_notes": "",
        },
        "setup_checks": {field: False for field in CHECK_FIELDS},
        "privacy": {
            "contains_raw_transcript": False,
            "contains_personal_data": False,
            "contains_credentials": False,
            "notes": "Simpan hanya catatan perilaku yang sudah disanitasi; jangan tempel transcript atau materi tugas mentah.",
        },
        "cases": [case_record(cid, contract_by_id[cid], behavior_by_id[cid]) for cid in selected],
        "overall": {},
        "limitations": [
            "Snapshot manual pada runtime/tanggal tertentu; bukan jaminan perilaku permanen.",
            "ChatGPT Projects product behavior dapat berbeda dari Responses API automated eval.",
        ],
    }
    data["overall"] = compute_overall(data, set(all_ids))
    return data


def schema_errors(data: dict[str, Any]) -> list[str]:
    schema = load_json(SCHEMA)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        path = "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in error.absolute_path)
        errors.append(f"{path}: {error.message}")
    return errors


def semantic_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        ctx = pack_context(data.get("pack_id"))
        _contracts, behavior, contract_by_id, behavior_by_id = current_contract(ctx)
    except (RepoError, EvidenceError) as exc:
        return [str(exc)]

    if str(data.get("pack_version")) != str(ctx["manifest"].get("pack_version")):
        errors.append("pack_version evidence tidak sama dengan manifest saat ini.")
    if str(data.get("contract_version")) != str(ctx["manifest"].get("contract_version")):
        errors.append("contract_version evidence tidak sama dengan manifest saat ini.")

    expected_ids = {str(case["id"]).upper() for case in behavior.get("cases", [])}
    seen: set[str] = set()
    for item in data.get("cases", []):
        cid = str(item.get("id", "")).upper()
        if cid in seen:
            errors.append(f"case evidence duplikat: {cid}")
            continue
        seen.add(cid)
        if cid not in expected_ids:
            errors.append(f"case evidence tidak ada di contract saat ini: {cid}")
            continue
        contract = contract_by_id[cid]
        behavior_case = behavior_by_id[cid]
        expected_suite = str(behavior_case.get("suite_id") or contract.get("suite_id") or "unknown")
        if item.get("title") != contract.get("title"):
            errors.append(f"{cid}: title evidence drift dari contract.")
        if str(item.get("suite_id")) != expected_suite:
            errors.append(f"{cid}: suite_id evidence {item.get('suite_id')} != {expected_suite}.")
        if bool(item.get("critical")) != bool(contract.get("critical", False)):
            errors.append(f"{cid}: critical flag evidence drift dari contract.")

    run_scope = data.get("run_scope")
    is_full = seen == expected_ids and len(seen) == len(expected_ids)
    if run_scope == "full" and not is_full:
        errors.append("run_scope=full tetapi evidence tidak mencakup seluruh case contract saat ini.")
    if run_scope == "subset" and is_full:
        errors.append("run_scope=subset tetapi evidence ternyata mencakup seluruh case; gunakan full.")

    calculated = compute_overall(data, expected_ids)
    if data.get("overall") != calculated:
        errors.append("overall evidence tidak cocok hasil perhitungan; jalankan subcommand finalize.")
    return errors


def validate(data: dict[str, Any]) -> list[str]:
    return schema_errors(data) + semantic_errors(data)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_prepare(args: argparse.Namespace) -> int:
    data = build_template(args.pack, args.only, args.fail_under)
    output = Path(args.output)
    write_json(output, data)
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Manual evidence template: {output}")
    print(f"Scope: {data['run_scope']} — {len(data['cases'])} case — status awal INCOMPLETE")
    return 0


def cmd_finalize(args: argparse.Namespace) -> int:
    path = Path(args.path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"Tidak dapat membaca evidence JSON: {exc}") from exc
    if args.tested_at_now and not data.get("tested_at"):
        data["tested_at"] = now_iso()
    try:
        ctx = pack_context(data.get("pack_id"))
        _contracts, behavior, _contract_by_id, _behavior_by_id = current_contract(ctx)
    except (RepoError, EvidenceError) as exc:
        raise EvidenceError(str(exc)) from exc
    expected_ids = {str(case["id"]).upper() for case in behavior.get("cases", [])}
    data["overall"] = compute_overall(data, expected_ids)
    write_json(path, data)
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Evidence finalized: {path}")
    print(f"Overall: {data['overall']['status']} — pass rate {data['overall']['pass_rate']:.1%}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    path = Path(args.path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"Tidak dapat membaca evidence JSON: {exc}") from exc
    errors = validate(data)
    if errors:
        print(f"Manual evidence validation — {len(errors)} error")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        f"Manual evidence validation — OK: {data['pack_id']} — {len(data['cases'])} case — "
        f"{data['overall']['status']}"
    )
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Kelola evidence manual ChatGPT Projects Ramu.")
    sub = root.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="Buat JSON evidence template dari merged eval contract.")
    prepare.add_argument("--pack", default=None)
    prepare.add_argument("--only", default="all")
    prepare.add_argument("--fail-under", type=float, default=DEFAULT_FAIL_UNDER)
    prepare.add_argument("--output", required=True)
    prepare.set_defaults(func=cmd_prepare)

    finalize = sub.add_parser("finalize", help="Hitung ulang overall dan validasi evidence yang sudah diisi.")
    finalize.add_argument("path")
    finalize.add_argument("--tested-at-now", action="store_true")
    finalize.set_defaults(func=cmd_finalize)

    validate_cmd = sub.add_parser("validate", help="Validasi schema + contract consistency tanpa mengubah file.")
    validate_cmd.add_argument("path")
    validate_cmd.set_defaults(func=cmd_validate)
    return root


def main() -> int:
    args = parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (EvidenceError, RepoError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
