#!/usr/bin/env python3
"""Helper stdlib untuk discovery pack, eval suite, dan source registry Ramu."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK_INDEX = ROOT / "packs/index.json"


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


def eval_paths(ctx: dict[str, Any]) -> list[tuple[str, Path, Path]]:
    config = ctx["manifest"].get("evals") or {}
    pairs = [
        ("core", config.get("core_contracts"), config.get("core_behavior")),
        ("pack", config.get("pack_contracts"), config.get("pack_behavior")),
    ]
    resolved: list[tuple[str, Path, Path]] = []
    for scope, contracts, behavior in pairs:
        if not contracts or not behavior:
            raise RepoError(f"Pack {ctx['id']} kehilangan eval {scope} contracts/behavior.")
        resolved.append((scope, repo_path(contracts), repo_path(behavior)))
    return resolved


def merged_eval_suite(ctx: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    contract_cases: list[dict[str, Any]] = []
    behavior_cases: list[dict[str, Any]] = []
    defaults: dict[str, Any] = {"min_score": 0.75, "max_output_tokens": 1200}

    for scope, contract_path, behavior_path in eval_paths(ctx):
        contracts = load_json(contract_path)
        behavior = load_json(behavior_path)
        if contracts.get("scope") not in {None, scope}:
            raise RepoError(f"Scope eval tidak cocok: {contract_path.relative_to(ROOT)}")
        if behavior.get("scope") not in {None, scope}:
            raise RepoError(f"Scope behavior tidak cocok: {behavior_path.relative_to(ROOT)}")
        if scope == "pack":
            for data, path in ((contracts, contract_path), (behavior, behavior_path)):
                declared = data.get("pack_id")
                if declared and declared != ctx["id"]:
                    raise RepoError(
                        f"pack_id eval {path.relative_to(ROOT)} adalah {declared}, bukan {ctx['id']}"
                    )
        contract_cases.extend(contracts.get("cases", []))
        behavior_cases.extend(behavior.get("cases", []))
        defaults.update(behavior.get("defaults") or {})

    return (
        {"version": 1, "pack_id": ctx["id"], "cases": contract_cases},
        {"version": 1, "pack_id": ctx["id"], "defaults": defaults, "cases": behavior_cases},
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
