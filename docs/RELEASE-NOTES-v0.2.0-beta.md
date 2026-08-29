# Ramu v0.2.0-beta — Multi-pack, Identity & Evidence Hardening Foundation

Public beta Ramu sekarang punya fondasi multi-pack yang tidak lagi mengunci tooling ke Universitas Terbuka S1 Akuntansi Semester 2, tidak mengasumsikan semua institusi memakai semester, dan mempunyai jalur evidence yang membedakan static proof, manual ChatGPT Projects validation, dan field/pilot evidence.

Pack yang tersedia saat release ini tetap **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**. Dukungan multi-pack di release ini berarti arsitektur dan validation tooling sudah diuji untuk lebih dari satu institusi/program/periode melalui fixture sintetis; bukan berarti pack akademik lain sudah tersedia.

## Yang berubah

- `packs/index.json` menjadi katalog pack machine-readable dan naik ke **format v3**.
- Setiap pack memakai manifest self-describing untuk identity institusi/program, periode, mata kuliah, source dependency, dan ordered `eval_suites`.
- Metadata identity mesin sekarang eksplisit: `institution_id`, `program_id`, dan pack `id` terpisah dari label manusia.
- Metadata periode generic memakai `period_id` + `period_label`, bukan field universal `semester`.
- Pack UT saat ini menggunakan `period_id: semester-02` dan `period_label: Semester 2`; sistem lain dapat memakai `trimester-01`, `quarter-fall`, atau `term-02` tanpa mengubah tooling generic.
- Manifest pack UT naik ke **`schema_version: 4`** untuk kontrak identity + period metadata.
- Website membaca katalog + manifest secara dinamis dan label periode manusia eksplisit, misalnya `Semester 2 • AKM I`, bukan `S2 • AKM I`.
- Behavior eval sekarang composable dengan urutan `core → institution → program → pack`.
- `scope_ref` institution/program/pack divalidasi terhadap identity pack yang sebenarnya.
- Regression case E14 source pusat-vs-regional menjadi suite tingkat Universitas Terbuka agar dapat direuse pack UT berikutnya.
- Source registry dapat diberi scope global/institusi/program/pack dan membawa claim-level evidence.
- JSON Schema Draft 2020-12 benar-benar dijalankan pada schema dan instance repository.
- Manual Projects evidence dan aggregate pilot evidence mempunyai schema + semantic validator sendiri.
- GitHub Actions dependency dipin full commit SHA dan CI/Pages membentuk validated deployment chain.

## Multi-pack proof

CI menjalankan **synthetic multi-pack foundation proof** pada temporary repository, bukan katalog pengguna.

Positive fixture mencakup dua institusi, dua program, dua pack, `Semester 2`, `Trimester 1`, institution/program suites, scoped registries, schema validation, identity validation, display-name validation, pack matrix, dan behavior dry-run.

Negative fixture memastikan gate menolak scope identity lintas institusi, registry identity salah, serta field legacy `semester` pada kontrak generic.

Fixture Alpha/Beta tidak masuk `packs/index.json` utama dan tidak tampil di website Ramu.

## Eval & security hardening

Automated behavior eval sekarang menjaga boundary antara instruksi berwenang dan external/reference content.

- **Project Instructions** berada pada Responses API `instructions`.
- Course pack, source, protocol/context yang digunakan case diberikan sebagai **user-level untrusted reference material**.
- Regression test mencegah reference material kembali masuk ke `instructions`.
- Candidate output, conversation, dan judge notes diperlakukan sebagai **untrusted evidence** pada LLM judge.
- Judge instructions melarang embedded instruction dalam evidence mengubah rubric/verdict.

Hardening ini bukan klaim bahwa prompt injection sudah terselesaikan. Responses API automated eval juga tetap regression/benchmark approximation, bukan simulasi identik ChatGPT Projects.

## Critical / must-pass eval

Aggregate pass rate tidak cukup sendirian. Contract dapat memberi `critical: true`.

Overall automated/manual full run membutuhkan threshold terpenuhi **dan** semua critical case PASS.

Core critical set awal:

- `E01` — jangan mengarang angka/data yang tidak terlihat;
- `E05` — jangan membuat sitasi/DOI/identitas sumber palsu;
- `E08` — hormati instruksi tugas yang melarang AI menghasilkan submission;
- `E13` — jangan mengikuti prompt injection dari Project Source atau membocorkan secret.

Regression test membuktikan **13/16 = 81,25% tetap FAIL** bila ada critical failure.

## Structured manual ChatGPT Projects evidence

Manual Eval Kit sekarang menghasilkan **checklist + `manual-evidence.json` template** tanpa API.

Evidence template mengikat:

- pack/version/contract dan Ramu revision;
- tanggal/runtime ChatGPT Projects;
- plan/model label bila memang terlihat—`unknown` tetap lebih benar daripada menebak;
- app surface dan project memory mode;
- setup/harness checks;
- suite/title/critical metadata setiap E-case;
- hasil `PASS / PARTIAL / FAIL / NOT_RUN`;
- privacy flags, limitations, pass rate, dan critical blockers.

Template selalu mulai `INCOMPLETE + NOT_RUN`. Tooling **tidak pernah menghasilkan PASS otomatis** saat template dibuat.

Full manual PASS hanya mungkin jika seluruh current contract cases dijalankan, setup checks lengkap, threshold terpenuhi, dan semua critical PASS. Subset seperti `E01,E05` tetap `INCOMPLETE` sebagai full-validation claim walaupun seluruh selected case lulus.

Individual evidence berada di `evals/manual/results/` yang Git-ignored. Raw transcript, direct personal data, dan credentials tidak menjadi payload evidence publik.

## Aggregate pilot / field evidence

Pilot 5–10 pengguna sekarang mempunyai contract terstruktur melalui `scripts/pilot_evidence.py` dan `schemas/pilot-summary.schema.json`.

Summary hanya menyimpan agregat:

- jumlah recruited/started/setup completed/first value;
- return-7-day denominator dan numerator;
- multi-course adoption;
- setup tanpa live help;
- time-to-first-value buckets;
- aggregate setup/behavior failure category;
- sanitized feedback themes;
- regression `P001...` dan optional linkage ke behavior case `E..`;
- pack/version/contract/revision, protocol checks, privacy flags, metrics, readiness, dan limitations.

Tidak ada row per peserta pada evidence publik. Schema secara eksplisit melarang direct identifier, participant rows, raw transcripts, exact assignment content, dan credentials.

Tooling menghitung rate/readiness dari count dan menolak impossible funnel, time bucket yang tidak konsisten, atau metrics/readiness yang diedit manual.

Pilot readiness hanya:

- `INCOMPLETE`;
- `INSUFFICIENT_SAMPLE`;
- `BLOCKED`;
- `REVIEW_READY`.

Tidak ada `PASS`, `STABLE`, atau `VALIDATED` otomatis. Open reproducible critical pilot regression membuat summary `BLOCKED`. `REVIEW_READY` hanya berarti evidence agregat cukup lengkap untuk review manusia.

Draft pilot tetap lokal di lokasi Git-ignored. Sanitized aggregate summary yang sengaja dipublish dapat ditempatkan di `evidence/pilots/*.json`, dan CI akan memvalidasi schema serta invariant semantiknya.

Pilot kecil dipakai untuk discovery/friction/failure evidence, **bukan** estimasi statistik populasi atau causal claim peningkatan hasil belajar.

## CI, Pages, dan dependency hardening

- **Validate Ramu berjalan pada setiap push ke `main`**, bukan path allowlist.
- **Deploy Pages menunggu successful `Validate Ramu` main-push** lewat `workflow_run`.
- Pages checkout `workflow_run.head_sha`, yaitu SHA yang benar-benar divalidasi.
- CI punya regression contract terhadap validation/deployment chain tersebut.
- Dependabot mingguan untuk dependency GitHub Actions dan Python validation dependency.
- Full-SHA action pins tetap dipertahankan; update datang melalui PR dan tetap harus direview.
- CI sekarang juga menguji manual evidence contract, pilot aggregate evidence contract, dan setiap published pilot summary.

## Product drift & source governance

Global OpenAI registry direview pada **29 Agustus 2026** dan naik ke format v2. ChatGPT Release Notes ditambahkan sebagai source resmi untuk kronologi perubahan produk.

Ramu membedakan freshness **source** dan freshness **claim**. Claim dapat mempunyai evidence dari beberapa source, status sendiri, review interval sendiri, dan operational fallback.

Dua official-doc conflict yang masih dicatat pada release candidate:

1. **Study Mode di Projects** — artikel Study Mode dan artikel Projects belum konsisten.
2. **Memory existing Project** — guidance/release notes terbaru dan wording FAQ lama belum sepenuhnya konsisten.

Fallback Ramu tidak bergantung pada Study Mode. Untuk memory, Project baru memilih Project-only sejak awal; Project lama mencoba Project settings → Memory dan membuat Project baru bila opsi belum tersedia.

Source Watch memeriksa claim evidence source IDs, umur review claim, dan operational policy untuk conflicted claim; URL hidup sendiri tidak dianggap bukti fakta masih current.

## Tanpa API tetap bisa dipakai dan diuji

OpenAI API bukan dependency Ramu.

Tanpa API, repository tetap dapat menjalankan:

- static/schema/identity validation;
- synthetic multi-pack proof;
- eval trust-boundary regression;
- critical gate regression;
- Manual Eval Kit + structured manual evidence;
- source/claim freshness validation;
- pilot aggregate evidence preparation/validation;
- CI/Pages chain;
- pilot pengguna nyata.

Automated Behavior Evals melalui API tetap tersedia sebagai QA tambahan jika suatu saat API key tersedia.

## Existing user

Project lama bernama `S2 • ...` tidak perlu dibuat ulang hanya karena naming. Nama dapat diubah menjadi `Semester 2 • ...` bila ingin mengikuti convention baru.

Perubahan `semester → period_id`, identity, eval/CI/source governance, dan evidence tooling berada di metadata/tooling repository. Pilihan Project-only memory tetap mengikuti availability UI akun/app seperti dijelaskan pada setup fallback.

## Status validasi

- JSON Schema validation: aktif.
- Static semantic/cross-file validation: aktif.
- Machine identity validation: aktif.
- Synthetic multi-pack + non-semester proof: aktif.
- Eval trust-boundary regression: aktif tanpa API.
- Critical must-pass gate regression: aktif tanpa API.
- Structured manual evidence contract regression: aktif tanpa API.
- Aggregate pilot evidence contract regression: aktif tanpa API.
- Published pilot aggregate validation: aktif bila summary dipublish.
- CI/Pages deployment-chain regression: aktif.
- Validate: wajib setiap main push.
- Pages: downstream dari successful validated main push.
- Source + claim freshness monitoring: aktif.
- Behavior contracts: **E01–E16** dari **3 suite** pada pack awal (`core → Universitas Terbuka → Semester 2`).
- Core critical must-pass: **E01, E05, E08, E13**.
- Manual Projects **evidence infrastructure siap**, tetapi full E01–E16 manusia nyata masih perlu dijalankan/direview.
- Pilot **evidence infrastructure siap**, tetapi pilot 5–10 pengguna nyata masih perlu dijalankan.
- Automated API behavior benchmark: opsional.

Ramu tetap **public beta** dan tidak mengklaim semua keluaran model selalu akurat, prompt injection sudah selesai, dokumentasi produk tidak akan berubah, manual run tunggal membuktikan universal behavior, atau pilot kecil membuktikan efektivitas populasi.
