#!/usr/bin/env python3
"""Regression test untuk retry reachability Source Freshness Watch tanpa akses jaringan."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_source_freshness as freshness  # noqa: E402


def main() -> int:
    original_probe_once = freshness.probe_once
    try:
        calls: list[str] = []
        delays: list[float] = []
        outcomes = iter([
            (False, "TimeoutError"),
            (False, "HTTP 503"),
            (True, "HTTP 200"),
        ])

        def flaky_probe(url: str) -> tuple[bool, str]:
            calls.append(url)
            return next(outcomes)

        freshness.probe_once = flaky_probe
        ok, detail = freshness.probe(
            "https://example.invalid/flaky",
            attempts=3,
            sleep_fn=delays.append,
        )
        if not ok:
            raise AssertionError(f"Probe flaky seharusnya pulih pada attempt ketiga: {detail}")
        if detail != "HTTP 200 (attempt 3/3)":
            raise AssertionError(f"Detail retry tidak sesuai: {detail!r}")
        if len(calls) != 3 or delays != [1, 3]:
            raise AssertionError(f"Retry contract berubah: calls={len(calls)}, delays={delays}")

        persistent_calls = 0
        persistent_delays: list[float] = []

        def persistent_failure(url: str) -> tuple[bool, str]:
            nonlocal persistent_calls
            persistent_calls += 1
            return False, "HTTP 503"

        freshness.probe_once = persistent_failure
        ok, detail = freshness.probe(
            "https://example.invalid/down",
            attempts=3,
            sleep_fn=persistent_delays.append,
        )
        if ok:
            raise AssertionError("Persistent failure tidak boleh dianggap reachable.")
        if detail != "HTTP 503 after 3 attempts":
            raise AssertionError(f"Final failure detail tidak sesuai: {detail!r}")
        if persistent_calls != 3 or persistent_delays != [1, 3]:
            raise AssertionError(
                f"Persistent retry contract berubah: calls={persistent_calls}, delays={persistent_delays}"
            )

        freshness.probe_once = lambda url: (True, "HTTP 204")
        no_retry_delays: list[float] = []
        ok, detail = freshness.probe(
            "https://example.invalid/ok",
            attempts=3,
            sleep_fn=no_retry_delays.append,
        )
        if not ok or detail != "HTTP 204" or no_retry_delays:
            raise AssertionError("Successful first probe seharusnya tidak melakukan retry.")
    finally:
        freshness.probe_once = original_probe_once

    print("Source freshness probe retry regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
