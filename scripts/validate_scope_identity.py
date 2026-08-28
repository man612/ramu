#!/usr/bin/env python3
"""Validasi stable identity dan relasi scope lintas catalog, manifest, registry, dan eval suite."""

from __future__ import annotations

import sys

from ramu_repo import (
    RepoError,
    declared_source_registry_paths,
    eval_suite_paths,
    load_json,
    load_pack_index,
    pack_context,
)


def main() -> int:
    errors: list[str] = []
    index = load_pack_index()

    for entry in index["packs"]:
        pack_id = str(entry.get("id", ""))
        try:
            ctx = pack_context(pack_id)
        except RepoError as exc:
            errors.append(str(exc))
            continue
        manifest = ctx["manifest"]

        for key in ("institution_id", "institution", "program_id", "program"):
            if entry.get(key) != manifest.get(key):
                errors.append(f"{pack_id}: catalog `{key}` berbeda dari manifest.")

        institution_id = str(manifest.get("institution_id", ""))
        program_id = str(manifest.get("program_id", ""))
        if not program_id.startswith(institution_id + "."):
            errors.append(f"{pack_id}: program_id {program_id!r} harus berada di namespace {institution_id!r}.")
        if not pack_id.startswith(program_id + "."):
            errors.append(f"{pack_id}: pack id harus berada di namespace program_id {program_id!r}.")

        try:
            eval_suite_paths(ctx)
        except RepoError as exc:
            errors.append(str(exc))

        try:
            for registry_path in declared_source_registry_paths(ctx):
                registry = load_json(registry_path)
                scope = registry.get("scope")
                if scope == "global":
                    continue
                if registry.get("institution_id") != institution_id:
                    errors.append(
                        f"{pack_id}: registry {registry_path.name} scope {scope} institution_id "
                        f"{registry.get('institution_id')!r} != {institution_id!r}."
                    )
                if scope in {"program", "pack"} and registry.get("program_id") != program_id:
                    errors.append(
                        f"{pack_id}: registry {registry_path.name} scope {scope} program_id "
                        f"{registry.get('program_id')!r} != {program_id!r}."
                    )
                if scope == "pack" and registry.get("pack_id") != pack_id:
                    errors.append(
                        f"{pack_id}: registry {registry_path.name} pack_id "
                        f"{registry.get('pack_id')!r} tidak cocok."
                    )
        except RepoError as exc:
            errors.append(str(exc))

    print(f"Scope identity validation — {len(index['packs'])} pack")
    if errors:
        print(f"FAILED: {len(errors)} error")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("OK: catalog, manifest, source registry, dan eval suite memakai stable identity yang konsisten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
