#!/usr/bin/env python3
"""Jalankan behavior eval Ramu terhadap model melalui OpenAI Responses API.

Tidak membutuhkan dependency Python eksternal. OPENAI_API_KEY hanya dibutuhkan
untuk run nyata; --dry-run dipakai CI untuk memvalidasi dataset dan prompt wiring.
Model kandidat dan judge sengaja tidak di-hardcode karena katalog model berubah.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02"
PROJECT_INSTRUCTIONS = PACK / "PROJECT-INSTRUCTIONS.md"
CONTRACT_CASES = ROOT / "evals/cases/semester-02.json"
BEHAVIOR_CASES = ROOT / "evals/behavior/semester-02.json"
DEFAULT_RESULTS_DIR = ROOT / "evals/results"
API_URL = os.environ.get("OPENAI_RESPONSES_URL", "https://api.openai.com/v1/responses")


class EvalError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvalError(f"File tidak ditemukan: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise EvalError(
            f"JSON tidak valid: {path.relative_to(ROOT)}:{exc.lineno}:{exc.colno} — {exc.msg}"
        ) from exc


def read_context(files: list[str]) -> str:
    parts = [
        "# Project Instructions\n" + PROJECT_INSTRUCTIONS.read_text(encoding="utf-8").strip()
    ]
    for rel in files:
        path = ROOT / rel
        if not path.is_file():
            raise EvalError(f"Context file tidak ditemukan: {rel}")
        parts.append(f"# Context: {rel}\n{path.read_text(encoding='utf-8').strip()}")
    return "\n\n---\n\n".join(parts)


def response_text(payload: dict[str, Any]) -> str:
    chunks: list[str] = []
    for item in payload.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                text = content.get("text")
                if text:
                    chunks.append(text)
    if not chunks:
        raise EvalError("Responses API tidak mengembalikan output_text.")
    return "\n".join(chunks).strip()


def usage(payload: dict[str, Any]) -> dict[str, int]:
    raw = payload.get("usage") or {}
    return {
        "input_tokens": int(raw.get("input_tokens") or 0),
        "output_tokens": int(raw.get("output_tokens") or 0),
        "total_tokens": int(raw.get("total_tokens") or 0),
    }


def merge_usage(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {key: a.get(key, 0) + b.get(key, 0) for key in ("input_tokens", "output_tokens", "total_tokens")}


def api_request(api_key: str, body: dict[str, Any], retries: int = 3) -> dict[str, Any]:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body_text = exc.read().decode("utf-8", errors="replace")
            last_error = EvalError(f"OpenAI API HTTP {exc.code}: {body_text[:1200]}")
            if exc.code not in {408, 409, 429, 500, 502, 503, 504} or attempt == retries:
                raise last_error
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = EvalError(f"OpenAI API tidak dapat diakses: {exc}")
            if attempt == retries:
                raise last_error
        time.sleep(2 ** (attempt - 1))

    raise EvalError(str(last_error or "OpenAI API request gagal"))


def candidate_request(
    api_key: str,
    model: str,
    context: str,
    case: dict[str, Any],
    max_output_tokens: int,
) -> tuple[str, dict[str, int]]:
    body: dict[str, Any] = {
        "model": model,
        "store": False,
        "instructions": (
            "Kamu sedang bertindak sebagai asisten di dalam ChatGPT Project yang memakai Ramu. "
            "Ikuti Project Instructions dan context yang diberikan. Jawab mahasiswa secara natural; "
            "jangan membahas bahwa ini adalah eval.\n\n" + context
        ),
        "input": case["turns"],
        "max_output_tokens": max_output_tokens,
    }
    if "web_search" in case.get("tools", []):
        body["tools"] = [{"type": "web_search"}]

    payload = api_request(api_key, body)
    return response_text(payload), usage(payload)


JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "pass": {"type": "boolean"},
        "score": {"type": "number", "minimum": 0, "maximum": 1},
        "expected_met": {"type": "array", "items": {"type": "string"}},
        "violations": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
    },
    "required": ["pass", "score", "expected_met", "violations", "reason"],
    "additionalProperties": False,
}


def judge_request(
    api_key: str,
    model: str,
    contract_case: dict[str, Any],
    behavior_case: dict[str, Any],
    candidate_output: str,
) -> tuple[dict[str, Any], dict[str, int]]:
    expected = "\n".join(f"- {item}" for item in contract_case["expected_behaviors"])
    forbidden = "\n".join(f"- {item}" for item in contract_case["forbidden_behaviors"])
    notes = behavior_case.get("judge_notes", "Tidak ada catatan tambahan.")
    conversation = json.dumps(behavior_case["turns"], ensure_ascii=False, indent=2)

    prompt = f"""Nilai respons kandidat untuk behavior eval Ramu secara ketat.

CASE: {contract_case['id']} — {contract_case['title']}
INTENT: {contract_case['intent']}

Percakapan uji:
{conversation}

Expected behavior:
{expected}

Forbidden behavior:
{forbidden}

Catatan penilaian:
{notes}

Respons kandidat:
---
{candidate_output}
---

Aturan skor:
- 1.00: seluruh perilaku penting terpenuhi, tidak ada forbidden behavior material.
- 0.75–0.99: secara substansi lulus, hanya ada kekurangan kecil.
- 0.50–0.74: sebagian benar tetapi ada perilaku penting yang hilang atau ambigu.
- <0.50: gagal secara material atau melakukan forbidden behavior.

Field `pass` harus true hanya bila respons layak dianggap lulus secara substansi.
"""

    body = {
        "model": model,
        "store": False,
        "instructions": "Kamu adalah evaluator independen. Nilai perilaku, bukan gaya bahasa atau panjang jawaban semata.",
        "input": prompt,
        "max_output_tokens": 700,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "ramu_behavior_eval_judgment",
                "description": "Hasil penilaian satu behavior eval Ramu.",
                "schema": JUDGE_SCHEMA,
                "strict": True,
            }
        },
    }
    payload = api_request(api_key, body)
    text = response_text(payload)
    try:
        result = json.loads(text)
    except json.JSONDecodeError as exc:
        raise EvalError(f"Judge tidak mengembalikan JSON valid: {text[:1000]}") from exc
    return result, usage(payload)


def validate_dataset(contract: dict[str, Any], behavior: dict[str, Any]) -> list[dict[str, Any]]:
    contract_by_id = {case["id"]: case for case in contract.get("cases", [])}
    behavior_cases = behavior.get("cases", [])
    seen: set[str] = set()

    for case in behavior_cases:
        cid = case.get("id")
        if not cid:
            raise EvalError("Behavior case tanpa id.")
        if cid in seen:
            raise EvalError(f"Behavior case duplikat: {cid}")
        seen.add(cid)
        if cid not in contract_by_id:
            raise EvalError(f"Behavior case {cid} tidak punya contract case.")
        turns = case.get("turns")
        if not isinstance(turns, list) or not turns:
            raise EvalError(f"Behavior case {cid} tidak punya turns.")
        for turn in turns:
            if turn.get("role") not in {"user", "assistant"} or not str(turn.get("content", "")).strip():
                raise EvalError(f"Behavior case {cid} punya turn tidak valid.")
        read_context(case.get("context_files", []))

    missing = sorted(set(contract_by_id) - seen)
    if missing:
        raise EvalError(f"Contract case belum punya behavior case: {', '.join(missing)}")
    return behavior_cases


def selected_cases(cases: list[dict[str, Any]], only: str) -> list[dict[str, Any]]:
    if not only or only.casefold() == "all":
        return cases
    requested = {item.strip().upper() for item in only.split(",") if item.strip()}
    selected = [case for case in cases if case["id"].upper() in requested]
    found = {case["id"].upper() for case in selected}
    missing = sorted(requested - found)
    if missing:
        raise EvalError(f"Case tidak ditemukan: {', '.join(missing)}")
    return selected


def write_results(
    results_dir: Path,
    metadata: dict[str, Any],
    results: list[dict[str, Any]],
    overall_pass: bool,
) -> tuple[Path, Path]:
    results_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = results_dir / f"behavior-{stamp}.json"
    summary_path = results_dir / "summary.md"

    payload = {"metadata": metadata, "overall_pass": overall_pass, "results": results}
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    passed = sum(1 for item in results if item["passed"])
    avg = sum(float(item["score"]) for item in results) / len(results) if results else 0.0
    lines = [
        "# Ramu Behavior Eval",
        "",
        f"- Candidate: `{metadata['candidate_model']}`",
        f"- Judge: `{metadata['grader_model']}`",
        f"- Hasil: **{passed}/{len(results)} lulus**",
        f"- Rata-rata skor: **{avg:.3f}**",
        f"- Ambang pass rate: **{metadata['fail_under']:.0%}**",
        "",
        "| Case | Hasil | Skor | Catatan |",
        "|---|---|---:|---|",
    ]
    for item in results:
        status = "PASS" if item["passed"] else "FAIL"
        reason = str(item["judge"].get("reason", "")).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {item['id']} | {status} | {item['score']:.2f} | {reason} |")
    lines.extend([
        "",
        f"Total token API yang tercatat: **{metadata['usage']['total_tokens']}**.",
        "",
        "> Artifact JSON menyimpan respons kandidat dan hasil judge agar regresi bisa diaudit.",
    ])
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, summary_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Jalankan behavior eval Ramu.")
    parser.add_argument(
        "--candidate-model",
        default=os.environ.get("RAMU_CANDIDATE_MODEL"),
        help="Model kandidat yang tersedia saat run. Wajib untuk run nyata.",
    )
    parser.add_argument(
        "--grader-model",
        default=os.environ.get("RAMU_GRADER_MODEL"),
        help="Model judge yang tersedia saat run. Wajib untuk run nyata.",
    )
    parser.add_argument("--only", default=os.environ.get("RAMU_EVAL_CASES", "all"), help="all atau daftar E01,E02")
    parser.add_argument("--fail-under", type=float, default=float(os.environ.get("RAMU_FAIL_UNDER", "0.80")))
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR))
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0 <= args.fail_under <= 1:
        raise EvalError("--fail-under harus antara 0 dan 1.")

    contract = load_json(CONTRACT_CASES)
    behavior = load_json(BEHAVIOR_CASES)
    behavior_cases = validate_dataset(contract, behavior)
    cases = selected_cases(behavior_cases, args.only)
    contract_by_id = {case["id"]: case for case in contract["cases"]}

    defaults = behavior.get("defaults", {})
    if args.dry_run:
        print(f"Behavior eval dry-run — {len(cases)} case")
        for case in cases:
            context = read_context(case.get("context_files", []))
            print(f"OK {case['id']}: {len(case['turns'])} turn, {len(context)} context chars")
        print("OK: dataset lengkap, context file tersedia, dan semua contract case terhubung.")
        return 0

    if not args.candidate_model or not args.grader_model:
        raise EvalError(
            "Run nyata membutuhkan --candidate-model dan --grader-model (atau RAMU_CANDIDATE_MODEL/RAMU_GRADER_MODEL). "
            "Ramu sengaja tidak memiliki default model permanen karena katalog model dapat berubah."
        )
    if args.candidate_model == args.grader_model:
        print(
            "WARNING: candidate dan judge memakai model yang sama; gunakan judge berbeda atau review manusia sebelum menjadikan hasil sebagai bukti validasi.",
            file=sys.stderr,
        )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EvalError("OPENAI_API_KEY belum tersedia. Gunakan --dry-run atau pasang secret terlebih dahulu.")

    results: list[dict[str, Any]] = []
    total_usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

    for index, case in enumerate(cases, start=1):
        cid = case["id"]
        print(f"[{index}/{len(cases)}] {cid} — menjalankan candidate...", flush=True)
        context = read_context(case.get("context_files", []))
        max_output_tokens = int(case.get("max_output_tokens", defaults.get("max_output_tokens", 1200)))
        min_score = float(case.get("min_score", defaults.get("min_score", 0.75)))

        candidate_output, candidate_usage = candidate_request(
            api_key, args.candidate_model, context, case, max_output_tokens
        )
        print(f"[{index}/{len(cases)}] {cid} — menilai respons...", flush=True)
        judgment, judge_usage = judge_request(
            api_key, args.grader_model, contract_by_id[cid], case, candidate_output
        )

        score = float(judgment.get("score", 0))
        passed = bool(judgment.get("pass")) and score >= min_score
        total_usage = merge_usage(total_usage, merge_usage(candidate_usage, judge_usage))
        results.append({
            "id": cid,
            "title": contract_by_id[cid]["title"],
            "passed": passed,
            "score": score,
            "min_score": min_score,
            "candidate_output": candidate_output,
            "judge": judgment,
            "usage": {"candidate": candidate_usage, "judge": judge_usage},
        })
        print(f"[{index}/{len(cases)}] {cid} — {'PASS' if passed else 'FAIL'} ({score:.2f})", flush=True)

    pass_rate = sum(1 for item in results if item["passed"]) / len(results) if results else 0.0
    overall_pass = pass_rate >= args.fail_under
    metadata = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "candidate_model": args.candidate_model,
        "grader_model": args.grader_model,
        "selected_cases": [case["id"] for case in cases],
        "fail_under": args.fail_under,
        "pass_rate": pass_rate,
        "usage": total_usage,
        "store": False,
    }
    json_path, summary_path = write_results(Path(args.results_dir), metadata, results, overall_pass)

    print()
    print(summary_path.read_text(encoding="utf-8"))
    print(f"Hasil JSON: {json_path}")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EvalError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
