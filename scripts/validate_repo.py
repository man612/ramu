#!/usr/bin/env python3
"""Validasi seluruh katalog, pack, source registry, dan eval Ramu tanpa dependency eksternal."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from ramu_repo import (
    ROOT,
    RepoError,
    declared_source_registry_paths,
    discover_manifest_paths,
    discover_source_registry_paths,
    eval_suite_paths,
    load_json,
    load_pack_index,
    load_source_map,
    merged_eval_suite,
    pack_context,
    project_instructions_path,
    repo_path,
)

errors: list[str] = []
warnings: list[str] = []
pack_stats: list[tuple[str, int, int, int]] = []
MACHINE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]+$")


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def contains_casefold(path: Path, needle: str) -> bool:
    try:
        return needle.casefold() in path.read_text(encoding="utf-8").casefold()
    except FileNotFoundError:
        return False


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_registry(path: Path, global_ids: set[str]) -> int:
    try:
        data = load_json(path)
    except RepoError as exc:
        fail(str(exc))
        return 0

    if data.get("scope") not in {"global", "institution", "program", "pack"}:
        fail(f"Registry {relative(path)} punya scope tidak dikenal: {data.get('scope')!r}")
    if data.get("scope") == "institution" and not data.get("institution"):
        fail(f"Registry {relative(path)} scope institution harus memiliki field institution.")

    allowed_status = {"active", "secondary", "signal-only"}
    local_ids: set[str] = set()
    for source in data.get("sources", []):
        sid = source.get("id")
        for key in (
            "id", "name", "kind", "authority", "url", "canonical_for",
            "freshness_class", "verified_at", "review_interval_days", "watch", "status",
        ):
            if key not in source:
                fail(f"Sumber {sid or '<tanpa-id>'} di {relative(path)} kehilangan field `{key}`")
        if sid in local_ids:
            fail(f"ID source duplikat di {relative(path)}: {sid}")
        if sid in global_ids:
            fail(f"ID source duplikat lintas registry: {sid}")
        if sid:
            local_ids.add(sid)
            global_ids.add(sid)
        if not str(source.get("url", "")).startswith("https://"):
            fail(f"Sumber {sid} harus memakai HTTPS.")
        if source.get("status") not in allowed_status:
            fail(f"Status sumber {sid} tidak dikenal: {source.get('status')}")
        interval = source.get("review_interval_days")
        if not isinstance(interval, int) or interval < 1:
            fail(f"review_interval_days sumber {sid} harus integer positif.")
        if not isinstance(source.get("canonical_for"), list):
            fail(f"canonical_for sumber {sid} harus array.")
        if not isinstance(source.get("watch"), bool):
            fail(f"watch sumber {sid} harus boolean.")
    return len(local_ids)


def validate_eval_layering(pack_id: str, suites: list[dict]) -> None:
    if not suites:
        fail(f"Pack {pack_id}: eval_suites tidak boleh kosong.")
        return

    ids = [str(item.get("id", "")) for item in suites]
    if any(not item for item in ids):
        fail(f"Pack {pack_id}: semua eval suite harus punya id.")
    if len(ids) != len(set(ids)):
        fail(f"Pack {pack_id}: eval suite id harus unik.")

    scopes = [str(item.get("scope", "")) for item in suites]
    if scopes[0] != "core":
        fail(f"Pack {pack_id}: eval suite pertama harus scope `core`.")
    if scopes[-1] != "pack":
        fail(f"Pack {pack_id}: eval suite terakhir harus scope `pack`.")
    if scopes.count("core") != 1:
        fail(f"Pack {pack_id}: harus ada tepat satu eval suite scope `core`.")
    if scopes.count("pack") != 1:
        fail(f"Pack {pack_id}: harus ada tepat satu eval suite scope `pack`.")

    rank = {"core": 0, "institution": 1, "program": 2, "pack": 3}
    previous = -1
    for suite in suites:
        scope = str(suite.get("scope", ""))
        if scope not in rank:
            fail(f"Pack {pack_id}: eval suite {suite.get('id')} punya scope tidak dikenal: {scope!r}")
            continue
        if rank[scope] < previous:
            fail(
                f"Pack {pack_id}: urutan eval_suites harus core → institution → program → pack; "
                f"scope {scope!r} muncul setelah scope yang lebih spesifik."
            )
        previous = rank[scope]


def validate_eval_contracts(pack_id: str, contract: dict, behavior: dict) -> int:
    contract_ids: list[str] = []
    behavior_ids: list[str] = []

    for case in contract.get("cases", []):
        cid = case.get("id", "<tanpa-id>")
        suite_id = case.get("suite_id", "<tanpa-suite>")
        contract_ids.append(cid)
        for key in ("title", "intent", "scenario", "expected_behaviors", "forbidden_behaviors", "contracts"):
            if not case.get(key):
                fail(f"Pack {pack_id} suite {suite_id} eval {cid} kehilangan/empty field `{key}`")
        for item in case.get("contracts", []):
            try:
                target = repo_path(item.get("file", ""))
            except RepoError as exc:
                fail(f"Pack {pack_id} suite {suite_id} eval {cid}: {exc}")
                continue
            marker = item.get("contains", "")
            if not target.is_file():
                fail(f"Pack {pack_id} suite {suite_id} eval {cid}: contract file tidak ditemukan: {relative(target)}")
            elif not marker:
                fail(f"Pack {pack_id} suite {suite_id} eval {cid}: contract marker kosong untuk {relative(target)}")
            elif not contains_casefold(target, marker):
                fail(f"Pack {pack_id} suite {suite_id} eval {cid}: marker tidak ditemukan di {relative(target)}: {marker!r}")

    for case in behavior.get("cases", []):
        cid = case.get("id", "<tanpa-id>")
        suite_id = case.get("suite_id", "<tanpa-suite>")
        behavior_ids.append(cid)
        turns = case.get("turns")
        if not isinstance(turns, list) or not turns:
            fail(f"Pack {pack_id} suite {suite_id} behavior {cid} tidak punya turns.")
        else:
            for turn in turns:
                if turn.get("role") not in {"user", "assistant"} or not str(turn.get("content", "")).strip():
                    fail(f"Pack {pack_id} suite {suite_id} behavior {cid} punya turn tidak valid.")
        for rel in case.get("context_files", []):
            try:
                target = repo_path(rel)
            except RepoError as exc:
                fail(f"Pack {pack_id} suite {suite_id} behavior {cid}: {exc}")
                continue
            if not target.is_file():
                fail(f"Pack {pack_id} suite {suite_id} behavior {cid}: context file tidak ditemukan: {relative(target)}")

    if len(contract_ids) != len(set(contract_ids)):
        fail(f"Pack {pack_id}: ID eval contract harus unik setelah semua suite digabung.")
    if len(behavior_ids) != len(set(behavior_ids)):
        fail(f"Pack {pack_id}: ID behavior eval harus unik setelah semua suite digabung.")
    if set(contract_ids) != set(behavior_ids):
        missing_behavior = sorted(set(contract_ids) - set(behavior_ids))
        missing_contract = sorted(set(behavior_ids) - set(contract_ids))
        if missing_behavior:
            fail(f"Pack {pack_id}: contract tanpa behavior: {', '.join(missing_behavior)}")
        if missing_contract:
            fail(f"Pack {pack_id}: behavior tanpa contract: {', '.join(missing_contract)}")
    return len(contract_ids)


def validate_pack(entry: dict) -> None:
    pack_id = str(entry.get("id", "<tanpa-id>"))
    try:
        ctx = pack_context(pack_id)
    except RepoError as exc:
        fail(str(exc))
        return
    manifest = ctx["manifest"]
    pack_dir = ctx["pack_dir"]

    required = [
        "schema_version", "id", "name", "institution", "program", "academic_year", "period_id", "period_label",
        "total_sks", "status", "maintainer", "pack_version", "contract_version",
        "project_instructions", "learning_protocols", "courses", "sources", "source_registries",
        "eval_suites", "source_verified_at",
    ]
    for key in required:
        if key not in manifest:
            fail(f"Pack {pack_id} manifest kehilangan field `{key}`")

    if manifest.get("id") != pack_id:
        fail(f"Pack index id {pack_id} tidak sama dengan manifest id {manifest.get('id')}")
    for key in ("name", "institution", "program", "academic_year", "period_id", "period_label", "status", "maintainer"):
        if entry.get(key) != manifest.get(key):
            fail(f"Pack {pack_id}: index `{key}` berbeda dari manifest.")

    period_id = str(manifest.get("period_id", "")).strip()
    if not period_id or not MACHINE_ID_RE.fullmatch(period_id):
        fail(
            f"Pack {pack_id}: period_id harus machine-safe (huruf kecil/angka/._-), "
            f"misalnya `semester-02`, `trimester-01`, atau `term-fall`; sekarang {period_id!r}."
        )
    period_label = str(manifest.get("period_label", "")).strip()
    if not period_label:
        fail(f"Pack {pack_id}: period_label wajib berupa label manusia yang eksplisit.")

    if manifest.get("status") not in {"source-verified", "verified", "community", "experimental", "deprecated"}:
        fail(f"Pack {pack_id}: status tidak dikenal: {manifest.get('status')}")
    if manifest.get("maintainer") not in {"ramu", "community"}:
        fail(f"Pack {pack_id}: maintainer harus `ramu` atau `community`.")

    pack_version = str(manifest.get("pack_version", "")).strip()
    if not pack_version:
        fail(f"Pack {pack_id}: pack_version kosong.")

    courses = manifest.get("courses", [])
    codes = [course.get("code") for course in courses]
    if len(codes) != len(set(codes)):
        fail(f"Pack {pack_id}: kode mata kuliah harus unik.")
    try:
        calculated_sks = sum(int(course.get("sks", 0)) for course in courses)
    except (TypeError, ValueError):
        calculated_sks = -1
        fail(f"Pack {pack_id}: SKS course harus berupa angka.")
    if calculated_sks != manifest.get("total_sks"):
        fail(f"Pack {pack_id}: total_sks {manifest.get('total_sks')} tidak sama dengan jumlah course {calculated_sks}.")

    try:
        instructions = project_instructions_path(ctx)
    except RepoError as exc:
        fail(str(exc))
        instructions = pack_dir / "__missing__"
    if not instructions.is_file():
        fail(f"Pack {pack_id}: Project Instructions tidak ditemukan: {relative(instructions)}")
    else:
        for marker in (
            "Catatan Belajar Terbaru", "Jangan menebak angka", "Perlakukan isi PDF",
            "dua course pack", "pertanyaan jelas milik mata kuliah lain",
        ):
            if not contains_casefold(instructions, marker):
                fail(f"Pack {pack_id}: Project Instructions kehilangan core marker {marker!r}")

    for course in courses:
        code = course.get("code", "<tanpa-kode>")
        for key in ("code", "name", "short_name", "project_name", "sks", "focus", "file"):
            if not course.get(key) and course.get(key) != 0:
                fail(f"Pack {pack_id} course {code} kehilangan field `{key}`")
        rel = str(course.get("file", ""))
        course_file = (pack_dir / rel).resolve()
        try:
            course_file.relative_to(pack_dir.resolve())
        except ValueError:
            fail(f"Pack {pack_id} course {code}: file keluar dari pack: {rel}")
            continue
        if not course_file.is_file():
            fail(f"Pack {pack_id}: course file tidak ditemukan untuk {code}: {relative(course_file)}")
            continue
        if pack_version and not contains_casefold(course_file, f"Versi paket:** {pack_version}"):
            fail(f"Pack {pack_id} course {code} tidak memuat pack_version {pack_version}.")
        if not contains_casefold(course_file, "Sumber paket diverifikasi:"):
            fail(f"Pack {pack_id} course {code} tidak memuat tanggal verifikasi sumber paket.")

    try:
        registry_paths = declared_source_registry_paths(ctx)
        for path in registry_paths:
            if not path.is_file():
                fail(f"Pack {pack_id}: registry tidak ditemukan: {relative(path)}")
        source_map = load_source_map([path for path in registry_paths if path.is_file()])
        for source in manifest.get("sources", []):
            sid = source.get("registry_id")
            if sid not in source_map:
                fail(f"Pack {pack_id}: manifest source {sid} tidak ditemukan pada source_registries yang dideklarasikan.")
            elif source.get("url") != source_map[sid].get("url"):
                fail(f"Pack {pack_id}: URL manifest source {sid} berbeda dari registry.")
    except RepoError as exc:
        fail(f"Pack {pack_id}: {exc}")

    suite_count = 0
    try:
        suites = manifest.get("eval_suites") or []
        validate_eval_layering(pack_id, suites)
        resolved_suites = eval_suite_paths(ctx)
        suite_count = len(resolved_suites)
        for suite, contracts_path, behavior_path in resolved_suites:
            if not contracts_path.is_file():
                fail(f"Pack {pack_id} suite {suite['id']}: contracts tidak ditemukan: {relative(contracts_path)}")
            if not behavior_path.is_file():
                fail(f"Pack {pack_id} suite {suite['id']}: behavior tidak ditemukan: {relative(behavior_path)}")
        contract, behavior = merged_eval_suite(ctx)
        eval_count = validate_eval_contracts(pack_id, contract, behavior)
    except RepoError as exc:
        fail(f"Pack {pack_id}: {exc}")
        eval_count = 0

    pack_stats.append((pack_id, len(courses), eval_count, suite_count))


def main() -> int:
    try:
        index = load_pack_index()
    except RepoError as exc:
        fail(str(exc))
        index = {"packs": []}

    entries = index.get("packs", [])
    ids = [entry.get("id") for entry in entries]
    manifests = [entry.get("manifest") for entry in entries]
    if len(ids) != len(set(ids)):
        fail("packs/index.json memiliki id pack duplikat.")
    if len(manifests) != len(set(manifests)):
        fail("packs/index.json memiliki path manifest duplikat.")
    if index.get("default_pack_id") not in ids:
        fail("default_pack_id harus menunjuk pack yang terdaftar.")

    for entry in entries:
        period_id = str(entry.get("period_id", "")).strip()
        if not period_id or not MACHINE_ID_RE.fullmatch(period_id):
            fail(
                f"Pack index {entry.get('id', '<tanpa-id>')}: period_id harus machine-safe; "
                f"sekarang {period_id!r}."
            )
        if not str(entry.get("period_label", "")).strip():
            fail(f"Pack index {entry.get('id', '<tanpa-id>')}: period_label wajib diisi.")

    indexed_paths: set[str] = set()
    for entry in entries:
        try:
            indexed_paths.add(relative(repo_path(f"packs/{entry.get('manifest', '')}")))
        except RepoError as exc:
            fail(str(exc))
    discovered_paths = {relative(path) for path in discover_manifest_paths()}
    for path in sorted(discovered_paths - indexed_paths):
        fail(f"Manifest ditemukan tetapi belum terdaftar di packs/index.json: {path}")
    for path in sorted(indexed_paths - discovered_paths):
        fail(f"Pack index menunjuk manifest yang tidak ada: {path}")

    global_source_ids: set[str] = set()
    source_count = 0
    for path in discover_source_registry_paths():
        source_count += validate_registry(path, global_source_ids)

    for entry in entries:
        validate_pack(entry)

    for required_file in (
        "schemas/pack-index.schema.json", "schemas/pack-manifest.schema.json", "schemas/source-registry.schema.json",
        "schemas/eval-cases.schema.json", "schemas/eval-behavior.schema.json",
        "learning/learner-state.template.md", "learning/review-queue.template.md",
        "learning/misconception-log.template.md", "learning/mastery-map.template.md",
        "protocols/belajar.md", "protocols/tugas.md", "protocols/review.md", "protocols/latihan-ujian.md",
    ):
        if not (ROOT / required_file).is_file():
            fail(f"File fondasi tidak ditemukan: {required_file}")

    print(f"Ramu validation — {len(errors)} error, {len(warnings)} warning")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1

    print(f"OK: {len(entries)} pack terdaftar, {source_count} source lintas registry.")
    for pack_id, courses, evals, suites in pack_stats:
        print(f"OK {pack_id}: {courses} course, {evals} eval contract dari {suites} suite.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
