# Contributing to Ramu

[Detailed guide in Bahasa Indonesia](CONTRIBUTING.md) · **English summary**

This page is a reviewed English entry point for contributors. `CONTRIBUTING.md` remains the canonical detailed guide; this file focuses on the rules and workflow most contributors need before opening an issue or pull request.

## Before you start

Please keep these rules intact:

1. Do not commit paid BMP modules, answer keys, or other material that cannot be redistributed.
2. Academic facts need appropriate official sources.
3. Distinguish verified facts, assumptions, community experience, and design decisions.
4. Do not lock the runtime to one AI model name.
5. A pack maintained in this repository is still independent; it is not an official university pack.
6. Use clear human-facing period labels such as `Semester 3`, not ambiguous abbreviations such as `S3`.
7. Keep `institution_id`, `program_id`, and pack IDs stable after they are in use.

## Useful contributions

Good contributions include documentation/onboarding fixes, source updates, reproducible behavior regression cases, validators and tooling, Project Instructions/course-pack improvements, or new institution/program/period packs.

For a private single-course setup, start with [Ramu Starter](starter/README.md). A personal Starter should not automatically become a public pack.

## Creating a public pack

The recommended scaffold path is [`scripts/create_pack.py`](scripts/create_pack.py). It creates an `experimental` + `community` draft under `pack-drafts/`, outside public discovery, and does not invent evaluation evidence.

Before proposing a public pack, review its identity, manifest, Project Instructions, source registry, course files, and eval scope. Add it to `packs/index.json` only after the draft is ready for public discovery.

Prefer the narrowest reusable eval scope:

```text
core → institution → program → pack
```

Do not duplicate the same regression case across many packs when the behavior belongs at a broader scope.

## Local validation

Install the development dependencies, then run the repository checks that match your change:

```bash
python -m pip install -r requirements-dev.txt
python -m compileall -q scripts tests
python scripts/validate_schemas.py
python scripts/validate_repo.py
python scripts/validate_scope_identities.py
python scripts/validate_display_names.py
python scripts/validate_site.py
python scripts/check_source_freshness.py
python scripts/run_behavior_evals.py --dry-run --pack <pack-id>
```

Browser regression also needs Playwright Chromium:

```bash
python -m playwright install chromium
python tests/test_site_browser.py
```

CI installs browser dependencies automatically and includes the browser job in the required validation gate.

## Pull requests

A useful PR explains the problem, the scope that changed, the sources used for current academic facts, how the result was verified, and what remains untested or risky.

If a change affects guardrails, source routing, learner state, or tutor behavior, add or update an eval at the appropriate scope.

The review goal is not maximum documentation. The goal is a change that can be understood and tested again: clear sources, stable identity, consistent period metadata, simple setup, and a reproducible place for important failure modes.
