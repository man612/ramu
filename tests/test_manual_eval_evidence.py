#!/usr/bin/env python3
"""Regression proof untuk evidence manual ChatGPT Projects tanpa API."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from manual_eval_evidence import build_template, compute_overall, current_contract, validate  # noqa: E402
from ramu_repo import pack_context  # noqa: E402


def ready(data: dict) -> None:
    data["tested_at"] = "2026-08-29T00:00:00Z"
    data["runtime"]["plan"] = "Plus"
    data["runtime"]["model_label"] = "visible-model-label"
    data["runtime"]["app_surface"] = "web"
    data["runtime"]["project_memory_mode"] = "project-only"
    for key in data["setup_checks"]:
        data["setup_checks"][key] = True


def recalc(data: dict) -> None:
    ctx = pack_context(data["pack_id"])
    _contracts, behavior, _contract_by_id, _behavior_by_id = current_contract(ctx)
    expected_ids = {case["id"].upper() for case in behavior["cases"]}
    data["overall"] = compute_overall(data, expected_ids)


def main() -> int:
    template = build_template(None, "all", 0.80)
    if template["run_scope"] != "full" or template["overall"]["status"] != "INCOMPLETE":
        raise AssertionError("Template full-run wajib dimulai INCOMPLETE.")
    if not template["overall"]["full_case_set"]:
        raise AssertionError("Template all harus mencakup full case set.")
    if validate(template):
        raise AssertionError(f"Template generated harus valid: {validate(template)}")

    healthy = copy.deepcopy(template)
    ready(healthy)
    for case in healthy["cases"]:
        case["result"] = "PASS"
    recalc(healthy)
    if healthy["overall"]["status"] != "PASS" or healthy["overall"]["pass_rate"] != 1.0:
        raise AssertionError(f"Full manual run sehat harus PASS: {healthy['overall']}")
    if validate(healthy):
        raise AssertionError(f"Full PASS evidence harus valid: {validate(healthy)}")

    critical_failure = copy.deepcopy(healthy)
    critical_case = next(case for case in critical_failure["cases"] if case["critical"])
    critical_case["result"] = "FAIL"
    recalc(critical_failure)
    if critical_failure["overall"]["status"] != "FAIL":
        raise AssertionError("Satu critical FAIL harus menggagalkan full manual run.")
    if critical_case["id"] not in critical_failure["overall"]["critical_blockers"]:
        raise AssertionError("Critical failure harus tercatat sebagai blocker.")

    subset = build_template(None, "E01,E05", 0.80)
    ready(subset)
    for case in subset["cases"]:
        case["result"] = "PASS"
    recalc(subset)
    if subset["overall"]["status"] != "INCOMPLETE" or subset["overall"]["full_case_set"]:
        raise AssertionError("Subset yang semuanya PASS tetap tidak boleh menjadi full-validation PASS.")

    tampered = copy.deepcopy(healthy)
    tampered["cases"][0]["critical"] = not tampered["cases"][0]["critical"]
    recalc(tampered)
    errors = validate(tampered)
    if not any("critical flag evidence drift" in error for error in errors):
        raise AssertionError(f"Tampered critical metadata harus ditolak: {errors}")

    unsafe = copy.deepcopy(healthy)
    unsafe["privacy"]["contains_raw_transcript"] = True
    errors = validate(unsafe)
    if not any("contains_raw_transcript" in error for error in errors):
        raise AssertionError(f"Evidence yang mengaku menyimpan raw transcript harus ditolak schema: {errors}")

    workflow = (ROOT / ".github/workflows/manual-eval-kit.yml").read_text(encoding="utf-8")
    for marker in (
        "scripts/manual_eval_evidence.py prepare",
        "scripts/manual_eval_evidence.py validate",
        "evals/results/manual-evidence.json",
        "evals/results/manual-checklist.md",
    ):
        if marker not in workflow:
            raise AssertionError(f"Manual Eval Kit kehilangan evidence wiring: {marker}")

    print("Manual Projects evidence regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
