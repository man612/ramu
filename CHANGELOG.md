# Changelog

Semua perubahan penting pada Ramu dicatat di file ini.

Formatnya mengikuti prinsip [Keep a Changelog](https://keepachangelog.com/) dan versi mengikuti [Semantic Versioning](https://semver.org/). Karena Ramu masih public beta, versi `0.x` tetap dapat berubah cukup cepat; setiap release tetap harus menjadi snapshot yang jelas dan tidak dipindahkan diam-diam ke commit lain.

## [Unreleased]

### Added

- Arsitektur **catalog-driven multi-pack** melalui `packs/index.json` dan `manifest.json` yang self-describing.
- Schema untuk pack catalog, manifest, source registry, dan eval cases.
- Scoped source registry agar source global/runtime terpisah dari source institusi.
- Pemisahan behavior eval menjadi reusable `evals/core/` dan eval khusus pack.
- **Manual Eval Kit** untuk membuat checklist behavior validation tanpa OpenAI API.
- CI matrix yang melakukan dry-run eval wiring untuk setiap pack yang terdaftar.
- Static site contract untuk mencegah front-end kembali hardcode ke satu pack.
- Metadata `period_label` agar label periode yang dilihat manusia eksplisit dan dapat mendukung istilah selain semester.
- Validator nama Project yang memastikan label manusia konsisten dengan `period_label`.

### Changed

- Website Ramu sekarang membaca katalog dan manifest secara dinamis; tidak lagi memiliki `PACK_BASE` Semester 2 di JavaScript.
- Behavior eval runner sekarang memilih pack melalui `--pack <pack-id>` dan menggabungkan core + pack eval dari manifest.
- Source freshness checker menemukan registry berdasarkan scope, bukan satu registry global saja.
- Dependency GitHub Actions dipin ke full commit SHA.
- Nama Project untuk pack awal berubah dari bentuk ambigu seperti `S2 • AKM I` menjadi `Semester 2 • AKM I`.
- UI katalog/setup menggunakan `period_label` dari metadata, bukan membentuk label periode sendiri.

### Notes

- Tidak ada API yang dibutuhkan untuk memakai Ramu, menjalankan static CI, membuat Manual Eval Kit, atau melakukan pilot pengguna.
- Automated Behavior Evals dengan API tetap tersedia sebagai QA tambahan dan bukan syarat public beta.
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
