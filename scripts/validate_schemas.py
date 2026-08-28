#!/usr/bin/env python3
"""Validasi schema Draft 2020-12 dan seluruh JSON instance utama Ramu."""

from __future__ import annotations

import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

from ramu_repo import (
    PACK_INDEX,
    ROOT,
    RepoError,
    discover_manifest_paths,
    discover_source_registry_paths,
    load_json,
)


SCHEMAS = {
    "pack-index": ROOT / "schemas/pack-index.schema.json",
    "pack-manifest": ROOT / "schemas/pack-manifest.schema.json",
    "source-registry": ROOT / "schemas/source-registry.schema.json",
    "eval-contract": ROOT / "schemas/eval-cases.schema.json",
    "eval-behavior": ROOT / "schemas/eval-behavior.schema.json",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def eval_paths(filename: str) -> list[Path]:
    paths = set(ROOT.glob(f"evals/**/{filename}"))
    paths.update(ROOT.glob(f"packs/**/evals/{filename}"))
    return sorted(paths)


def targets() -> list[tuple[str, Path, list[Path]]]:
    return [
        ("pack-index", SCHEMAS["pack-index"], [PACK_INDEX]),
        ("pack-manifest", SCHEMAS["pack-manifest"], discover_manifest_paths()),
        ("source-registry", SCHEMAS["source-registry"], discover_source_registry_paths()),
        ("eval-contract", SCHEMAS["eval-contract"], eval_paths("contracts.json")),
        ("eval-behavior", SCHEMAS["eval-behavior"], eval_paths("behavior.json")),
    ]


def error_path(error) -> str:
    if not error.absolute_path:
        return "$"
    return "$" + "".join(f"[{item}]" if isinstance(item, int) else f".{item}" for item in error.absolute_path)


def main() -> int:
    failures: list[str] = []
    instance_count = 0

    for label, schema_path, instances in targets():
        try:
            schema = load_json(schema_path)
            Draft202012Validator.check_schema(schema)
        except (RepoError, SchemaError) as exc:
            failures.append(f"Schema {rel(schema_path)} invalid: {exc}")
            continue

        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        if not instances:
            failures.append(f"Tidak ada instance ditemukan untuk schema {label}.")
            continue

        for instance_path in instances:
            instance_count += 1
            try:
                instance = load_json(instance_path)
            except RepoError as exc:
                failures.append(str(exc))
                continue
            errors = sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
            for error in errors:
                failures.append(f"{rel(instance_path)} {error_path(error)}: {error.message}")

    print(f"JSON Schema validation — {instance_count} instance")
    if failures:
        print(f"FAILED: {len(failures)} error")
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1

    print("OK: seluruh schema valid Draft 2020-12 dan seluruh JSON instance cocok dengan schema-nya.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
