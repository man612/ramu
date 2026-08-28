#!/usr/bin/env python3
"""Validasi identity institusi/program/pack lintas katalog, manifest, registry, dan eval suite."""

from __future__ import annotations

import sys

from ramu_repo import (
    ROOT,
    RepoError,
    declared_source_registry_paths,
    eval_suite_paths,
    load_json,
    load_pack_index,
    pack_context,
)


def main() -> int:
    errors: list[str] = []
    try:
        index = load_pack_index()
    except RepoError as exc:
        print(f"Scope identity validation — discovery gagal: {exc}", file=sys.stderr)
        return 2

    institution_names: dict[str, str] = {}
    program_owners: dict[str, tuple[str, str]] = {}

    for entry in index["packs"]:
        pack_id = str(entry.get("id", "<tanpa-id>"))
        try:
            ctx = pack_context(pack_id)
        except RepoError as exc:
            errors.append(str(exc))
            continue

        manifest = ctx["manifest"]
        institution_id = str(manifest.get("institution_id", "")).strip()
        institution = str(manifest.get("institution", "")).strip()
        program_id = str(manifest.get("program_id", "")).strip()
        program = str(manifest.get("program", "")).strip()

        for key in ("institution_id", "institution", "program_id", "program"):
            if entry.get(key) != manifest.get(key):
                errors.append(
                    f"{pack_id}: katalog `{key}` {entry.get(key)!r} berbeda dari manifest {manifest.get(key)!r}."
                )

        known_institution = institution_names.setdefault(institution_id, institution)
        if known_institution != institution:
            errors.append(
                f"institution_id {institution_id!r} dipakai untuk dua nama berbeda: {known_institution!r} dan {institution!r}."
            )

        owner = (institution_id, program)
        known_owner = program_owners.setdefault(program_id, owner)
        if known_owner != owner:
            errors.append(
                f"program_id {program_id!r} tidak unik secara global: {known_owner!r} vs {owner!r}."
            )

        try:
            eval_suite_paths(ctx)
        except RepoError as exc:
            errors.append(str(exc))

        try:
            registries = declared_source_registry_paths(ctx)
        except RepoError as exc:
            errors.append(str(exc))
            continue

        for path in registries:
            try:
                registry = load_json(path)
            except RepoError as exc:
                errors.append(str(exc))
                continue
            scope = str(registry.get("scope", ""))
            rel = str(path.relative_to(ROOT))
            if scope == "global":
                continue
            if registry.get("institution_id") != institution_id:
                errors.append(
                    f"{pack_id}: registry {rel} scope {scope} institution_id {registry.get('institution_id')!r} "
                    f"tidak sama dengan {institution_id!r}."
                )
            if registry.get("institution") != institution:
                errors.append(
                    f"{pack_id}: registry {rel} institution {registry.get('institution')!r} tidak sama dengan {institution!r}."
                )
            if scope in {"program", "pack"}:
                if registry.get("program_id") != program_id:
                    errors.append(
                        f"{pack_id}: registry {rel} program_id {registry.get('program_id')!r} tidak sama dengan {program_id!r}."
                    )
                if registry.get("program") != program:
                    errors.append(
                        f"{pack_id}: registry {rel} program {registry.get('program')!r} tidak sama dengan {program!r}."
                    )
            if scope == "pack" and registry.get("pack_id") != pack_id:
                errors.append(
                    f"{pack_id}: registry {rel} pack_id {registry.get('pack_id')!r} tidak sama dengan pack aktif."
                )

    if errors:
        print(f"Scope identity validation — {len(errors)} error")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "Scope identity validation — OK: "
        f"{len(index['packs'])} pack, {len(institution_names)} institution id, {len(program_owners)} program id konsisten."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
