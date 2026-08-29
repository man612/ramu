#!/usr/bin/env python3
"""Regression proof untuk aggregate pilot evidence yang privacy-safe."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from pilot_evidence import build_template, compute_metrics, compute_readiness, validate  # noqa: E402


def finalize(data: dict) -> None:
    data["metrics"] = compute_metrics(data)
    data["readiness"] = compute_readiness(data)


def healthy_summary() -> dict:
    data = build_template(None, 5, 10)
    data["pilot_started_at"] = "2026-08-29T01:00:00Z"
    data["pilot_ended_at"] = "2026-09-05T01:00:00Z"
    data["pilot_status"] = "completed"
    data["protocol_checks"]["target_population_matches_pack"] = True
    data["protocol_checks"]["one_course_first"] = True
    data["participants"].update(
        {
            "recruited": 6,
            "started": 5,
            "setup_completed": 5,
            "first_value_reached": 5,
            "return_7d_eligible": 5,
            "returned_within_7d": 4,
            "multi_course_adopted": 2,
            "setup_completed_without_live_help": 4,
        }
    )
    data["time_to_first_value"].update(
        {"under_5m": 1, "m5_to_15": 3, "m15_to_30": 1, "over_30m": 0, "unknown": 0}
    )
    data["feedback_themes"] = [
        {
            "theme": "setup clarity",
            "sentiment": "positive",
            "mentions": 4,
            "summary": "Mayoritas tester dapat menyelesaikan setup satu mata kuliah tanpa bantuan langsung.",
        }
    ]
    finalize(data)
    return data


def main() -> int:
    template = build_template(None, 5, 10)
    errors, _warnings = validate(template)
    if errors:
        raise AssertionError(f"Template pilot generated harus valid: {errors}")
    if template["readiness"]["status"] != "INCOMPLETE":
        raise AssertionError("Template baru wajib dimulai sebagai INCOMPLETE.")

    healthy = healthy_summary()
    errors, warnings = validate(healthy)
    if errors:
        raise AssertionError(f"Healthy pilot summary harus valid: {errors}")
    if warnings:
        raise AssertionError(f"Healthy current-repo pilot tidak seharusnya warning: {warnings}")
    if healthy["readiness"]["status"] != "REVIEW_READY":
        raise AssertionError(f"Healthy completed pilot harus REVIEW_READY: {healthy['readiness']}")
    if healthy["readiness"]["status"] == "PASS":
        raise AssertionError("Pilot tooling tidak boleh punya semantic PASS/stable otomatis.")

    critical = copy.deepcopy(healthy)
    critical["regressions"] = [
        {
            "id": "P001",
            "category": "fabrication",
            "critical": True,
            "reproducible": True,
            "linked_eval_case": "E01",
            "disposition": "open",
            "notes": "Sanitized reproduction menunjukkan model menebak angka yang tidak terlihat.",
        }
    ]
    finalize(critical)
    errors, _warnings = validate(critical)
    if errors:
        raise AssertionError(f"Critical regression summary harus valid structurally: {errors}")
    if critical["readiness"]["status"] != "BLOCKED":
        raise AssertionError("Open reproducible critical regression harus BLOCKED.")
    if critical["readiness"]["open_critical_regressions"] != ["P001"]:
        raise AssertionError("Critical blocker ID harus tercatat eksplisit.")

    insufficient = healthy_summary()
    insufficient["participants"].update(
        {
            "recruited": 4,
            "started": 4,
            "setup_completed": 4,
            "first_value_reached": 4,
            "return_7d_eligible": 4,
            "returned_within_7d": 3,
            "multi_course_adopted": 1,
            "setup_completed_without_live_help": 3,
        }
    )
    insufficient["time_to_first_value"].update(
        {"under_5m": 1, "m5_to_15": 2, "m15_to_30": 1, "over_30m": 0, "unknown": 0}
    )
    finalize(insufficient)
    errors, _warnings = validate(insufficient)
    if errors:
        raise AssertionError(f"Insufficient sample tetap harus valid evidence: {errors}")
    if insufficient["readiness"]["status"] != "INSUFFICIENT_SAMPLE":
        raise AssertionError("Pilot di bawah minimum sample harus INSUFFICIENT_SAMPLE.")

    broken_protocol = healthy_summary()
    broken_protocol["protocol_checks"]["target_population_matches_pack"] = False
    finalize(broken_protocol)
    errors, _warnings = validate(broken_protocol)
    if errors:
        raise AssertionError(f"Protocol-failed summary tetap boleh structurally valid: {errors}")
    if broken_protocol["readiness"]["status"] != "INCOMPLETE":
        raise AssertionError("Protocol invalid tidak boleh REVIEW_READY.")

    tampered_metrics = healthy_summary()
    tampered_metrics["metrics"]["activation_rate"] = 0.123456
    errors, _warnings = validate(tampered_metrics)
    if not any("metrics tidak cocok" in error for error in errors):
        raise AssertionError(f"Metrik yang dimanipulasi harus ditolak: {errors}")

    unsafe = healthy_summary()
    unsafe["privacy"]["contains_raw_transcripts"] = True
    errors, _warnings = validate(unsafe)
    if not any("contains_raw_transcripts" in error for error in errors):
        raise AssertionError(f"Pilot evidence dengan raw transcript harus ditolak schema: {errors}")

    bad_counts = healthy_summary()
    bad_counts["participants"]["first_value_reached"] = 6
    finalize(bad_counts)
    errors, _warnings = validate(bad_counts)
    if not any("first_value_reached tidak boleh melebihi setup_completed" in error for error in errors):
        raise AssertionError(f"Impossible participant funnel harus ditolak: {errors}")

    print("Pilot aggregate evidence regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
