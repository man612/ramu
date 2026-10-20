#!/usr/bin/env python3
"""CI policy: published pack behavior/content changes need a pack version and reviewable notes.

Compare Git snapshots, not working-tree timestamps. Works for PR merge SHA and main push SHA.
Source registry review debt and repository-only edits do not force re-uploading user packs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath


def read_at(rev: str, path: str) -> bytes | None:
    result = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True)
    return result.stdout if result.returncode == 0 else None


def parsed(rev: str, path: str) -> dict | None:
    content = read_at(rev, path)
    return json.loads(content) if content is not None else None


def pack_snapshots(rev: str) -> dict[str, tuple[str, dict]]:
    index = parsed(rev, "packs/index.json")
    if index is None:
        return {}
    result = {}
    for entry in index.get("packs", []):
        path = f"packs/{entry['manifest']}"
        manifest = parsed(rev, path)
        if manifest is None:
            raise ValueError(f"{rev}: manifest pack hilang: {path}")
        result[entry["id"]] = (path, manifest)
    return result


def published_signature(rev: str, manifest_path: str, manifest: dict) -> str:
    base = str(PurePosixPath(manifest_path).parent)
    files: dict[str, str] = {}
    refs = [manifest["project_instructions"]] + [c["file"] for c in manifest["courses"]]
    for ref in refs:
        path = str(PurePosixPath(base) / ref)
        payload = read_at(rev, path)
        if payload is None:
            raise ValueError(f"{rev}: published pack file hilang: {path}")
        files[ref] = hashlib.sha256(payload).hexdigest()
    # source_verified_at/status/registry metadata is NOT a runtime pack change.
    # Conversely course metadata, Sources URLs, and protocols affect what users receive.
    data = {
        "pack_id": manifest["id"], "academic_year": manifest["academic_year"],
        "period_id": manifest["period_id"], "period_label": manifest["period_label"],
        "institution_id": manifest["institution_id"], "program_id": manifest["program_id"],
        "courses": manifest["courses"], "sources": manifest.get("sources", []),
        "learning_protocols": manifest.get("learning_protocols", []),
        "project_instructions": manifest["project_instructions"],
        "files": files,
    }
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def version_is_newer(old: str, new: str) -> bool:
    if old == new:
        return False
    a = re.fullmatch(r"(.+\.)([0-9]+)", old)
    b = re.fullmatch(r"(.+\.)([0-9]+)", new)
    if a and b:
        return a.group(1) == b.group(1) and int(b.group(2)) > int(a.group(2))
    # Non-numeric conventions can still bump, but may not silently reuse old version.
    return True


def check(base: str, head: str) -> list[str]:
    before = pack_snapshots(base)
    after = pack_snapshots(head)
    failures = []
    for pack_id, (new_path, new_manifest) in after.items():
        if pack_id not in before:
            continue  # First publication already needs schema/identity validation.
        old_path, old_manifest = before[pack_id]
        if published_signature(base, old_path, old_manifest) == published_signature(
            head, new_path, new_manifest
        ):
            continue
        previous = str(old_manifest.get("pack_version", ""))
        current = str(new_manifest.get("pack_version", ""))
        if not version_is_newer(previous, current):
            failures.append(
                f"{pack_id}: isi konfigurasi yang diterbitkan berubah, tetapi pack_version "
                f"{previous!r} → {current!r} tidak naik. Naikkan versi pack."
            )
            continue
        change_file = str(PurePosixPath(new_path).parent / "PACK-CHANGES.md")
        notes = read_at(head, change_file)
        if notes is None or f"## {current}" not in notes.decode("utf-8"):
            failures.append(
                f"{pack_id}: pack_version naik ke {current!r}, tetapi {change_file} "
                f"belum punya heading '## {current}' yang menjelaskan perubahan bagi pengguna."
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args()
    if not args.base or set(args.base) == {"0"}:
        print("Pack version policy — SKIP: initial push has no valid baseline.")
        return 0
    try:
        errors = check(args.base, args.head)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Pack version policy — ERROR: {exc}")
        return 1
    for error in errors:
        print(f"Pack version policy — ERROR: {error}")
    if errors:
        return 1
    print("Pack version policy — OK: perubahan published pack mempunyai versi dan notes, bila diperlukan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
