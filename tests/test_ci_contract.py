#!/usr/bin/env python3
"""Regression contract untuk validation trigger, browser gate, Pages gate, dan dependency update config."""

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

    # Browser regression is a real gate, not a best-effort side job.
    require(validate, "  browser:\n", "Validate workflow")
    require(validate, "python -m playwright install --with-deps chromium", "Validate workflow")
    require(validate, "python tests/test_site_browser.py", "Validate workflow")
    require(validate, "needs: [catalog, eval-wiring, browser]", "Validate workflow")
    require(validate, 'test "${{ needs.browser.result }}" = "success"', "Validate workflow")

    # Pages deployment must stay in the trusted main-push chain after validation succeeds.
    require(validate, "  deploy-pages:\n", "Validate workflow")
    require(validate, "needs: validate", "Validate workflow")
    require(validate, "if: github.event_name == 'push' && github.ref == 'refs/heads/main'", "Validate workflow")
    require(validate, "uses: ./.github/workflows/pages.yml", "Validate workflow")
    require(validate, "pages: write", "Validate workflow")
    require(validate, "id-token: write", "Validate workflow")

    # The privileged Pages workflow is reusable only: never accept workflow_run head_sha for checkout.
    require(pages, "  workflow_call:\n", "Pages workflow")
    forbid(pages, "  workflow_run:\n", "Pages workflow")
    forbid(pages, "  push:\n", "Pages workflow")
    forbid(pages, "  workflow_dispatch:\n", "Pages workflow")
    forbid(pages, "github.event.workflow_run", "Pages workflow")
    forbid(pages, "          ref:", "Pages workflow")
    require(pages, "Checkout validated main commit", "Pages workflow")
    require(pages, "pages: write", "Pages workflow")
    require(pages, "id-token: write", "Pages workflow")

    # Dependency bots should update immutable action SHAs / pinned validation deps through reviewed PRs.
    require(dependabot, 'package-ecosystem: "github-actions"', "Dependabot config")
    require(dependabot, 'package-ecosystem: "pip"', "Dependabot config")
    require(dependabot, 'interval: "weekly"', "Dependabot config")

    print("CI/browser/Pages contract regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
