#!/usr/bin/env python3
"""Regression proof untuk abstraction multi-pack, multi-institution, dan academic period generic."""

from __future__ import annotations

import copy
import sys

from jsonschema import Draft202012Validator, FormatChecker

from ramu_repo import ROOT, RepoError, load_json, validate_eval_scope_identity


FIXTURE = ROOT / "tests/fixtures/multi-pack-proof.json"


def validator(name: str) -> Draft202012Validator:
    schema = load_json(ROOT / f"schemas/{name}")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def require_valid(checker: Draft202012Validator, value: dict, label: str) -> None:
    errors = list(checker.iter_errors(value))
    if errors:
        raise AssertionError(f"{label} seharusnya valid: {errors[0].message}")


def require_invalid(checker: Draft202012Validator, value: dict, label: str) -> None:
    if not list(checker.iter_errors(value)):
        raise AssertionError(f"{label} seharusnya ditolak schema.")


def check_namespace(manifest: dict) -> None:
    institution_id = manifest["institution_id"]
    program_id = manifest["program_id"]
    pack_id = manifest["id"]
    if not program_id.startswith(institution_id + "."):
        raise AssertionError(f"program_id {program_id} keluar namespace {institution_id}")
    if not pack_id.startswith(program_id + "."):
        raise AssertionError(f"pack id {pack_id} keluar namespace {program_id}")


def main() -> int:
    data = load_json(FIXTURE)
    catalog = data["catalog"]
    manifests = data["manifests"]

    catalog_schema = validator("pack-index.schema.json")
    manifest_schema = validator("pack-manifest.schema.json")
    registry_schema = validator("source-registry.schema.json")

    require_valid(catalog_schema, catalog, "fixture catalog")
    manifest_by_id = {item["id"]: item for item in manifests}
    for manifest in manifests:
        require_valid(manifest_schema, manifest, manifest["id"])
        check_namespace(manifest)
        ctx = {"id": manifest["id"], "manifest": manifest}
        for suite in manifest["eval_suites"]:
            validate_eval_scope_identity(ctx, suite)

    if len(manifest_by_id) != len(catalog["packs"]):
        raise AssertionError("Jumlah manifest fixture harus sama dengan catalog fixture.")
    for entry in catalog["packs"]:
        manifest = manifest_by_id.get(entry["id"])
        if not manifest:
            raise AssertionError(f"Catalog fixture tidak punya manifest untuk {entry['id']}")
        for key in ("institution_id", "institution", "program_id", "program", "period_id", "period_label"):
            if entry[key] != manifest[key]:
                raise AssertionError(f"Fixture {entry['id']} mismatch {key}")

    institutions = {item["institution_id"] for item in manifests}
    periods = {item["period_id"] for item in manifests}
    if len(institutions) < 2:
        raise AssertionError("Fixture harus membuktikan minimal dua institusi.")
    if not any(item.startswith("trimester-") for item in periods):
        raise AssertionError("Fixture harus membuktikan academic period non-semester: trimester.")
    if not any(item.startswith("term-") for item in periods):
        raise AssertionError("Fixture harus membuktikan academic period non-semester: term.")
    if not any(any(suite["scope"] == "program" for suite in item["eval_suites"]) for item in manifests):
        raise AssertionError("Fixture harus membuktikan program-level eval suite.")

    wrong_scope = copy.deepcopy(manifests[0])
    institution_suite = next(item for item in wrong_scope["eval_suites"] if item["scope"] == "institution")
    institution_suite["scope_ref"] = "id.beta"
    try:
        validate_eval_scope_identity({"id": wrong_scope["id"], "manifest": wrong_scope}, institution_suite)
    except RepoError:
        pass
    else:
        raise AssertionError("Cross-institution eval scope_ref harus ditolak.")

    legacy_semester = copy.deepcopy(manifests[0])
    legacy_semester["semester"] = 2
    require_invalid(manifest_schema, legacy_semester, "legacy field semester")

    valid_registries = [
        {"version": 1, "scope": "global", "verified_at": "2026-08-01", "sources": []},
        {"version": 1, "scope": "institution", "institution_id": "id.alpha", "institution": "Alpha University", "verified_at": "2026-08-01", "sources": []},
        {"version": 1, "scope": "program", "institution_id": "id.alpha", "institution": "Alpha University", "program_id": "id.alpha.business", "program": "Business", "verified_at": "2026-08-01", "sources": []},
        {"version": 1, "scope": "pack", "institution_id": "id.alpha", "institution": "Alpha University", "program_id": "id.alpha.business", "program": "Business", "pack_id": "id.alpha.business.2026-2027.s2", "verified_at": "2026-08-01", "sources": []},
    ]
    for item in valid_registries:
        require_valid(registry_schema, item, f"registry scope {item['scope']}")

    invalid_program_registry = copy.deepcopy(valid_registries[2])
    invalid_program_registry.pop("program_id")
    require_invalid(registry_schema, invalid_program_registry, "program registry tanpa program_id")

    print(
        "Architecture proof — OK: 3 synthetic packs, 2 institutions, semester + trimester + term, "
        "program suite, namespace identity, cross-scope rejection, dan registry conditionals teruji."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, RepoError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
