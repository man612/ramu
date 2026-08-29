# Changelog

Semua perubahan penting pada Ramu dicatat di file ini.

Formatnya mengikuti prinsip [Keep a Changelog](https://keepachangelog.com/) dan versi mengikuti [Semantic Versioning](https://semver.org/). Karena Ramu masih public beta, versi `0.x` tetap dapat berubah cukup cepat; setiap release tetap harus menjadi snapshot yang jelas dan tidak dipindahkan diam-diam ke commit lain.

## [Unreleased]

Belum ada perubahan produk yang dijadwalkan untuk release berikutnya.

## [0.2.1-beta] - 2026-08-29

### Changed

- Copy homepage dan halaman setup dibuat lebih langsung dan tidak terlalu editorial/marketing.
- Native browser `<select>` untuk pack diganti custom pack picker dengan keyboard navigation, focus state, `aria-expanded`, `aria-selected`, dan listbox semantics.
- Bila katalog hanya berisi satu pack, pack picker tampil sebagai field statis; pada mobile, menu multi-pack memakai panel yang lebih sesuai untuk touch interaction.
- Petunjuk upload source dibuat lebih defensif terhadap perubahan label UI ChatGPT dan tidak lagi bergantung pada label `Add from library`.
- Overall visual scale desktop dipadatkan sekitar 10–15% melalui ukuran layout aktual, bukan browser zoom atau `transform: scale()`; mobile tetap mempertahankan ukuran baca dan touch target yang nyaman.
- Site regression guard sekarang menolak native pack `<select>` dan beberapa copy lama yang sengaja dihapus.

### Validation

- `Validate Ramu` dan downstream `Deploy Pages` berhasil untuk release snapshot `036a970bfa49a1e8318444e61c6eefd646107bb0`.
- Tidak ada perubahan data akademik, course pack, behavior contract, critical eval, atau arsitektur multi-pack pada patch ini.

## [0.2.0-beta] - 2026-08-29

### Added

- Arsitektur **catalog-driven multi-pack** melalui `packs/index.json` dan `manifest.json` yang self-describing.
- Schema untuk pack catalog, manifest, source registry, eval contracts, behavior eval, **manual ChatGPT Projects evidence**, dan **aggregate pilot evidence**.
- **JSON Schema Draft 2020-12 validation nyata** di CI: schema Ramu diperiksa terhadap dialect/meta-schema dan seluruh katalog/manifest/registry/eval serta published pilot summary divalidasi terhadap schema yang dipublish.
- Stable machine identity `institution_id` + `program_id`, terpisah dari label manusia, beserta cross-file identity gate untuk katalog, manifest, scoped registry, dan eval suite.
- Scoped source registry agar source global/runtime terpisah dari source institusi/program/pack.
- **Claim-level source governance** dengan status, evidence locator, claim review interval, dan fallback operasional untuk konflik dokumentasi resmi.
- **Composable eval suites** dengan urutan `core → institution → program → pack` agar failure mode reusable tidak perlu dicopy ke setiap periode.
- **Manual Eval Kit** untuk membuat checklist behavior validation tanpa OpenAI API, termasuk provenance suite dan critical/must-pass status tiap case.
- **Structured manual Projects evidence** melalui `scripts/manual_eval_evidence.py`: template terikat pack/version/contract/revision, runtime/harness metadata, per-case result, privacy contract, automatic overall calculation, dan semantic validation terhadap contract saat ini.
- Regression proof yang memastikan full manual evidence sehat dapat PASS, critical failure memblokir PASS, subset tidak dapat menjadi full-validation PASS, metadata contract yang dimanipulasi ditolak, dan evidence yang mengaku memuat transcript mentah ditolak schema.
- **Aggregate pilot evidence** melalui `scripts/pilot_evidence.py`: sample target, protocol checks, funnel peserta agregat, time-to-first-value buckets, failure categories, sanitized feedback themes, regression linkage, privacy contract, calculated metrics, readiness, dan limitations.
- Pilot readiness hanya memiliki `INCOMPLETE`, `INSUFFICIENT_SAMPLE`, `BLOCKED`, atau `REVIEW_READY`; tooling tidak mempunyai status `PASS`/`STABLE` otomatis.
- Regression proof pilot yang menguji healthy review-ready summary, critical blocker, sample minimum, invalid protocol, tampered metrics, impossible participant funnel, dan raw-transcript privacy violation.
- `evidence/pilots/` sebagai lokasi khusus sanitized aggregate summary yang memang sengaja dipublish; CI memvalidasi seluruh `*.json` di sana.
- CI matrix yang melakukan dry-run eval wiring untuk setiap pack yang terdaftar.
- **Synthetic multi-pack foundation proof** yang membangun repo sementara dengan dua institusi, dua program, `Semester 2`, `Trimester 1`, program-level suite, serta positive/negative identity cases tanpa mempublish pack palsu ke katalog utama.
- Static site contract untuk mencegah front-end kembali hardcode ke satu pack.
- Metadata periode generic `period_id` + `period_label` agar tooling tidak mengasumsikan semua institusi memakai semester.
- Validator nama Project yang memastikan label manusia konsisten dengan `period_label`.
- **Eval trust-boundary regression** yang memastikan Project Instructions tetap berada pada authority `instructions`, reference/course/source content tetap user-level untrusted input, dan candidate output tidak masuk ke judge instructions.
- **Critical eval gate**: case integritas/security tertentu dapat ditandai `critical: true` dan wajib lulus terlepas dari aggregate pass rate.
- Regression test yang membuktikan pass rate `13/16 = 81.25%` tetap gagal bila ada critical FAIL, serta memastikan Manual Eval Kit mewarisi semantics critical dari contract yang sama.
- **CI/Pages contract regression** yang mencegah main validation kembali memakai path allowlist atau Pages kembali deploy langsung tanpa validated SHA.
- Dependabot weekly untuk immutable GitHub Actions pins dan dependency validation Python.

### Changed

- `packs/index.json` naik ke **v3**: field universal `semester` sudah diganti `period_id`, dan setiap entry sekarang membawa `institution_id` + `program_id` sebagai identity mesin.
- Manifest pack awal naik ke **`schema_version: 4`** untuk kontrak identity + period metadata; `pack_version`/`contract_version` tidak berubah karena course content dan behavior contract tidak berubah.
- Scoped source registry sekarang wajib membawa identity sesuai scope; registry global tidak membawa identity institusi/program/pack.
- Global source registry OpenAI naik ke **v2** dan sekarang mencatat claim-level evidence. ChatGPT Release Notes ditambahkan sebagai source resmi untuk kronologi perubahan produk.
- Source freshness checker sekarang memeriksa umur review claim, evidence source IDs, dan fallback `operational_policy` untuk claim conflicted—bukan hanya umur/reachability source.
- Review OpenAI 29 Agustus 2026 mencatat dua unresolved official-doc conflicts: **Study Mode di Projects** dan **perubahan memory existing Project**. Ramu memakai fallback yang tidak menjadikan keduanya dependency runtime.
- Setup site dibuat defensif terhadap variasi/rollout UI ChatGPT: Project baru memilih Project-only memory sejak awal; Project lama mencoba Project settings → Memory dan membuat Project baru bila opsi belum tersedia.
- Setup tidak lagi menjanjikan per-course Project Instructions override yang belum ada di schema dan tidak lagi bergantung pada label `Add from library`; label Project Sources diperlakukan sebagai UI yang dapat berubah.
- `scope_ref` eval bukan lagi string bebas: institution harus cocok ke `institution_id`, program ke `program_id`, dan pack ke pack `id`.
- Website Ramu sekarang membaca katalog dan manifest secara dinamis; tidak lagi memiliki `PACK_BASE` Semester 2 ataupun fallback `Semester ${...}` di JavaScript.
- Behavior eval runner memilih pack melalui `--pack <pack-id>` dan menggabungkan ordered `eval_suites` dari manifest, bukan fixed `core + pack`.
- Automated candidate eval sekarang memisahkan **Project Instructions** dari reference material sesuai trust boundary Responses API; course/source/context tidak lagi digabung ke `instructions`.
- LLM judge sekarang memperlakukan candidate output, conversation, dan judge notes sebagai **untrusted evidence**, dengan evaluator instructions yang melarang embedded instruction mengubah rubric/verdict.
- Overall automated eval PASS sekarang membutuhkan pass rate memenuhi threshold **dan** tidak ada critical case yang gagal.
- Core critical set awal: `E01` (jangan mengarang data), `E05` (sitasi palsu), `E08` (larangan AI pada submission), dan `E13` (prompt injection/secret).
- Manual Eval Kit sekarang meng-upload **checklist + JSON evidence template**. Template selalu dimulai `INCOMPLETE`/`NOT_RUN`; subset tetap `INCOMPLETE` walaupun seluruh selected case PASS.
- Manual evidence individual disimpan lokal/private secara default melalui `evals/manual/results/` yang di-ignore Git; raw transcript, data pribadi, dan credential tidak menjadi payload evidence publik.
- Manual Eval Kit menandai critical case dan menganggap satu critical FAIL sebagai blocker overall PASS; `--output` checklist juga aman menunjuk path di luar repository.
- Pilot plan sekarang memakai aggregate evidence workflow. Participant-level row, direct identifier, raw transcript, exact assignment content, dan credential dilarang dari published pilot evidence.
- Pilot metrics/readiness dihitung tooling dari aggregate counts; impossible funnel, time-to-first-value total yang tidak konsisten, atau metrics/readiness yang diedit manual ditolak validation.
- Open reproducible critical pilot regression membuat readiness `BLOCKED`; `REVIEW_READY` hanya berarti evidence cukup lengkap untuk review manusia, bukan klaim stabilitas/statistik/efektivitas.
- Regression case E14 konflik source pusat-vs-regional dipindahkan menjadi suite tingkat Universitas Terbuka agar dapat dipakai ulang oleh pack UT lain.
- Validator period metadata memastikan `period_id` machine-safe dan sama antara katalog/manifest; site validator melarang asumsi `item.semester`/`manifest.semester` kembali muncul.
- Validator eval memastikan core berada di awal, pack berada di akhir, scope tidak mundur, `scope_ref` cocok, ID case unik setelah merge, dan contract/behavior tetap berpasangan.
- Validation tooling mendukung `RAMU_REPO_ROOT` untuk fixture/test repo sementara; penggunaan normal tetap memakai root repository aktual.
- `validate_display_names.py` memakai shared repository root helper agar ikut dapat diuji terhadap fixture sintetis.
- **Validate Ramu sekarang berjalan pada setiap push ke `main`**, termasuk docs/release/workflow changes; push validation tidak lagi dibatasi `paths:`.
- **Deploy Pages sekarang downstream dari successful `Validate Ramu` main-push** dan checkout `workflow_run.head_sha`, sehingga SHA yang diterbitkan persis SHA yang divalidasi.
- Dependency GitHub Actions tetap dipin ke full commit SHA dan direfresh ke current major releases: checkout v7.0.1, setup-python v7.0.0, upload-artifact v7.0.1, configure-pages v6.0.0, upload-pages-artifact v5.0.0, dan deploy-pages v5.0.0.
- Nama Project untuk pack awal berubah dari bentuk ambigu seperti `S2 • AKM I` menjadi `Semester 2 • AKM I`.
- UI katalog/setup menggunakan `period_label` dari metadata, bukan membentuk label periode sendiri.

### Notes

- Tidak ada API yang dibutuhkan untuk memakai Ramu, menjalankan static CI, membuat Manual Eval Kit + manual evidence template, synthetic multi-pack proof, trust-boundary regression, critical-gate regression, CI/Pages contract regression, source/claim freshness validation, atau menyiapkan/memvalidasi pilot aggregate evidence.
- `jsonschema[format]` adalah dependency **validation/dev only**, bukan dependency runtime mahasiswa/site.
- Automated Behavior Evals dengan API tetap tersedia sebagai QA tambahan dan bukan syarat public beta.
- Responses API automated eval adalah **regression/benchmark approximation**, bukan simulasi identik ChatGPT Projects; manual validation pada Projects asli tetap dibutuhkan untuk product-level evidence.
- Full manual evidence PASS hanya mendukung claim pada runtime/harness/tanggal/pack/contract yang tercatat. Subset regression tidak boleh dipromosikan menjadi full-validation claim.
- Pilot kecil 5–10 pengguna ditujukan untuk menemukan friction/failure dan bukan estimasi statistik populasi atau causal proof hasil belajar.
- Individual manual/pilot data tetap private/local secara default; hanya sanitized aggregate pilot summary yang boleh dipublish setelah review manusia.
- Dependabot hanya mengusulkan dependency update melalui PR; full-SHA action pin dan normal validation/review tetap dipertahankan.
- Pack awal tetap Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027; synthetic Alpha/Beta hanya fixture test dan tidak dipublish sebagai pack pengguna.
- Perubahan metadata/identity/eval/CI/source-governance tooling repository tidak meminta pengguna ChatGPT Project membuat ulang workspace/course pack secara otomatis; fallback existing-Project memory dijelaskan terpisah karena UI produk dapat berbeda.

## [0.1.0-beta] - 2026-08-28

### Added

- Public beta pertama Ramu dengan pack awal **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**.
- Project Instructions dan course pack untuk Perpajakan, AKM I, Manajemen Keuangan, Ekonomi Mikro, dan Manajemen.
- Static repository validation dan source freshness monitoring.
- Behavior contracts E01–E16, termasuk guardrail integritas tugas, source freshness, prompt injection, source conflict, duplicate pack, dan cross-course context.
- MIT License, contributing guide, security policy, code of conduct, issue templates, dan pull request template.
- Onboarding public beta yang memungkinkan pengguna mencoba satu mata kuliah terlebih dahulu.

### Changed

- Behavior eval runner dibuat model-agnostic; candidate/judge dipilih saat runtime dan tidak di-hardcode ke nama model tertentu.
- Source Watch dibuat gagal secara eksplisit untuk network failure ketika mode strict digunakan.

### Known limitations

- Behavior validation aktual belum menjadi klaim penuh pada release ini.
- Pilot pengguna nyata masih diperlukan sebelum Ramu dapat dianggap stabil.

[Unreleased]: https://github.com/man612/ramu/compare/v0.2.1-beta...HEAD
[0.2.1-beta]: https://github.com/man612/ramu/compare/v0.2.0-beta...v0.2.1-beta
[0.2.0-beta]: https://github.com/man612/ramu/compare/v0.1.0-beta...v0.2.0-beta
[0.1.0-beta]: https://github.com/man612/ramu/releases/tag/v0.1.0-beta
