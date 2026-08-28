#!/usr/bin/env python3
"""Cek umur verifikasi source/claim registry dan, opsional, reachability URL."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from datetime import date, datetime
from typing import Any

from ramu_repo import ROOT, RepoError, discover_source_registry_paths, load_json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true", help="Coba akses watched URL dengan request ringan.")
    parser.add_argument("--fail-on-network", action="store_true", help="Exit non-zero bila watched source tidak dapat dijangkau.")
    return parser.parse_args()


def probe(url: str) -> tuple[bool, str]:
    headers = {"User-Agent": "ramu-source-watch/3.0 (+https://github.com/man612/ramu)"}
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return 200 <= response.status < 400, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code not in {403, 405}:
            return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, type(exc).__name__

    fallback = urllib.request.Request(url, headers={**headers, "Range": "bytes=0-1023"}, method="GET")
    try:
        with urllib.request.urlopen(fallback, timeout=20) as response:
            return 200 <= response.status < 400, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, type(exc).__name__


def parsed_age(raw_date: str, today: date) -> int:
    return (today - datetime.strptime(raw_date, "%Y-%m-%d").date()).days


def main() -> int:
    args = parse_args()
    today = date.today()
    overdue_sources: list[tuple[dict[str, Any], int, Any]] = []
    overdue_claims: list[tuple[dict[str, Any], int, Any]] = []
    network_warnings: list[tuple[dict[str, Any], str, Any]] = []
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
            except (KeyError, ValueError, TypeError) as exc:
                print(f"ERROR: metadata freshness tidak valid untuk {sid}: {exc}", file=sys.stderr)
                return 2
            due_in = interval - age
            state = "OK" if due_in >= 0 else "DUE"
            print(f"[{state}] source {sid}: verified {age}d ago; interval {interval}d")
            if due_in < 0 and source.get("status") == "active":
                overdue_sources.append((source, -due_in, rel))
            if args.online and source.get("watch"):
                ok, detail = probe(source["url"])
                if ok:
                    print(f"  URL: {detail}")
                else:
                    network_warnings.append((source, detail, rel))
                    print(f"  URL WARNING: {detail}")

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

    if network_warnings:
        print("\nNetwork warnings (tidak otomatis dianggap fakta berubah):")
        for source, detail, rel in network_warnings:
            print(f"- {source['id']} [{rel}]: {detail}")
    if overdue_sources:
        print("\nSumber aktif yang perlu diverifikasi ulang:")
        for source, late, rel in overdue_sources:
            print(f"- {source['id']} [{rel}] — lewat {late} hari")
    if overdue_claims:
        print("\nClaim yang perlu direview ulang secara semantik:")
        for claim, late, rel in overdue_claims:
            print(f"- {claim['id']} [{rel}] — lewat {late} hari; status {claim.get('status')}")

    if overdue_sources or overdue_claims:
        return 1
    if network_warnings and args.fail_on_network:
        return 2

    print(
        f"\nOK: {source_count} source + {claim_count} claim lintas {len(registries)} registry "
        "masih dalam interval review."
    )
    if network_warnings:
        print("Ada watched source yang perlu dicek reachability-nya; kegagalan jaringan bukan bukti fakta berubah.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
