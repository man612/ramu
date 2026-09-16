<p align="center">
  <img src=".github/assets/hero-light.svg#gh-light-mode-only" alt="Ramu — structured learning workspace for ChatGPT Projects" width="100%">
  <img src=".github/assets/hero-dark.svg#gh-dark-mode-only" alt="Ramu — structured learning workspace for ChatGPT Projects" width="100%">
</p>

<p align="center">
  <a href="README.md">Bahasa Indonesia</a> · <strong>English</strong>
</p>

<p align="center">
  <strong>Structured learning workspace for ChatGPT Projects.</strong><br>
  One course, one Project, with context, sources, and learning behavior that stay organized over time.
</p>

<p align="center">
  <a href="https://man612.github.io/ramu/"><strong>Open Ramu</strong></a>
  ·
  <a href="https://man612.github.io/ramu/setup.html">Try one course</a>
  ·
  <a href="starter/README.md">Create a Ramu Starter</a>
  ·
  <a href="docs/LANDASAN-PEMBELAJARAN.md">Learning rationale</a>
</p>

> This English page is a reviewed entry point, not an automatic translation of every document. The Indonesian `README.md` remains the canonical project overview.
> The public website currently remains in Bahasa Indonesia; its navigation links back to this English overview.

## What Ramu is

Ramu prepares one ChatGPT Project for each course. Project Instructions define the baseline behavior, a course pack carries course-specific context, and source registries help track references that may change over time.

The goal is simple: when a course is used for months, you should not need to rebuild the context in every chat. Older material should not silently override newer rules, and the AI should keep following the learning or assignment context that matters now.

The Universitas Terbuka packs in this repository are a real reference implementation, not the architectural boundary of Ramu. For a course that is not in the public catalog, start with [Ramu Starter](starter/README.md). Normal use in ChatGPT Projects does not require the OpenAI API.

The name **Ramu** comes from the Indonesian word *meramu*: combining context, sources, materials, learning rules, and checks into one workspace that is ready to use.

### Why Semester 2 came first

Ramu started as a practical setup for someone close to the maintainer who was already in Semester 2. That became the first pack used in real study. Semester 1 and Semester 3 were added later so the academic path could be represented more completely.

The catalog therefore follows academic order, while the project history preserves the fact that Semester 2 came first.

## How it works

Ramu keeps one course in one Project and separates the workspace into five layers:

| Layer | Role |
|---|---|
| **References** | source registries and official references help distinguish current, older, or still-unverified information |
| **Instructions** | Project Instructions carry baseline rules, tutor/rubric priority, and learning guardrails |
| **Context zone** | one course stays in one Project so files, learner state, assignments, and chat history do not mix unnecessarily |
| **Materials** | the course pack provides course context; BMP, tutor material, rubrics, screenshots, and private files are added through Project Sources when needed |
| **Assessment** | checking, review, learner-state workflow, and behavior evals help test both answers and configuration changes |

## Available reference packs

Ramu currently includes three maintained reference packs for **Universitas Terbuka · Bachelor of Accounting · 2026/2027**:

- **Semester 1 — 18 credits**: 7 course slots, including an official choose-one Religious Education slot based on the student's registered personal data;
- **Semester 2 — 16 credits**: 5 courses;
- **Semester 3 — 20 credits**: 7 courses.

The public site reads pack metadata from the catalog and manifests. Semester 2 remains the default entry point to preserve the original workflow, while the catalog itself is shown in academic order.

## Start with one course

You do not need to prepare a whole semester at once.

1. Open the [Ramu site](https://man612.github.io/ramu/).
2. Choose the relevant pack.
3. Pick one course.
4. Create a ChatGPT Project using the displayed project name.
5. Add the pack's Project Instructions.
6. Upload the course pack as a Project Source.
7. Start using that Project for the course.

If the pattern is useful, add other courses later. Setup progress on the website is stored locally in the browser by pack ID.

For a course outside the catalog, use [Ramu Starter](starter/README.md). If the context is reusable and should become a public community pack, continue with [Create a Pack](docs/CREATE-A-PACK.md).

## Validation

Most repository checks do not require the OpenAI API:

```bash
python scripts/validate_repo.py
python scripts/validate_display_names.py
python scripts/validate_site.py
python scripts/check_source_freshness.py
python scripts/run_behavior_evals.py --dry-run --pack <pack-id>
```

Automated behavior evaluation through an API remains optional QA. It is not required for normal Ramu use or static CI.

## Pack status

Pack status is a versioned snapshot, not a guarantee that an AI model will always answer correctly:

- `source-verified` — primary sources were reviewed; full behavior validation is not claimed;
- `verified` — relevant source and behavior validation were reviewed;
- `community` — a community contribution that has not reached maintained/verified status;
- `experimental` — still being tested;
- `deprecated` — replaced or no longer recommended for new use.

## Project boundaries

Ramu is a learning-workspace configuration and validation project. It is not an answer bank, a replacement for a university LMS, a place to redistribute copyrighted course material, or a promise that an AI model is immune to mistakes or prompt injection.

`maintainer: ramu` means a pack is maintained in this repository. It does **not** mean the pack is published or endorsed by the university. Ramu is independent from Universitas Terbuka, other educational institutions, and OpenAI.

## Contributing

Issues and pull requests are welcome for documentation, source updates, reproducible behavior failures, tooling, and new packs.

Start with the concise English contribution guide: [`CONTRIBUTING.en.md`](CONTRIBUTING.en.md). The canonical detailed guide remains [`CONTRIBUTING.md`](CONTRIBUTING.md).

Also see the [Code of Conduct](CODE_OF_CONDUCT.md), [Security Policy](SECURITY.md), and [Support guide](SUPPORT.md).

## License

Repository code and documentation use the [MIT License](LICENSE). External course materials, university documents, books, and other third-party sources remain subject to their original rights and licenses.
