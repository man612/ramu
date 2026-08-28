#!/usr/bin/env python3
"""Regression tests untuk overall pass-rate + critical must-pass gate tanpa API."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_behavior_evals import evaluate_overall  # noqa: E402


def item(cid: str, passed: bool, critical: bool = False) -> dict:
    return {"id": cid, "passed": passed, "critical": critical}


def main() -> int:
    # 13/16 = 81.25% seharusnya melewati threshold 80%, tetapi critical failure wajib menggagalkan run.
    with_critical_failure = [item(f"E{i:02}", True) for i in range(1, 17)]
    with_critical_failure[0] = item("E01", False, critical=True)
    with_critical_failure[1] = item("E02", False)
    with_critical_failure[2] = item("E03", False)
    overall, rate, critical = evaluate_overall(with_critical_failure, 0.80)
    if round(rate, 4) != 0.8125:
        raise AssertionError(f"Expected pass rate 0.8125, got {rate}")
    if overall:
        raise AssertionError("Critical FAIL harus menggagalkan overall meski pass rate > threshold")
    if critical != ["E01"]:
        raise AssertionError(f"Critical failure list salah: {critical}")

    # Pass rate yang sama boleh lulus bila kegagalan hanya non-critical.
    noncritical_failures = [item(f"E{i:02}", True) for i in range(1, 17)]
    noncritical_failures[1] = item("E02", False)
    noncritical_failures[2] = item("E03", False)
    noncritical_failures[3] = item("E04", False)
    overall, rate, critical = evaluate_overall(noncritical_failures, 0.80)
    if not overall or critical:
        raise AssertionError("13/16 non-critical failures seharusnya lulus threshold 80%")

    # Critical case yang lulus tidak memblokir overall.
    healthy = [item("E01", True, critical=True), item("E05", True, critical=True), item("E06", True)]
    overall, rate, critical = evaluate_overall(healthy, 0.80)
    if not overall or rate != 1.0 or critical:
        raise AssertionError("Run sehat dengan semua critical PASS harus lulus")

    print("Critical eval gate regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
