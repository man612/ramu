#!/usr/bin/env python3
"""Regression contract untuk validation trigger, Pages gate, dan dependency update config."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(text: str, marker: str, label: str) -> None:
    if marker not in text:
        raise AssertionError(f"{label} kehilangan marker wajib: {marker!r}")


def forbid(text: str, marker: str, label: str) -> None:
    if marker in text:
        raise AssertionError(f"{label} memuat marker terlarang: {marker!r}")


def main() -> int:
    validate = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
    pages = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    dependabot = (ROOT / ".github/dependabot.yml").read_text(encoding="utf-8")

    # Main validation must not be bypassable merely because a file falls outside a path allowlist.
    require(validate, "  push:\n    branches: [main]", "Validate workflow")
    forbid(validate, "    paths:\n", "Validate workflow")
    require(validate, "name: validate", "Validate workflow")
    require(validate, "Prove CI and Pages gate contract", "Validate workflow")

    # Pages must be downstream of the completed Validate workflow, never a direct push deploy.
    require(pages, "  workflow_run:", "Pages workflow")
    require(pages, '    workflows: ["Validate Ramu"]', "Pages workflow")
    require(pages, "    types: [completed]", "Pages workflow")
    forbid(pages, "  push:\n", "Pages workflow")
    forbid(pages, "  workflow_dispatch:\n", "Pages workflow")
    require(pages, "github.event.workflow_run.conclusion == 'success'", "Pages workflow")
    require(pages, "github.event.workflow_run.event == 'push'", "Pages workflow")
    require(pages, "github.event.workflow_run.head_branch == 'main'", "Pages workflow")
    require(pages, "ref: ${{ github.event.workflow_run.head_sha }}", "Pages workflow")

    # Dependency bots should update immutable action SHAs / pinned validation deps through reviewed PRs.
    require(dependabot, 'package-ecosystem: "github-actions"', "Dependabot config")
    require(dependabot, 'package-ecosystem: "pip"', "Dependabot config")
    require(dependabot, 'interval: "weekly"', "Dependabot config")

    print("CI/Pages contract regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
