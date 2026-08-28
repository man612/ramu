# Changelog

Semua perubahan penting pada Ramu dicatat di file ini.

Formatnya mengikuti prinsip [Keep a Changelog](https://keepachangelog.com/) dan versi mengikuti [Semantic Versioning](https://semver.org/). Karena Ramu masih public beta, versi `0.x` tetap dapat berubah cukup cepat; setiap release tetap harus menjadi snapshot yang jelas dan tidak dipindahkan diam-diam ke commit lain.

## [Unreleased]

### Added

- Arsitektur **catalog-driven multi-pack** melalui `packs/index.json` dan `manifest.json` yang self-describing.
- Schema untuk pack catalog, manifest, source registry, eval contracts, dan behavior eval.
- Scoped source registry agar source global/runtime terpisah dari source institusi/program/pack.
- **Composable eval suites** dengan urutan `core → institution → program → pack` agar failure mode reusable tidak perlu dicopy ke setiap periode.
- **Manual Eval Kit** untuk membuat checklist behavior validation tanpa OpenAI API, termasuk provenance suite tiap case.
- CI matrix yang melakukan dry-run eval wiring untuk setiap pack yang terdaftar.
- Static site contract untuk mencegah front-end kembali hardcode ke satu pack.
- Metadata periode generic `period_id` + `period_label` agar tooling tidak mengasumsikan semua institusi memakai semester.
- Validator nama Project yang memastikan label manusia konsisten dengan `period_label`.

### Changed

- `packs/index.json` naik ke v2 dan mengganti field universal `semester` dengan `period_id` machine-safe.
- Manifest pack awal naik ke `schema_version: 3`; `pack_version`/`contract_version` tidak berubah karena course content dan behavior contract tidak berubah.
- Website Ramu sekarang membaca katalog dan manifest secara dinamis; tidak lagi memiliki `PACK_BASE` Semester 2 ataupun fallback `Semester ${...}` di JavaScript.
- Behavior eval runner sekarang memilih pack melalui `--pack <pack-id>` dan menggabungkan ordered `eval_suites` dari manifest, bukan fixed `core + pack`.
- Regression case E14 konflik source pusat-vs-regional dipindahkan menjadi suite tingkat Universitas Terbuka agar dapat dipakai ulang oleh pack UT lain.
- Validator period metadata memastikan `period_id` machine-safe dan sama antara katalog/manifest; site validator melarang asumsi `item.semester`/`manifest.semester` kembali muncul.
- Validator eval memastikan core berada di awal, pack berada di akhir, scope tidak mundur, `scope_ref` cocok, ID case unik setelah merge, dan contract/behavior tetap berpasangan.
- Source freshness checker menemukan registry berdasarkan scope, bukan satu registry global saja.
- Dependency GitHub Actions dipin ke full commit SHA; workflow lama diperbarui ke checkout/setup-python v6 yang Node 24-native.
- Nama Project untuk pack awal berubah dari bentuk ambigu seperti `S2 • AKM I` menjadi `Semester 2 • AKM I`.
- UI katalog/setup menggunakan `period_label` dari metadata, bukan membentuk label periode sendiri.
- Global source registry OpenAI direview ulang pada 28 Agustus 2026. Dokumentasi Study Mode kini dicatat eksplisit sebagai tidak tersedia di Projects, sehingga tetap bukan dependency runtime Ramu.

### Notes

- Tidak ada API yang dibutuhkan untuk memakai Ramu, menjalankan static CI, membuat Manual Eval Kit, atau melakukan pilot pengguna.
- Automated Behavior Evals dengan API tetap tersedia sebagai QA tambahan dan bukan syarat public beta.
- Pack awal tetap Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027; fondasi multi-pack tidak berarti pack periode/program/institusi lain sudah tersedia.
- Perubahan metadata `semester` → `period_id` tidak meminta pengguna ChatGPT Project membuat ulang workspace/course pack; ini adalah migrasi kontrak repository/tooling.
- Perubahan di bagian `Unreleased` di atas adalah kandidat utama untuk release berikutnya, **`v0.2.0-beta`**.

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

[Unreleased]: https://github.com/man612/ramu/compare/v0.1.0-beta...HEAD
[0.1.0-beta]: https://github.com/man612/ramu/releases/tag/v0.1.0-beta
