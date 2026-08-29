#!/usr/bin/env python3
"""Validasi schema Ramu dan seluruh instance JSON yang menjadi kontrak publik."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

from ramu_repo import (
    PACK_INDEX,
    ROOT,
    RepoError,
    discover_manifest_paths,
    discover_source_registry_paths,
    eval_suite_paths,
    load_json,
    pack_context,
    pack_ids,
)

SCHEMAS = {
    "pack-index": ROOT / "schemas/pack-index.schema.json",
    "pack-manifest": ROOT / "schemas/pack-manifest.schema.json",
    "source-registry": ROOT / "schemas/source-registry.schema.json",
    "eval-cases": ROOT / "schemas/eval-cases.schema.json",
    "eval-behavior": ROOT / "schemas/eval-behavior.schema.json",
    "manual-eval-result": ROOT / "schemas/manual-eval-result.schema.json",
    "pilot-summary": ROOT / "schemas/pilot-summary.schema.json",
}


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def unique_paths(paths: Iterable[Path]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            result.append(path)
    return sorted(result)


def eval_instance_paths() -> tuple[list[Path], list[Path]]:
    contracts: list[Path] = []
    behavior: list[Path] = []
    for pack_id in pack_ids():
        ctx = pack_context(pack_id)
        for _suite, contracts_path, behavior_path in eval_suite_paths(ctx):
            contracts.append(contracts_path)
            behavior.append(behavior_path)
    return unique_paths(contracts), unique_paths(behavior)


def instance_map() -> dict[str, list[Path]]:
    contracts, behavior = eval_instance_paths()
    published_pilots = sorted((ROOT / "evidence/pilots").glob("*.json"))
    return {
        "pack-index": [PACK_INDEX],
        "pack-manifest": discover_manifest_paths(),
        "source-registry": discover_source_registry_paths(),
        "eval-cases": contracts,
        "eval-behavior": behavior,
        # Manual evidence bersifat local/private by default. Generated evidence diuji oleh
        # tests/test_manual_eval_evidence.py; schema tetap diperiksa sebagai Draft 2020-12 di sini.
        "manual-eval-result": [],
        # Hanya summary pilot agregat yang sengaja dipublish ke repository yang divalidasi sebagai instance.
        "pilot-summary": published_pilots,
    }


def location(error) -> str:
    if not error.absolute_path:
        return "$"
    parts: list[str] = ["$"]
    for item in error.absolute_path:
        if isinstance(item, int):
            parts.append(f"[{item}]")
        else:
            parts.append(f".{item}")
    return "".join(parts)


def main() -> int:
    errors: list[str] = []
    try:
        targets = instance_map()
    except RepoError as exc:
        print(f"Schema validation — discovery gagal: {exc}", file=sys.stderr)
        return 2

    schemas: dict[str, dict] = {}
    for name, path in SCHEMAS.items():
        try:
            schema = load_json(path)
            Draft202012Validator.check_schema(schema)
            schemas[name] = schema
        except (RepoError, SchemaError) as exc:
            errors.append(f"schema {relative(path)} tidak valid sebagai Draft 2020-12: {exc}")

    for name, paths in targets.items():
        schema = schemas.get(name)
        if schema is None:
            continue
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for path in paths:
            try:
                instance = load_json(path)
            except RepoError as exc:
                errors.append(str(exc))
                continue
            for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
                errors.append(f"{relative(path)} {location(error)}: {error.message}")

    if errors:
        print(f"JSON Schema validation — {len(errors)} error")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    total = sum(len(paths) for paths in targets.values())
    print(f"JSON Schema validation — OK: {len(SCHEMAS)} schema valid, {total} instance tervalidasi.")
    for name, paths in targets.items():
        print(f"OK {name}: {len(paths)} instance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
