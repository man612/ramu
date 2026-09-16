# Ramu v0.3.0-beta — Starter, Pack Creation & Runtime Validation

`v0.3.0-beta` memperluas Ramu dari maintained pack yang sudah ada menjadi workflow yang juga dapat dipakai untuk **mata kuliah personal apa pun** dan untuk **membuat draft community pack** tanpa mengorbankan source governance, identity, atau validation contract yang sudah dibangun pada `v0.2.x`.

Release ini juga membawa UT S1 Akuntansi Semester 3, browser-level regression dengan Playwright, source-watch signal yang lebih tepat, onboarding README yang lebih jelas, serta hardening deployment GitHub Pages setelah temuan CodeQL pada privileged checkout boundary.

> Release dianggap benar-benar terbit hanya setelah tag `v0.3.0-beta` dan GitHub Release dibuat dari commit `main` yang sudah lolos validation. Dokumen ini adalah snapshot release notes yang disiapkan untuk tag tersebut.

## Ramu Starter

Ramu sekarang memiliki jalur personal yang tidak membutuhkan public pack atau OpenAI API.

`python scripts/create_starter.py` menghasilkan:

- `PROJECT-INSTRUCTIONS.md` generik untuk satu mata kuliah;
- `COURSE-PACK.txt` dari konteks yang diberikan pengguna;
- `START-HERE.md` untuk setup singkat;
- `starter.json` untuk metadata tooling.

Starter sengaja tidak masuk `packs/` dan membawa trust marker:

```json
"public_pack": false,
"source_verified": false
```

Dengan begitu source yang disebut pengguna tidak berubah status menjadi seolah-olah sudah direview maintainer Ramu. Output default `ramu-starter-*/` juga di-ignore Git untuk mengurangi risiko artefak personal ikut ter-commit secara tidak sengaja.

## Create a Pack

`scripts/create_pack.py` menyediakan scaffold untuk community pack tanpa mengharuskan contributor menulis struktur repository dari nol.

Generator menerima identity institusi/program/periode, daftar course, serta minimal satu source HTTPS yang benar-benar sudah dibaca contributor. Output awal selalu:

```text
status: experimental
maintainer: community
```

Draft default dibuat di `pack-drafts/`, yang di-ignore Git dan berada di luar discovery `packs/**`. Artinya scaffold setengah jadi tidak ikut masuk schema validation, source discovery, site, atau pack matrix sebelum contributor sengaja memindahkannya ke path final dan mendaftarkannya di `packs/index.json`.

Pack-specific eval dimulai dengan `cases: []`. Generator tidak membuat regression case palsu hanya agar draft terlihat lengkap.

## UT S1 Akuntansi Semester 3

Sejak perubahan setelah `v0.2.2-beta`, `main` juga memperoleh pack **UT S1 Akuntansi Semester 3 2026/2027**:

- 7 mata kuliah;
- 20 SKS;
- pack-scoped registry untuk halaman BMP current;
- behavior regression E17–E24;
- source review terhadap katalog/pedoman UT 2026/2027 dan halaman BMP yang relevan;
- current metadata AKM II `EACC4205` BP/BPro dan detail periode lain yang tidak disalin dari metadata lama.

Semester 3 tetap berstatus `source-verified`, bukan `verified`. Full manual behavior validation pada ChatGPT Projects asli dan pilot pengguna nyata tetap dipisahkan sebagai evidence lanjutan.

## Browser-level site validation

Static site contract tetap dipertahankan, tetapi sekarang dilengkapi Playwright + Chromium pada CI.

Browser regression menguji behavior yang tidak cukup dibuktikan dengan pencarian marker source:

- homepage benar-benar merender katalog/manifest aktif;
- custom pack picker dapat dibuka/ditutup lewat keyboard;
- pemilihan pack mengganti manifest melalui query string;
- pack ID tidak dikenal fallback ke default pack;
- halaman setup merender seluruh course;
- progress setup bertahan melalui `localStorage`;
- Project Instructions dapat diambil dari URL yang dirender;
- tombol download benar-benar menghasilkan course pack;
- penolakan write `localStorage` tidak memecahkan interaksi halaman.

Browser job menjadi bagian dari required `validate` gate, bukan best-effort check terpisah.

## Source Watch yang lebih tepat signal-nya

Source registry mendukung:

```json
"reachability_policy": "strict"
```

atau:

```json
"reachability_policy": "advisory"
```

Default tetap `strict`. `advisory` hanya ditujukan untuk source sah yang dapat menolak probe otomatis sehingga failure network dari GitHub Actions bukan signal yang cukup andal.

Failure advisory tetap dicatat sebagai `URL INCONCLUSIVE`, tetapi tidak membuat scheduled watch gagal hanya karena reachability. Freshness semantik tidak dilonggarkan: source/claim yang melewati `review_interval_days` tetap memblokir watch, dan advisory tidak memperbarui `verified_at`/`reviewed_at` secara otomatis.

Source Watch juga melakukan retry terbatas dan regression test membuktikan transient failure dapat pulih sementara persistent strict failure tetap gagal.

Source OpenAI yang relevan direview ulang pada 16 September 2026. Source yang probe-nya stabil tetap `strict`; mode advisory dipertahankan hanya untuk endpoint yang memang terbukti noisy terhadap automated probe.

## Runtime hardening site

Write `localStorage` untuk progress setup sekarang ditangani defensif. Browser/privacy configuration yang menolak storage tidak lagi menyebabkan event handler melempar error. Progress mungkin tidak persisten pada environment tersebut, tetapi setup page tetap berfungsi.

## Onboarding README

README tidak dirombak total. Origin story, urutan lima lapisan, tabel pack, dan struktur utama tetap dipertahankan.

Perubahan onboarding hanya memperjelas beberapa hal penting untuk pembaca baru:

- Ramu Starter sekarang punya shortcut di area atas;
- pack Universitas Terbuka dijelaskan sebagai reference implementation, bukan batas arsitektur Ramu;
- penggunaan dasar Ramu di ChatGPT Projects tidak memerlukan OpenAI API;
- `CODE_OF_CONDUCT.md` ditautkan dari bagian kontribusi.

## Pages deployment security hardening

CodeQL menemukan alert **“Checkout of untrusted code in a privileged context”** pada desain Pages sebelumnya. Workflow deploy saat itu dipicu melalui `workflow_run` lalu checkout `github.event.workflow_run.head_sha` di job yang mempunyai `pages: write` dan `id-token: write`.

Alert tidak di-dismiss. Trust boundary deployment diubah.

Sekarang alurnya:

```text
push main
  → catalog/eval/browser validation
  → validate
  → deploy-pages
  → reusable pages.yml via workflow_call
```

Perubahan penting:

- `.github/workflows/pages.yml` sekarang reusable melalui `workflow_call`;
- deploy hanya dipanggil setelah job `validate` sukses pada `push` ke `main`;
- tidak ada lagi privileged `workflow_run` trigger untuk Pages;
- tidak ada lagi checkout dengan `github.event.workflow_run.head_sha`;
- permission tetap minimum: `contents: read`, `pages: write`, `id-token: write`;
- `tests/test_ci_contract.py` melarang pola `workflow_run` + dynamic checkout tersebut masuk kembali.

Setelah perubahan ini, validation, browser regression, Pages deployment, serta CodeQL Actions/Python/JavaScript-TypeScript berhasil pada `main`.

## Test/tooling hardening

Validation sekarang juga menjalankan:

- `python -m compileall -q scripts tests`;
- regression generator personal Starter;
- regression generator community pack;
- source-watch retry + reachability policy regression;
- Playwright browser regression pada Chromium;
- CI/Pages trust-chain regression.

`requirements-dev.txt` menambahkan Playwright `1.62.0` untuk browser QA.

## Dependency maintenance

GitHub Pages deployment memperbarui immutable pin `actions/deploy-pages` dari v5.0.0 ke v5.0.1. Update tetap menggunakan full commit SHA.

## Yang tidak berubah

Release ini tidak:

- merombak visual/UI/UX website;
- menjadikan OpenAI API dependency penggunaan normal;
- menjadikan Starter sebagai maintained pack;
- otomatis menaikkan community draft menjadi `source-verified` atau `verified`;
- menyalin BMP/materi kuliah berhak cipta ke repository;
- mengklaim semua output AI benar;
- mengklaim full manual validation atau pilot pengguna sudah selesai.

## Validation sebelum tag

Release candidate harus memenuhi semuanya pada commit `main` yang akan ditag:

1. required `validate` hijau, termasuk browser regression;
2. job `deploy-pages / deploy` sukses pada trusted main-push chain yang sama;
3. CodeQL Actions, Python, dan JavaScript/TypeScript selesai tanpa blocker release baru;
4. Source Freshness Watch/source review tidak dimanipulasi hanya untuk membuat release terlihat hijau;
5. `CHANGELOG.md` sudah memindahkan perubahan dari `Unreleased` ke `0.3.0-beta`;
6. tag `v0.3.0-beta` menunjuk tepat ke commit release candidate yang sudah divalidasi;
7. GitHub Release dipublish sebagai pre-release.

---

**Release:** `v0.3.0-beta`  
**Previous release:** `v0.2.2-beta`  
**Channel:** Public Beta / pre-release  
**Focus:** Generic Starter, community pack creation, Semester 3, browser QA, source-watch signal quality, and Pages trust-boundary hardening
