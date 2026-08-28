#!/usr/bin/env python3
"""Cek umur verifikasi sumber dan, opsional, reachability URL."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sources/registry.json"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true", help="Coba akses URL dengan request ringan.")
    parser.add_argument(
        "--fail-on-network",
        action="store_true",
        help="Kembalikan exit code non-zero bila watched source tidak dapat dijangkau.",
    )
    return parser.parse_args()


def probe(url: str) -> tuple[bool, str]:
    headers = {"User-Agent": "ramu-source-watch/1.0 (+https://github.com/man612/ramu)"}
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return 200 <= response.status < 400, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code not in {403, 405}:
            return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, type(exc).__name__

    fallback = urllib.request.Request(
        url,
        headers={**headers, "Range": "bytes=0-1023"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(fallback, timeout=20) as response:
            return 200 <= response.status < 400, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, type(exc).__name__


def main() -> int:
    args = parse_args()
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    today = date.today()
    overdue = []
    network_warnings = []

    print(f"Source freshness check — {today.isoformat()}")
    for source in data["sources"]:
        verified = datetime.strptime(source["verified_at"], "%Y-%m-%d").date()
        age = (today - verified).days
        interval = source["review_interval_days"]
        due_in = interval - age

        state = "OK" if due_in >= 0 else "DUE"
        print(f"[{state}] {source['id']}: verified {age}d ago; interval {interval}d")

        if due_in < 0 and source["status"] == "active":
            overdue.append((source, -due_in))

        if args.online and source.get("watch"):
            ok, detail = probe(source["url"])
            if ok:
                print(f"  URL: {detail}")
            else:
                network_warnings.append((source, detail))
                print(f"  URL WARNING: {detail}")

    if network_warnings:
        print("\nNetwork warnings (tidak otomatis dianggap fakta berubah):")
        for source, detail in network_warnings:
            print(f"- {source['id']}: {detail}")

    if overdue:
        print("\nSumber aktif yang perlu diverifikasi ulang:")
        for source, late in overdue:
            print(f"- {source['id']} — lewat {late} hari")

    if overdue:
        return 1
    if network_warnings and args.fail_on_network:
        return 2

    print("\nSemua sumber aktif masih dalam interval review.")
    if network_warnings:
        print("Ada watched source yang perlu dicek reachability-nya; jalankan dengan --fail-on-network untuk menjadikannya gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
