#!/usr/bin/env python3
"""Cek umur verifikasi seluruh source registry dan, opsional, reachability URL."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from datetime import date, datetime

from ramu_repo import ROOT, RepoError, discover_source_registry_paths, load_json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true", help="Coba akses watched URL dengan request ringan.")
    parser.add_argument("--fail-on-network", action="store_true", help="Exit non-zero bila watched source tidak dapat dijangkau.")
    return parser.parse_args()


def probe(url: str) -> tuple[bool, str]:
    headers = {"User-Agent": "ramu-source-watch/2.0 (+https://github.com/man612/ramu)"}
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


def main() -> int:
    args = parse_args()
    today = date.today()
    overdue = []
    network_warnings = []
    seen_ids: set[str] = set()
    source_count = 0

    print(f"Source freshness check — {today.isoformat()}")
    try:
        registries = discover_source_registry_paths()
    except RepoError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for registry_path in registries:
        try:
            data = load_json(registry_path)
        except RepoError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        rel = registry_path.relative_to(ROOT)
        print(f"\nRegistry: {rel} [{data.get('scope', 'unknown')}]")
        for source in data.get("sources", []):
            source_count += 1
            sid = source.get("id", "<tanpa-id>")
            if sid in seen_ids:
                print(f"ERROR: source id duplikat lintas registry: {sid}", file=sys.stderr)
                return 2
            seen_ids.add(sid)
            try:
                verified = datetime.strptime(source["verified_at"], "%Y-%m-%d").date()
                interval = int(source["review_interval_days"])
            except (KeyError, ValueError, TypeError) as exc:
                print(f"ERROR: metadata freshness tidak valid untuk {sid}: {exc}", file=sys.stderr)
                return 2
            age = (today - verified).days
            due_in = interval - age
            state = "OK" if due_in >= 0 else "DUE"
            print(f"[{state}] {sid}: verified {age}d ago; interval {interval}d")
            if due_in < 0 and source.get("status") == "active":
                overdue.append((source, -due_in, rel))
            if args.online and source.get("watch"):
                ok, detail = probe(source["url"])
                if ok:
                    print(f"  URL: {detail}")
                else:
                    network_warnings.append((source, detail, rel))
                    print(f"  URL WARNING: {detail}")

    if network_warnings:
        print("\nNetwork warnings (tidak otomatis dianggap fakta berubah):")
        for source, detail, rel in network_warnings:
            print(f"- {source['id']} [{rel}]: {detail}")
    if overdue:
        print("\nSumber aktif yang perlu diverifikasi ulang:")
        for source, late, rel in overdue:
            print(f"- {source['id']} [{rel}] — lewat {late} hari")

    if overdue:
        return 1
    if network_warnings and args.fail_on_network:
        return 2

    print(f"\nOK: {source_count} source lintas {len(registries)} registry masih dalam interval review.")
    if network_warnings:
        print("Ada watched source yang perlu dicek reachability-nya; kegagalan jaringan bukan bukti fakta berubah.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
