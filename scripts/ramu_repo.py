#!/usr/bin/env python3
"""Helper stdlib untuk discovery pack, eval suite, dan source registry Ramu."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK_INDEX = ROOT / "packs/index.json"
PACK_INDEX_VERSION = 3
PACK_MANIFEST_SCHEMA_VERSION = 4
VALID_EVAL_SCOPES = {"core", "institution", "program", "pack"}


class RepoError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RepoError(f"File tidak ditemukan: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise RepoError(
            f"JSON tidak valid: {path.relative_to(ROOT)}:{exc.lineno}:{exc.colno} — {exc.msg}"
        ) from exc


def repo_path(value: str) -> Path:
    value = str(value or "").strip().replace("\\", "/")
    if not value or value.startswith("/"):
        raise RepoError(f"Path repo tidak valid: {value!r}")
    path = (ROOT / value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise RepoError(f"Path keluar dari repository: {value}") from exc
    return path


def load_pack_index() -> dict[str, Any]:
    data = load_json(PACK_INDEX)
    if data.get("version") != PACK_INDEX_VERSION:
        raise RepoError(
            f"packs/index.json version {data.get('version')!r} tidak didukung; "
            f"tooling ini membutuhkan version {PACK_INDEX_VERSION}."
        )
    packs = data.get("packs")
    if not isinstance(packs, list) or not packs:
        raise RepoError("packs/index.json harus memiliki daftar pack non-empty.")
    return data


def pack_entries() -> list[dict[str, Any]]:
    return load_pack_index()["packs"]


def pack_ids() -> list[str]:
    return [str(entry.get("id", "")) for entry in pack_entries()]


def pack_context(pack_id: str | None = None) -> dict[str, Any]:
    index = load_pack_index()
    selected_id = pack_id or index.get("default_pack_id")
    matches = [entry for entry in index["packs"] if entry.get("id") == selected_id]
    if not matches:
        available = ", ".join(pack_ids())
        raise RepoError(f"Pack tidak ditemukan: {selected_id}. Tersedia: {available}")
    entry = matches[0]
    manifest_path = repo_path(f"packs/{entry['manifest']}")
    manifest = load_json(manifest_path)
    if manifest.get("schema_version") != PACK_MANIFEST_SCHEMA_VERSION:
        raise RepoError(
            f"Manifest {manifest_path.relative_to(ROOT)} schema_version {manifest.get('schema_version')!r} "
            f"tidak didukung; tooling ini membutuhkan schema_version {PACK_MANIFEST_SCHEMA_VERSION}."
        )
    return {
        "id": selected_id,
        "entry": entry,
        "manifest": manifest,
        "manifest_path": manifest_path,
        "pack_dir": manifest_path.parent,
    }


def project_instructions_path(ctx: dict[str, Any]) -> Path:
    rel = str(ctx["manifest"].get("project_instructions", ""))
    path = (ctx["pack_dir"] / rel).resolve()
    try:
        path.relative_to(ctx["pack_dir"].resolve())
    except ValueError as exc:
        raise RepoError(f"Project Instructions keluar dari pack: {rel}") from exc
    return path


def expected_eval_scope_ref(ctx: dict[str, Any], scope: str) -> str | None:
    """Return stable identity yang wajib dirujuk suite pada scope tertentu."""
    manifest = ctx["manifest"]
    if scope == "core":
        return None
    if scope == "institution":
        return str(manifest.get("institution_id", "")).strip() or None
    if scope == "program":
        return str(manifest.get("program_id", "")).strip() or None
    if scope == "pack":
        return str(ctx["id"])
    raise RepoError(f"Scope eval tidak dikenal: {scope!r}")


def normalized_scope_ref(value: Any) -> str:
    """Normalisasi scope_ref tanpa mengubah None menjadi string literal 'None'."""
    if value is None:
        return ""
    return str(value).strip()


def validate_eval_scope_identity(ctx: dict[str, Any], suite: dict[str, Any]) -> None:
    """Pastikan scope_ref suite menunjuk identity milik pack, bukan sekadar slug bebas."""
    scope = str(suite.get("scope", "")).strip()
    scope_ref = normalized_scope_ref(suite.get("scope_ref"))
    expected = expected_eval_scope_ref(ctx, scope)
    if scope == "core":
        if scope_ref:
            raise RepoError(f"Pack {ctx['id']} suite {suite.get('id')} core tidak boleh memiliki scope_ref.")
        return
    if not expected:
        raise RepoError(f"Pack {ctx['id']} tidak memiliki stable identity untuk scope {scope!r}.")
    if scope_ref != expected:
        raise RepoError(
            f"Pack {ctx['id']} suite {suite.get('id')} scope {scope} harus merujuk {expected!r}; "
            f"sekarang {scope_ref!r}."
        )


def eval_suite_paths(ctx: dict[str, Any]) -> list[tuple[dict[str, Any], Path, Path]]:
    """Resolve ordered eval suites declared by one pack manifest."""
    suites = ctx["manifest"].get("eval_suites")
    if not isinstance(suites, list) or not suites:
        raise RepoError(f"Pack {ctx['id']} tidak mendeklarasikan eval_suites.")

    seen_ids: set[str] = set()
    resolved: list[tuple[dict[str, Any], Path, Path]] = []
    for index, raw in enumerate(suites, start=1):
        if not isinstance(raw, dict):
            raise RepoError(f"Pack {ctx['id']} eval_suites[{index}] harus object.")
        suite_id = str(raw.get("id", "")).strip()
        scope = str(raw.get("scope", "")).strip()
        scope_ref = normalized_scope_ref(raw.get("scope_ref"))
        contracts = str(raw.get("contracts", "")).strip()
        behavior = str(raw.get("behavior", "")).strip()

        if not suite_id:
            raise RepoError(f"Pack {ctx['id']} eval_suites[{index}] kehilangan id.")
        if suite_id in seen_ids:
            raise RepoError(f"Pack {ctx['id']} memiliki eval suite id duplikat: {suite_id}")
        seen_ids.add(suite_id)
        if scope not in VALID_EVAL_SCOPES:
            raise RepoError(f"Pack {ctx['id']} suite {suite_id} punya scope tidak dikenal: {scope!r}")
        if scope != "core" and not scope_ref:
            raise RepoError(f"Pack {ctx['id']} suite {suite_id} scope {scope} membutuhkan scope_ref.")
        if not contracts or not behavior:
            raise RepoError(f"Pack {ctx['id']} suite {suite_id} kehilangan contracts/behavior.")

        suite = {
            "id": suite_id,
            "scope": scope,
            "scope_ref": scope_ref or None,
        }
        validate_eval_scope_identity(ctx, suite)
        resolved.append((suite, repo_path(contracts), repo_path(behavior)))
    return resolved


def merged_eval_suite(ctx: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Merge ordered eval suites. Later behavior defaults override earlier defaults."""
    contract_cases: list[dict[str, Any]] = []
    behavior_cases: list[dict[str, Any]] = []
    defaults: dict[str, Any] = {"min_score": 0.75, "max_output_tokens": 1200}
    suite_order: list[str] = []

    for suite, contract_path, behavior_path in eval_suite_paths(ctx):
        contracts = load_json(contract_path)
        behavior = load_json(behavior_path)
        suite_id = suite["id"]
        scope = suite["scope"]
        scope_ref = suite["scope_ref"]
        suite_order.append(suite_id)

        for data, path, kind in (
            (contracts, contract_path, "contracts"),
            (behavior, behavior_path, "behavior"),
        ):
            if data.get("suite_id") != suite_id:
                raise RepoError(
                    f"Eval {kind} {path.relative_to(ROOT)} suite_id {data.get('suite_id')!r} tidak sama dengan {suite_id!r}."
                )
            if data.get("scope") != scope:
                raise RepoError(
                    f"Eval {kind} {path.relative_to(ROOT)} scope {data.get('scope')!r} tidak sama dengan {scope!r}."
                )
            declared_ref = data.get("scope_ref")
            if scope == "core":
                if declared_ref not in {None, ""}:
                    raise RepoError(f"Eval core {path.relative_to(ROOT)} tidak boleh memiliki scope_ref.")
            elif declared_ref != scope_ref:
                raise RepoError(
                    f"Eval {kind} {path.relative_to(ROOT)} scope_ref {declared_ref!r} tidak sama dengan {scope_ref!r}."
                )

        for case in contracts.get("cases", []):
            item = dict(case)
            item["suite_id"] = suite_id
            contract_cases.append(item)
        for case in behavior.get("cases", []):
            item = dict(case)
            item["suite_id"] = suite_id
            behavior_cases.append(item)
        defaults.update(behavior.get("defaults") or {})

    return (
        {"version": 1, "pack_id": ctx["id"], "suite_order": suite_order, "cases": contract_cases},
        {
            "version": 1,
            "pack_id": ctx["id"],
            "suite_order": suite_order,
            "defaults": defaults,
            "cases": behavior_cases,
        },
    )


def discover_manifest_paths() -> list[Path]:
    return sorted(ROOT.glob("packs/**/manifest.json"))


def discover_source_registry_paths() -> list[Path]:
    paths = [ROOT / "sources/registry.json"]
    paths.extend(sorted(ROOT.glob("packs/**/source-registry.json")))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            unique.append(path)
            seen.add(resolved)
    return unique


def declared_source_registry_paths(ctx: dict[str, Any]) -> list[Path]:
    values = ctx["manifest"].get("source_registries") or []
    if not values:
        raise RepoError(f"Pack {ctx['id']} tidak mendeklarasikan source_registries.")
    return [repo_path(value) for value in values]


def load_source_map(paths: list[Path]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in paths:
        data = load_json(path)
        for source in data.get("sources", []):
            sid = source.get("id")
            if not sid:
                raise RepoError(f"Source tanpa id di {path.relative_to(ROOT)}")
            if sid in result:
                raise RepoError(f"Source id duplikat lintas registry: {sid}")
            result[sid] = source
    return result
