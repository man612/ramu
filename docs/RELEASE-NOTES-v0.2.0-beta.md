# Ramu v0.2.0-beta — Multi-pack & Composable Eval Foundation

Public beta Ramu sekarang punya fondasi multi-pack yang tidak lagi mengunci tooling ke Universitas Terbuka S1 Akuntansi Semester 2, tidak mengasumsikan semua institusi memakai semester, dan tidak lagi mengasumsikan behavior eval selalu hanya `core + pack`.

Pack yang tersedia saat release ini tetap **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**. Dukungan multi-pack di release ini berarti arsitekturnya sudah siap menambah periode akademik, program studi, atau institusi lain tanpa mengubah core/tooling; bukan berarti pack akademik lain sudah tersedia.

## Yang berubah

- `packs/index.json` menjadi katalog pack machine-readable dan naik ke format v2.
- Setiap pack memakai manifest self-describing untuk institusi, program, periode, mata kuliah, source dependency, dan ordered `eval_suites`.
- Metadata periode generic sekarang memakai `period_id` + `period_label`, bukan field universal `semester`.
- Pack UT saat ini menggunakan `period_id: semester-02` dan `period_label: Semester 2`; sistem lain dapat memakai bentuk seperti `trimester-01`, `quarter-fall`, atau `term-02` tanpa mengubah tooling generic.
- Manifest pack UT naik ke `schema_version: 3` untuk kontrak period metadata baru. `pack_version` dan `contract_version` tidak berubah karena course content dan behavior contract tidak berubah.
- Website membaca katalog + manifest secara dinamis dan tidak lagi punya fallback `Semester ${...}` di JavaScript.
- Label periode manusia eksplisit, misalnya `Semester 2 • AKM I`, bukan `S2 • AKM I` yang dapat disalahartikan sebagai jenjang Magister.
- Behavior eval sekarang composable dengan urutan `core → institution → program → pack`; scope institusi/program bersifat opsional.
- Regression case E14 tentang source pusat-vs-regional dipindahkan menjadi suite tingkat **Universitas Terbuka**, sehingga pack UT berikutnya dapat reuse rule tersebut tanpa copy-paste.
- Validator memastikan `period_id` machine-safe dan sama antara katalog/manifest; site validator juga menolak asumsi `item.semester`/`manifest.semester` agar semantic bias tidak kembali.
- Validator eval memastikan core berada di awal, pack berada di akhir, scope tidak mundur, `scope_ref` cocok, ID case tetap unik setelah merge, dan contract/behavior tetap berpasangan.
- Schema eval contracts digeneralisasi dan ditambah schema behavior eval agar format publik sesuai file yang benar-benar dipakai tooling.
- Manual Eval Kit dapat membuat checklist behavior validation untuk diuji langsung di ChatGPT Projects tanpa OpenAI API, termasuk provenance suite tiap case.
- Source registry sekarang dapat diberi scope global/institusi/program/pack dan Source Watch menemukan registry tersebut secara otomatis.
- CI menggunakan matrix per pack dan tetap menyediakan final gate bernama `validate`.
- GitHub Actions dependency dipin ke full commit SHA; workflow lama sudah dipindahkan ke checkout/setup-python Node 24-native.
- Schema pack/catalog/source/eval ikut dipublish bersama GitHub Pages.

## Source produk OpenAI

Dokumentasi produk OpenAI di global source registry direview ulang pada **28 Agustus 2026**. Projects dan Data Controls tetap menjadi source aktif untuk fungsi masing-masing. Dokumentasi Study Mode sekarang eksplisit menyatakan fitur tersebut tidak tersedia di Projects, sehingga Ramu tetap tidak menjadikan Study Mode dependency runtime.

## Tanpa API tetap bisa dipakai dan diuji

OpenAI API bukan dependency Ramu. Mahasiswa tetap memakai ChatGPT Projects seperti biasa, static CI tetap berjalan, Manual Eval Kit tidak membutuhkan secret, dan pilot pengguna dapat dilakukan sekarang.

Automated Behavior Evals melalui API tetap tersedia sebagai lapisan QA tambahan bila suatu saat API key tersedia.

## Existing user

Kalau sudah memiliki Project bernama `S2 • ...`, Project tersebut tidak perlu dibuat ulang hanya karena perubahan naming. Nama dapat diubah menjadi `Semester 2 • ...` bila ingin mengikuti convention baru; course pack dan Project Instructions tetap menjadi bagian yang menentukan workspace Ramu.

Perubahan `semester` → `period_id` hanya menyentuh metadata repository/tooling. Pengguna yang sudah memasang course pack ke ChatGPT Project tidak perlu mengubah file atau membuat ulang Project karena migrasi schema ini.

## Status validasi

- Static repository validation: aktif.
- Catalog/site/eval wiring: divalidasi CI.
- Source freshness monitoring: aktif.
- Behavior contracts: **E01–E16** tetap tersedia dan digabung dari **3 suite** pada pack awal (`core → Universitas Terbuka → Semester 2`).
- Manual behavior validation dan pilot pengguna: masih menjadi evidence yang perlu dikumpulkan sebelum klaim stabilitas lebih tinggi.
- Automated API behavior benchmark: opsional dan belum menjadi syarat release ini.

Ramu tetap **public beta** dan tidak mengklaim semua keluaran model selalu akurat atau kebal prompt injection.
