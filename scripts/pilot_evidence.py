#!/usr/bin/env python3
"""Siapkan dan validasi ringkasan agregat pilot Ramu tanpa data peserta mentah."""

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

SCHEMA = ROOT / "schemas/pilot-summary.schema.json"
PUBLISHED_DIR = ROOT / "evidence/pilots"


class PilotError(RuntimeError):
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


def rate(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 6)


def compute_metrics(data: dict[str, Any]) -> dict[str, float | None]:
    p = data.get("participants") or {}
    return {
        "activation_rate": rate(int(p.get("first_value_reached", 0)), int(p.get("started", 0))),
        "setup_success_rate": rate(int(p.get("setup_completed", 0)), int(p.get("started", 0))),
        "return_7d_rate": rate(int(p.get("returned_within_7d", 0)), int(p.get("return_7d_eligible", 0))),
        "multi_course_adoption_rate": rate(int(p.get("multi_course_adopted", 0)), int(p.get("started", 0))),
        "unassisted_setup_rate": rate(
            int(p.get("setup_completed_without_live_help", 0)), int(p.get("setup_completed", 0))
        ),
    }


def compute_readiness(data: dict[str, Any]) -> dict[str, Any]:
    target = data.get("sample_target") or {}
    p = data.get("participants") or {}
    checks = data.get("protocol_checks") or {}
    sample_minimum_met = int(p.get("started", 0)) >= int(target.get("minimum", 1))
    protocol_valid = all(
        checks.get(field) is True
        for field in (
            "target_population_matches_pack",
            "one_course_first",
            "participant_level_data_excluded",
            "raw_course_material_excluded",
        )
    )
    critical_open = sorted(
        str(item.get("id"))
        for item in data.get("regressions", [])
        if item.get("critical") is True
        and item.get("reproducible") is True
        and item.get("disposition") == "open"
    )

    if data.get("pilot_status") != "completed" or not data.get("pilot_started_at") or not data.get("pilot_ended_at"):
        status = "INCOMPLETE"
        note = "Pilot belum ditutup sebagai completed dengan rentang waktu yang tercatat."
    elif not protocol_valid:
        status = "INCOMPLETE"
        note = "Protocol checks belum cukup untuk menjadikan summary sebagai evidence review-ready."
    elif not sample_minimum_met:
        status = "INSUFFICIENT_SAMPLE"
        note = "Pilot selesai tetapi jumlah peserta yang mulai belum mencapai minimum target yang dideklarasikan."
    elif critical_open:
        status = "BLOCKED"
        note = "Ada regression critical yang reproducible dan masih open."
    else:
        status = "REVIEW_READY"
        note = "Aggregate pilot evidence siap direview manusia; status ini bukan klaim stable atau statistically representative."

    return {
        "status": status,
        "sample_minimum_met": sample_minimum_met,
        "protocol_valid": protocol_valid,
        "open_critical_regressions": critical_open,
        "notes": note,
    }


def build_template(pack_id: str | None, minimum: int, maximum: int) -> dict[str, Any]:
    if minimum < 1 or maximum < minimum:
        raise PilotError("sample target harus minimum >= 1 dan maximum >= minimum.")
    ctx = pack_context(pack_id)
    data: dict[str, Any] = {
        "schema_version": 1,
        "evidence_type": "public-beta-pilot-summary",
        "pack_id": ctx["id"],
        "pack_version": str(ctx["manifest"].get("pack_version", "unknown")),
        "contract_version": str(ctx["manifest"].get("contract_version", "unknown")),
        "ramu_revision": git_revision(),
        "generated_at": now_iso(),
        "pilot_started_at": None,
        "pilot_ended_at": None,
        "pilot_status": "planned",
        "sample_target": {"minimum": minimum, "maximum": maximum},
        "protocol_checks": {
            "target_population_matches_pack": False,
            "one_course_first": False,
            "participant_level_data_excluded": True,
            "raw_course_material_excluded": True,
        },
        "participants": {
            "recruited": 0,
            "started": 0,
            "setup_completed": 0,
            "first_value_reached": 0,
            "return_7d_eligible": 0,
            "returned_within_7d": 0,
            "multi_course_adopted": 0,
            "setup_completed_without_live_help": 0,
        },
        "time_to_first_value": {
            "under_5m": 0,
            "m5_to_15": 0,
            "m15_to_30": 0,
            "over_30m": 0,
            "unknown": 0,
        },
        "setup_failures": [],
        "behavior_failures": [],
        "feedback_themes": [],
        "regressions": [],
        "privacy": {
            "contains_direct_identifiers": False,
            "contains_participant_rows": False,
            "contains_raw_transcripts": False,
            "contains_exact_assignment_content": False,
            "contains_credentials": False,
            "notes": "Hanya simpan agregat dan tema yang sudah disanitasi. Jangan masukkan nama, email, transcript, atau isi tugas mentah.",
        },
        "metrics": {},
        "readiness": {},
        "limitations": [
            "Pilot kecil 5–10 pengguna ditujukan untuk menemukan friction/failure, bukan estimasi statistik populasi.",
            "Hasil terkait pack, periode, product state, dan Ramu revision yang tercatat pada summary ini.",
            "REVIEW_READY berarti evidence cukup untuk review manusia, bukan otomatis stable/validated.",
        ],
    }
    data["metrics"] = compute_metrics(data)
    data["readiness"] = compute_readiness(data)
    return data


def schema_errors(data: dict[str, Any]) -> list[str]:
    schema = load_json(SCHEMA)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        path = "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in error.absolute_path)
        errors.append(f"{path}: {error.message}")
    return errors


def internal_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    target = data.get("sample_target") or {}
    minimum = int(target.get("minimum", 0))
    maximum = int(target.get("maximum", 0))
    if minimum < 1 or maximum < minimum:
        errors.append("sample_target harus minimum >= 1 dan maximum >= minimum.")

    p = data.get("participants") or {}
    names = (
        "recruited",
        "started",
        "setup_completed",
        "first_value_reached",
        "return_7d_eligible",
        "returned_within_7d",
        "multi_course_adopted",
        "setup_completed_without_live_help",
    )
    values = {name: int(p.get(name, 0)) for name in names}
    if values["started"] > values["recruited"]:
        errors.append("participants.started tidak boleh melebihi recruited.")
    if values["setup_completed"] > values["started"]:
        errors.append("setup_completed tidak boleh melebihi started.")
    if values["first_value_reached"] > values["setup_completed"]:
        errors.append("first_value_reached tidak boleh melebihi setup_completed.")
    if values["return_7d_eligible"] > values["started"]:
        errors.append("return_7d_eligible tidak boleh melebihi started.")
    if values["returned_within_7d"] > values["return_7d_eligible"]:
        errors.append("returned_within_7d tidak boleh melebihi return_7d_eligible.")
    if values["multi_course_adopted"] > values["started"]:
        errors.append("multi_course_adopted tidak boleh melebihi started.")
    if values["setup_completed_without_live_help"] > values["setup_completed"]:
        errors.append("setup_completed_without_live_help tidak boleh melebihi setup_completed.")

    buckets = data.get("time_to_first_value") or {}
    bucket_total = sum(int(buckets.get(name, 0)) for name in ("under_5m", "m5_to_15", "m15_to_30", "over_30m", "unknown"))
    if bucket_total != values["first_value_reached"]:
        errors.append(
            "Jumlah bucket time_to_first_value harus sama dengan participants.first_value_reached "
            f"({bucket_total} != {values['first_value_reached']})."
        )

    if data.get("pilot_status") in {"running", "completed"} and not data.get("pilot_started_at"):
        errors.append("pilot_status running/completed membutuhkan pilot_started_at.")
    if data.get("pilot_status") == "completed" and not data.get("pilot_ended_at"):
        errors.append("pilot_status completed membutuhkan pilot_ended_at.")

    ids = [str(item.get("id")) for item in data.get("regressions", [])]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append(f"regression id duplikat: {', '.join(duplicates)}")

    calculated_metrics = compute_metrics(data)
    if data.get("metrics") != calculated_metrics:
        errors.append("metrics tidak cocok hitungan aggregate; jalankan subcommand finalize.")
    calculated_readiness = compute_readiness(data)
    if data.get("readiness") != calculated_readiness:
        errors.append("readiness tidak cocok policy; jalankan subcommand finalize.")
    return errors


def current_repo_warnings(data: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    try:
        ctx = pack_context(data.get("pack_id"))
    except RepoError:
        return ["Pack evidence tidak lagi tersedia di katalog current repo; perlakukan summary sebagai historical snapshot."]

    current_pack = str(ctx["manifest"].get("pack_version"))
    current_contract = str(ctx["manifest"].get("contract_version"))
    if str(data.get("pack_version")) != current_pack:
        warnings.append(f"Historical pack_version {data.get('pack_version')} != current {current_pack}.")
    if str(data.get("contract_version")) != current_contract:
        warnings.append(f"Historical contract_version {data.get('contract_version')} != current {current_contract}.")
    else:
        contracts, _behavior = merged_eval_suite(ctx)
        current_ids = {str(item["id"]).upper() for item in contracts.get("cases", [])}
        unknown_links = sorted(
            {
                str(item.get("linked_eval_case")).upper()
                for item in data.get("regressions", [])
                if item.get("linked_eval_case") and str(item.get("linked_eval_case")).upper() not in current_ids
            }
        )
        if unknown_links:
            warnings.append(f"linked_eval_case tidak ada di current contract: {', '.join(unknown_links)}")
    return warnings


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    return schema_errors(data) + internal_errors(data), current_repo_warnings(data)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_path(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PilotError(f"Tidak dapat membaca pilot evidence JSON {path}: {exc}") from exc


def print_validation(path: Path, data: dict[str, Any]) -> int:
    errors, warnings = validate(data)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print(f"Pilot evidence validation — {len(errors)} error")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Pilot evidence validation — OK: {path} — {data['readiness']['status']}")
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    data = build_template(args.pack, args.minimum, args.maximum)
    output = Path(args.output)
    write_json(output, data)
    return print_validation(output, data)


def cmd_finalize(args: argparse.Namespace) -> int:
    path = Path(args.path)
    data = load_path(path)
    if args.start_now and not data.get("pilot_started_at"):
        data["pilot_started_at"] = now_iso()
        if data.get("pilot_status") == "planned":
            data["pilot_status"] = "running"
    if args.complete_now:
        data["pilot_status"] = "completed"
        data["pilot_ended_at"] = now_iso()
    data["metrics"] = compute_metrics(data)
    data["readiness"] = compute_readiness(data)
    write_json(path, data)
    return print_validation(path, data)


def cmd_validate(args: argparse.Namespace) -> int:
    path = Path(args.path)
    return print_validation(path, load_path(path))


def cmd_validate_published(_args: argparse.Namespace) -> int:
    paths = sorted(PUBLISHED_DIR.glob("*.json")) if PUBLISHED_DIR.is_dir() else []
    failures = 0
    for path in paths:
        failures += 1 if print_validation(path, load_path(path)) else 0
    if failures:
        return 1
    print(f"Published pilot evidence — OK: {len(paths)} summary.")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Kelola aggregate pilot evidence Ramu.")
    sub = root.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare")
    prepare.add_argument("--pack", default=None)
    prepare.add_argument("--minimum", type=int, default=5)
    prepare.add_argument("--maximum", type=int, default=10)
    prepare.add_argument("--output", required=True)
    prepare.set_defaults(func=cmd_prepare)

    finalize = sub.add_parser("finalize")
    finalize.add_argument("path")
    finalize.add_argument("--start-now", action="store_true")
    finalize.add_argument("--complete-now", action="store_true")
    finalize.set_defaults(func=cmd_finalize)

    validate_cmd = sub.add_parser("validate")
    validate_cmd.add_argument("path")
    validate_cmd.set_defaults(func=cmd_validate)

    published = sub.add_parser("validate-published")
    published.set_defaults(func=cmd_validate_published)
    return root


def main() -> int:
    args = parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (PilotError, RepoError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
