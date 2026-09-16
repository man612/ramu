# Ramu v0.3.0-beta — Starter, Pack Creation & Runtime Validation

> **Draft release notes.** Dokumen ini disiapkan untuk release candidate berikutnya. Jangan menganggap `v0.3.0-beta` sudah terbit sebelum tag/release GitHub benar-benar dibuat dari `main` yang lolos validation.

`v0.3.0-beta` memperluas Ramu dari maintained pack yang sudah ada menjadi workflow yang juga dapat dipakai untuk **mata kuliah personal apa pun** dan untuk **membuat draft community pack** tanpa mengorbankan source governance, identity, atau validation contract yang sudah dibangun pada `v0.2.x`.

Release candidate ini juga membawa UT S1 Akuntansi Semester 3 yang sejak `v0.2.2-beta` sudah masuk `main`, serta menambah browser-level regression agar site tidak hanya lolos static marker checks.

## Ramu Starter

Ramu sekarang memiliki jalur personal yang tidak membutuhkan public pack atau OpenAI API.

`python scripts/create_starter.py` menghasilkan:

- `PROJECT-INSTRUCTIONS.md` generik untuk satu mata kuliah;
- `COURSE-PACK.txt` dari konteks yang diberikan pengguna;
- `START-HERE.md` untuk setup singkat;
- `starter.json` untuk metadata tooling.

Starter sengaja tidak masuk `packs/` dan selalu membawa trust marker:

```json
"public_pack": false,
"source_verified": false
```

Dengan begitu source yang disebut pengguna tidak berubah status menjadi seolah-olah sudah direview maintainer Ramu.

## Create a Pack

`scripts/create_pack.py` menyediakan scaffold untuk community pack tanpa mengharuskan contributor menulis struktur repository dari nol.

Generator menerima identity institusi/program/periode, daftar course, serta minimal satu source HTTPS yang benar-benar sudah dibaca contributor. Output awal selalu:

```text
status: experimental
maintainer: community
```

Draft default dibuat di `pack-drafts/`, yang di-ignore Git dan berada di luar discovery `packs/**`. Artinya scaffold setengah jadi tidak ikut masuk schema validation, source discovery, site, atau pack matrix sebelum contributor sengaja memindahkannya ke path final dan mendaftarkannya di `packs/index.json`.

Pack-specific eval dimulai dengan `cases: []`. Generator tidak membuat regression case palsu hanya agar draft terlihat lengkap.

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

Browser job menjadi bagian dari required `validate` gate. Pages tetap hanya berjalan setelah `Validate Ramu` sukses pada push `main` dan tetap checkout SHA upstream yang sama.

## Source Watch yang lebih tepat signal-nya

Source registry sekarang dapat mendeklarasikan:

```json
"reachability_policy": "strict"
```

atau:

```json
"reachability_policy": "advisory"
```

Default untuk entry lama tetap `strict`.

`advisory` ditujukan untuk source sah yang dapat menolak probe otomatis sehingga failure network dari GitHub Actions bukan signal yang cukup andal. Failure advisory tetap dicatat sebagai `URL INCONCLUSIVE`, tetapi tidak membuat scheduled watch gagal hanya karena reachability dan tidak membuka issue sendiri.

Freshness semantik tidak dilonggarkan: source/claim yang melewati `review_interval_days` tetap memblokir watch, dan advisory tidak memperbarui `verified_at`/`reviewed_at` secara otomatis.

OpenAI Help Center pada registry global menggunakan advisory setelah scheduled probes berulang kali menerima HTTP 403 walaupun masalahnya merupakan automated reachability, bukan evidence bahwa claim produk berubah.

## Runtime hardening site

Write `localStorage` untuk progress setup sekarang ditangani defensif. Browser/privacy configuration yang menolak storage tidak lagi menyebabkan event handler melempar error. Progress mungkin tidak persisten pada environment tersebut, tetapi setup page tetap berfungsi.

## Test/tooling hardening

Validation sekarang juga menjalankan:

- `python -m compileall -q scripts tests`;
- regression generator personal Starter;
- regression generator community pack;
- source-watch retry + reachability policy regression;
- Playwright browser regression pada Chromium.

`requirements-dev.txt` menambahkan Playwright `1.62.0` untuk browser QA.

## Dependency maintenance

GitHub Pages deployment memperbarui immutable pin `actions/deploy-pages` dari v5.0.0 ke v5.0.1. Update tetap menggunakan full commit SHA.

## UT S1 Akuntansi Semester 3

Sejak release `v0.2.2-beta`, `main` juga memperoleh pack **UT S1 Akuntansi Semester 3 2026/2027**:

- 7 mata kuliah;
- 20 SKS;
- pack-scoped registry untuk halaman BMP current;
- behavior regression E17–E24;
- source review terhadap katalog/pedoman UT 2026/2027 dan halaman BMP yang relevan;
- current metadata AKM II `EACC4205` BP/BPro dan detail periode lain yang tidak disalin dari metadata lama.

Semester 3 tetap berstatus `source-verified`, bukan `verified`.

## Yang tidak berubah

Release candidate ini tidak:

- merombak visual/UI/UX website;
- menjadikan OpenAI API dependency penggunaan normal;
- menjadikan Starter sebagai maintained pack;
- otomatis menaikkan community draft menjadi `source-verified` atau `verified`;
- menyalin BMP/materi kuliah berhak cipta ke repository;
- mengklaim semua output AI benar;
- mengklaim full manual validation atau pilot pengguna sudah selesai.

## Validation sebelum publish

Sebelum release benar-benar diterbitkan:

1. merge perubahan melalui PR ke `main`;
2. pastikan required `validate` hijau pada SHA `main` tersebut, termasuk browser job;
3. pastikan downstream Deploy Pages berhasil untuk SHA yang sama;
4. review Source Freshness Watch dan source/claim yang memang jatuh tempo;
5. pindahkan item `Unreleased` di `CHANGELOG.md` ke `0.3.0-beta`;
6. buat tag `v0.3.0-beta` pada SHA yang sudah divalidasi;
7. publish sebagai pre-release.

---

**Planned release:** `v0.3.0-beta`  
**Previous release:** `v0.2.2-beta`  
**Channel:** Public Beta  
**Focus:** Generic Starter, community pack creation, browser QA, source-watch signal quality
