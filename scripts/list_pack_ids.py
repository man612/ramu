#!/usr/bin/env python3
"""Cetak pack id Ramu untuk shell atau GitHub Actions matrix."""

from __future__ import annotations

import argparse
import json
import sys

from ramu_repo import RepoError, pack_ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", action="store_true")
    args = parser.parse_args()
    ids = pack_ids()
    if args.matrix:
        print(json.dumps({"pack": ids}, separators=(",", ":")))
    else:
        print("\n".join(ids))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RepoError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
