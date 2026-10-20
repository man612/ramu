#!/usr/bin/env python3
"""Regression test untuk retry dan policy reachability Source Freshness Watch tanpa jaringan."""

from __future__ import annotations

import socket
import sys
import urllib.error
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

        # Default dan scheduled watch tetap memblokir keterlambatan review.
        if freshness.outcome_code(has_overdue=True, has_strict_network_failure=False) != 1:
            raise AssertionError("Overdue dalam mode strict wajib memblokir Source Watch.")
        if freshness.outcome_code(
            has_overdue=True, has_strict_network_failure=False, report_only_overdue=True
        ) != 0:
            raise AssertionError("Overdue dalam mode CI advisory tidak boleh memblokir validation.")
        if freshness.outcome_code(
            has_overdue=True, has_strict_network_failure=True,
            report_only_overdue=True, fail_on_network=True,
        ) != 2:
            raise AssertionError("Network failure strict tetap gagal meskipun review debt advisory.")
        if freshness.outcome_code(has_overdue=False, has_strict_network_failure=False) != 0:
            raise AssertionError("Status bersih wajib sukses.")

        # Probe HEAD yang gagal karena DNS juga mencoba GET agar HEAD-only
        # rejection tidak keliru dianggap link mati. Penyebabnya harus terbaca.
        freshness.probe_once = original_probe_once
        old_urlopen = freshness.urllib.request.urlopen
        methods: list[str] = []

        def dns_failure(request, timeout):
            methods.append(request.get_method())
            raise urllib.error.URLError(socket.gaierror(-2, "hostname not resolved"))

        try:
            freshness.urllib.request.urlopen = dns_failure
            ok, detail = freshness.probe_once("https://example.invalid/test")
        finally:
            freshness.urllib.request.urlopen = old_urlopen
        if ok or methods != ["HEAD", "GET"]:
            raise AssertionError(f"Fallback HEAD->GET saat DNS error rusak: {methods}")
        if detail != "HEAD DNS resolution failure; GET DNS resolution failure":
            raise AssertionError(f"DNS error harus spesifik namun aman: {detail!r}")

        # ThreadPoolExecutor wajib mengembalikan hasil dalam urutan source input
        # supaya warning tetap menunjuk ke source ID yang benar.
        urls = ["one", "two", "three", "four"]
        results = freshness.batch_probe(
            urls, max_workers=2, runner=lambda url: (url in {"one", "three"}, url)
        )
        if results != [(True, "one"), (False, "two"), (True, "three"), (False, "four")]:
            raise AssertionError(f"Batch probe mengacaukan urutan: {results}")
        if freshness.batch_probe([], max_workers=2) != []:
            raise AssertionError("Batch kosong harus valid tanpa jaringan.")
        try:
            freshness.batch_probe(["one"], max_workers=0, runner=lambda url: (True, url))
        except ValueError:
            pass
        else:
            raise AssertionError("Jumlah worker tidak valid harus ditolak.")

        if freshness.reachability_policy({"id": "legacy"}) != "strict":
            raise AssertionError("Source lama tanpa policy harus tetap strict agar kompatibel dan fail-safe.")
        if freshness.reachability_policy({"id": "bot-protected", "reachability_policy": "advisory"}) != "advisory":
            raise AssertionError("Source advisory harus tetap advisory.")
        try:
            freshness.reachability_policy({"id": "invalid", "reachability_policy": "ignore"})
        except ValueError:
            pass
        else:
            raise AssertionError("Policy reachability yang tidak dikenal harus ditolak.")
    finally:
        freshness.probe_once = original_probe_once

    print("Source freshness probe + policy regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
