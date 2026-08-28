# Ramu v0.2.0-beta — Multi-pack Foundation

Public beta Ramu sekarang punya fondasi multi-pack yang tidak lagi mengunci tooling ke Universitas Terbuka S1 Akuntansi Semester 2.

Pack yang tersedia saat release ini tetap **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**. Dukungan multi-pack di release ini berarti arsitekturnya sudah siap menambah semester, program studi, atau institusi lain tanpa mengubah core/tooling; bukan berarti pack akademik lain sudah tersedia.

## Yang berubah

- `packs/index.json` menjadi katalog pack machine-readable.
- Setiap pack memakai manifest self-describing untuk institusi, program, periode, mata kuliah, source dependency, dan eval wiring.
- Website membaca katalog + manifest secara dinamis; tidak lagi hardcode Semester 2 di JavaScript.
- Label periode manusia sekarang eksplisit, misalnya `Semester 2 • AKM I`, bukan `S2 • AKM I` yang dapat disalahartikan sebagai jenjang Magister.
- Core behavior eval dipisahkan dari eval khusus pack sehingga pack baru tidak perlu menyalin seluruh failure mode universal.
- Manual Eval Kit dapat membuat checklist behavior validation untuk diuji langsung di ChatGPT Projects tanpa OpenAI API.
- Source registry sekarang dapat diberi scope global/institusi/pack dan Source Watch menemukan registry tersebut secara otomatis.
- CI menggunakan matrix per pack dan tetap menyediakan final gate bernama `validate`.
- GitHub Actions dependency dipin ke full commit SHA.
- Schema pack/catalog/source/eval ikut dipublish bersama GitHub Pages.

## Tanpa API tetap bisa dipakai dan diuji

OpenAI API bukan dependency Ramu. Mahasiswa tetap memakai ChatGPT Projects seperti biasa, static CI tetap berjalan, Manual Eval Kit tidak membutuhkan secret, dan pilot pengguna dapat dilakukan sekarang.

Automated Behavior Evals melalui API tetap tersedia sebagai lapisan QA tambahan bila suatu saat API key tersedia.

## Existing user

Kalau sudah memiliki Project bernama `S2 • ...`, Project tersebut tidak perlu dibuat ulang hanya karena perubahan naming. Nama dapat diubah menjadi `Semester 2 • ...` bila ingin mengikuti convention baru; course pack dan Project Instructions tetap menjadi bagian yang menentukan workspace Ramu.

## Status validasi

- Static repository validation: aktif.
- Catalog/site/eval wiring: divalidasi CI.
- Source freshness monitoring: aktif.
- Behavior contracts: E01–E16 tersedia sebagai core + pack suite.
- Manual behavior validation dan pilot pengguna: masih menjadi evidence yang perlu dikumpulkan sebelum klaim stabilitas lebih tinggi.
- Automated API behavior benchmark: opsional dan belum menjadi syarat release ini.

Ramu tetap **public beta** dan tidak mengklaim semua keluaran model selalu akurat atau kebal prompt injection.
