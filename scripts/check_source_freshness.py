#!/usr/bin/env python3
"""Cek umur verifikasi source/claim registry dan, opsional, reachability URL."""

from __future__ import annotations

import argparse
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from typing import Any, Callable

from ramu_repo import ROOT, RepoError, discover_source_registry_paths, load_json

PROBE_ATTEMPTS = 3
PROBE_RETRY_DELAYS = (1, 3)
REACHABILITY_POLICIES = {"strict", "advisory"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true", help="Coba akses watched URL dengan request ringan.")
    parser.add_argument(
        "--report-only-overdue",
        action="store_true",
        help="Laporkan source/claim overdue tanpa memblokir CI; metadata invalid tetap gagal. Scheduled watch tetap strict.",
    )
    parser.add_argument(
        "--fail-on-network",
        action="store_true",
        help="Exit non-zero bila watched source berpolicy strict tetap tidak dapat dijangkau setelah retry.",
    )
    return parser.parse_args()


def probe_error_detail(exc: urllib.error.URLError) -> str:
    """Ringkas sebab kegagalan tanpa mencetak URL, token, atau pesan jaringan mentah."""
    reason = exc.reason
    if isinstance(reason, socket.gaierror):
        return "DNS resolution failure"
    if isinstance(reason, ssl.SSLError):
        return "TLS handshake/certificate failure"
    if isinstance(reason, (TimeoutError, socket.timeout)):
        return "network timeout"
    if isinstance(reason, ConnectionRefusedError):
        return "connection refused"
    if isinstance(reason, ConnectionResetError):
        return "connection reset"
    return f"URLError ({type(reason).__name__})"


def probe_once(url: str) -> tuple[bool, str]:
    headers = {"User-Agent": "ramu-source-watch/3.2 (+https://github.com/man612/ramu)"}
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return 200 <= response.status < 400, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code not in {403, 405}:
            return False, f"HTTP {exc.code}"
        head_detail = f"HEAD HTTP {exc.code}"
    except urllib.error.URLError as exc:
        # Beberapa origin memutus koneksi untuk HEAD tetapi tetap melayani GET.
        head_detail = f"HEAD {probe_error_detail(exc)}"
    except Exception as exc:
        return False, type(exc).__name__

    fallback = urllib.request.Request(url, headers={**headers, "Range": "bytes=0-1023"}, method="GET")
    try:
        with urllib.request.urlopen(fallback, timeout=20) as response:
            return 200 <= response.status < 400, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return False, f"{head_detail}; GET {probe_error_detail(exc)}"
    except Exception as exc:
        return False, f"{head_detail}; GET {type(exc).__name__}"


def probe(
    url: str,
    *,
    attempts: int = PROBE_ATTEMPTS,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> tuple[bool, str]:
    if attempts < 1:
        raise ValueError("attempts harus >= 1")

    last_detail = "unknown"
    for attempt in range(1, attempts + 1):
        ok, detail = probe_once(url)
        if ok:
            if attempt == 1:
                return True, detail
            return True, f"{detail} (attempt {attempt}/{attempts})"

        last_detail = detail
        if attempt < attempts:
            delay_index = min(attempt - 1, len(PROBE_RETRY_DELAYS) - 1)
            sleep_fn(PROBE_RETRY_DELAYS[delay_index])

    return False, f"{last_detail} after {attempts} attempts"


def batch_probe(
    urls: list[str],
    *,
    max_workers: int = 3,
    runner: Callable[[str], tuple[bool, str]] = probe,
) -> list[tuple[bool, str]]:
    """Batasi probe paralel; hasil mengikuti urutan input demi diagnostics deterministik."""
    if max_workers < 1:
        raise ValueError("max_workers harus >= 1")
    if not urls:
        return []
    with ThreadPoolExecutor(max_workers=min(max_workers, len(urls))) as pool:
        return list(pool.map(runner, urls))


def reachability_policy(source: dict[str, Any]) -> str:
    """Return policy source; legacy entries default ke strict."""
    policy = str(source.get("reachability_policy", "strict")).strip().lower()
    if policy not in REACHABILITY_POLICIES:
        sid = source.get("id", "<tanpa-id>")
        raise ValueError(f"reachability_policy tidak valid untuk {sid}: {policy!r}")
    return policy


def parsed_age(raw_date: str, today: date) -> int:
    return (today - datetime.strptime(raw_date, "%Y-%m-%d").date()).days


def outcome_code(
    *, has_overdue: bool, has_strict_network_failure: bool,
    report_only_overdue: bool = False, fail_on_network: bool = False,
) -> int:
    """Pisahkan review debt dari error metadata dan kegagalan probe strict."""
    if has_overdue and not report_only_overdue:
        return 1
    if has_strict_network_failure and fail_on_network:
        return 2
    return 0


def main() -> int:
    args = parse_args()
    today = date.today()
    overdue_sources: list[tuple[dict[str, Any], int, Any]] = []
    overdue_claims: list[tuple[dict[str, Any], int, Any]] = []
    network_failures: list[tuple[dict[str, Any], str, Any]] = []
    network_advisories: list[tuple[dict[str, Any], str, Any]] = []
    watched_sources: list[tuple[dict[str, Any], str, Any]] = []
    seen_ids: set[str] = set()
    seen_claim_ids: set[str] = set()
    source_map: dict[str, tuple[dict[str, Any], Any]] = {}
    source_count = 0
    claim_count = 0

    print(f"Source freshness check — {today.isoformat()}")
    try:
        registry_paths = discover_source_registry_paths()
        registries = [(path, load_json(path)) for path in registry_paths]
    except RepoError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    # Pass 1: sumber fisik/URL. Claim evidence divalidasi setelah seluruh source ID diketahui.
    for registry_path, data in registries:
        rel = registry_path.relative_to(ROOT)
        print(f"\nRegistry: {rel} [{data.get('scope', 'unknown')}]")
        for source in data.get("sources", []):
            source_count += 1
            sid = source.get("id", "<tanpa-id>")
            if sid in seen_ids:
                print(f"ERROR: source id duplikat lintas registry: {sid}", file=sys.stderr)
                return 2
            seen_ids.add(sid)
            source_map[sid] = (source, rel)
            try:
                age = parsed_age(source["verified_at"], today)
                interval = int(source["review_interval_days"])
                policy = reachability_policy(source)
            except (KeyError, ValueError, TypeError) as exc:
                print(f"ERROR: metadata freshness tidak valid untuk {sid}: {exc}", file=sys.stderr)
                return 2
            due_in = interval - age
            state = "OK" if due_in >= 0 else "DUE"
            print(f"[{state}] source {sid}: verified {age}d ago; interval {interval}d")
            if due_in < 0 and source.get("status") == "active":
                overdue_sources.append((source, -due_in, rel))
            if args.online and source.get("watch"):
                watched_sources.append((source, policy, rel))

    # Pass 2: semantic claims. Reachability tidak cukup untuk membuktikan claim masih benar.
    for registry_path, data in registries:
        rel = registry_path.relative_to(ROOT)
        for claim in data.get("claims", []):
            claim_count += 1
            cid = claim.get("id", "<tanpa-id>")
            if cid in seen_claim_ids:
                print(f"ERROR: claim id duplikat lintas registry: {cid}", file=sys.stderr)
                return 2
            seen_claim_ids.add(cid)
            try:
                age = parsed_age(claim["reviewed_at"], today)
                interval = int(claim["review_interval_days"])
            except (KeyError, ValueError, TypeError) as exc:
                print(f"ERROR: metadata freshness claim tidak valid untuk {cid}: {exc}", file=sys.stderr)
                return 2

            evidence = claim.get("evidence", [])
            missing_sources = sorted({item.get("source_id") for item in evidence if item.get("source_id") not in source_map})
            if missing_sources:
                print(
                    f"ERROR: claim {cid} mereferensikan source id yang tidak ada: {', '.join(str(x) for x in missing_sources)}",
                    file=sys.stderr,
                )
                return 2
            if claim.get("status") == "conflicted" and not str(claim.get("operational_policy", "")).strip():
                print(f"ERROR: claim conflicted {cid} wajib punya operational_policy.", file=sys.stderr)
                return 2

            due_in = interval - age
            freshness = "OK" if due_in >= 0 else "DUE"
            status = str(claim.get("status", "unknown")).upper()
            print(f"[{freshness}] claim {cid}: {status}; reviewed {age}d ago; interval {interval}d")
            if due_in < 0 and claim.get("status") != "deprecated":
                overdue_claims.append((claim, -due_in, rel))

    # Jalan setelah metadata/claim tervalidasi, agar request jaringan tidak mubazir
    # ketika kontrak registry sendiri salah.
    if watched_sources:
        print(f"\nURL reachability ({len(watched_sources)} watched sources, maksimal 3 worker):")
        try:
            results = batch_probe([source["url"] for source, _, _ in watched_sources])
        except Exception as exc:
            print(f"ERROR: online probe gagal secara internal: {type(exc).__name__}", file=sys.stderr)
            return 2
        for (source, policy, rel), (ok, detail) in zip(watched_sources, results):
            sid = source["id"]
            if ok:
                print(f"  [OK] {sid} [{rel}]: {detail}")
            elif policy == "advisory":
                network_advisories.append((source, detail, rel))
                print(f"  [INCONCLUSIVE] {sid} [{rel}]: {detail} (policy advisory)")
            else:
                network_failures.append((source, detail, rel))
                print(f"  [WARNING] {sid} [{rel}]: {detail} (policy strict)")

    if network_advisories:
        print("\nReachability inconclusive (signal saja; tidak membuat watch gagal):")
        for source, detail, rel in network_advisories:
            print(f"- {source['id']} [{rel}]: {detail}")
    if network_failures:
        print("\nNetwork warnings yang perlu ditinjau:")
        for source, detail, rel in network_failures:
            print(f"- {source['id']} [{rel}]: {detail}")
    if overdue_sources:
        print("\nSumber aktif yang perlu diverifikasi ulang:")
        for source, late, rel in overdue_sources:
            print(f"- {source['id']} [{rel}] — lewat {late} hari")
    if overdue_claims:
        print("\nClaim yang perlu direview ulang secara semantik:")
        for claim, late, rel in overdue_claims:
            print(f"- {claim['id']} [{rel}] — lewat {late} hari; status {claim.get('status')}")

    exit_code = outcome_code(
        has_overdue=bool(overdue_sources or overdue_claims),
        has_strict_network_failure=bool(network_failures),
        report_only_overdue=args.report_only_overdue,
        fail_on_network=args.fail_on_network,
    )
    if exit_code:
        return exit_code

    if overdue_sources or overdue_claims:
        print(
            "\nREVIEW REQUIRED (non-blocking for this run): source/claim overdue. "
            "Scheduled Source Watch tetap wajib meminta review; tidak ada tanggal yang diperpanjang otomatis."
        )
    else:
        print(
            f"\nOK: {source_count} source + {claim_count} claim lintas {len(registries)} registry "
            "masih dalam interval review."
        )
    if network_advisories:
        print("Ada source advisory yang probe otomatisnya inconclusive; freshness semantik tetap mengikuti review evidence.")
    if network_failures:
        print("Ada watched source strict yang perlu dicek reachability-nya; kegagalan jaringan bukan bukti fakta berubah.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
