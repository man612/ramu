<p align="center">
  <img src=".github/assets/hero-light.svg#gh-light-mode-only" alt="Ramu — workspace belajar terstruktur untuk ChatGPT Projects" width="100%">
  <img src=".github/assets/hero-dark.svg#gh-dark-mode-only" alt="Ramu — workspace belajar terstruktur untuk ChatGPT Projects" width="100%">
</p>

<p align="center">
  <strong>Workspace belajar terstruktur untuk ChatGPT Projects.</strong><br>
  Satu mata kuliah, satu Project, dengan konteks, sumber, dan pola bantuan yang tetap rapi dari waktu ke waktu.
</p>

<p align="center">
  <a href="https://man612.github.io/ramu/"><strong>Buka Ramu</strong></a>
  ·
  <a href="https://man612.github.io/ramu/setup.html">Coba satu mata kuliah</a>
  ·
  <a href="docs/LANDASAN-PEMBELAJARAN.md">Landasan pembelajaran</a>
  ·
  <a href="evals/manual/README.md">Manual validation</a>
</p>

<p align="center">
  <img alt="GitHub Pages" src="https://img.shields.io/github/actions/workflow/status/man612/ramu/pages.yml?label=pages&style=flat-square">
  <img alt="Validasi Ramu" src="https://img.shields.io/github/actions/workflow/status/man612/ramu/validate.yml?label=contracts&style=flat-square">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-4C6B58?style=flat-square">
  <img alt="Status" src="https://img.shields.io/badge/status-public%20beta-BB8C51?style=flat-square">
</p>

---

## Tentang Ramu

Ramu menyiapkan satu ChatGPT Project untuk setiap mata kuliah. Project Instructions mengatur perilaku dasar, course pack memberi konteks mata kuliah, dan source registry membantu menjaga rujukan yang berubah dari waktu ke waktu.

Tujuannya sederhana: saat sebuah mata kuliah dipakai berbulan-bulan, konteksnya tidak perlu dibangun ulang setiap chat, materi lama tidak mudah bercampur dengan aturan terbaru, dan bantuan AI tetap mengikuti kebutuhan belajar atau tugas yang sedang dikerjakan.

> Nama **Ramu** berasal dari kata *meramu*: menyatukan konteks, sumber, materi, aturan belajar, dan pemeriksaan menjadi satu ruang belajar yang siap dipakai.

### Berawal dari kebutuhan nyata

Ramu awalnya saya buat untuk membantu seseorang yang dekat dengan saya, yang saat itu sudah masuk Semester 2. Karena kebutuhan belajarnya dimulai dari sana, Semester 2 menjadi pack pertama yang benar-benar dipakai. Setelah fondasinya cukup matang, periode lain mulai dilengkapi supaya perjalanan akademiknya bisa ditelusuri dengan lebih rapi.

Karena itu, urutan pack di katalog mengikuti **urutan akademik**, bukan urutan kapan pack tersebut dibuat. Sejarah pengembangannya bisa berbeda dengan urutan semester, dan itu memang wajar untuk proyek yang tumbuh dari kebutuhan nyata.

## Cara kerjanya

Satu mata kuliah ditempatkan di satu Project. Di dalamnya ada beberapa lapisan yang punya tugas berbeda:

| Bagian | Fungsinya |
|---|---|
| **Project Instructions** | aturan dasar saat AI membantu belajar atau mengerjakan tugas |
| **Course pack** | konteks, karakter materi, workflow, dan pemeriksaan khusus mata kuliah |
| **Project Sources** | BMP, materi tutor, rubrik, screenshot, atau file lain yang memang dibutuhkan |
| **Source registry** | mencatat sumber resmi, fungsi sumber, tanggal review, dan konflik yang perlu diawasi |
| **Behavior eval** | menyimpan failure mode penting supaya perubahan prompt/pack bisa diuji ulang |

Website hanya membantu memilih pack, menyalin instruksi, dan mengunduh course pack. File kuliah pribadi tetap masuk langsung ke ChatGPT Project pengguna.

## Pack yang tersedia

Saat ini ada dua pack aktif untuk **Universitas Terbuka · S1 Akuntansi · 2026/2027**.

### Semester 2 — 16 SKS

| Project | Mata kuliah | SKS |
|---|---|---:|
| `Semester 2 • Perpajakan` | EACC4104 Perpajakan | 3 |
| `Semester 2 • AKM I` | EACC4103 Akuntansi Keuangan Menengah I | 3 |
| `Semester 2 • Manajemen Keuangan` | EMBS4210 Manajemen Keuangan | 3 |
| `Semester 2 • Ekonomi Mikro` | ECON4102 Pengantar Ekonomi Mikro | 3 |
| `Semester 2 • Manajemen` | EMBS4101 Manajemen | 4 |

Manifest: [`semester-02/manifest.json`](packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/manifest.json)

### Semester 3 — 20 SKS

| Project | Mata kuliah | SKS |
|---|---|---:|
| `Semester 3 • Lab Perpajakan` | EACC4206 Laboratorium Perpajakan | 2 |
| `Semester 3 • Kewirausahaan Digital` | MKDI4203 Kewirausahaan di Era Digital | 3 |
| `Semester 3 • Akuntansi Manajemen` | EMBS4326 Akuntansi Manajemen | 3 |
| `Semester 3 • SIA` | EACC4207 Sistem Informasi Akuntansi | 3 |
| `Semester 3 • Bahasa Inggris` | MKDI4201 Bahasa Inggris | 3 |
| `Semester 3 • AKM II` | EACC4205 Akuntansi Keuangan Menengah II | 3 |
| `Semester 3 • Belajar di Era Digital` | MKDI4202 Belajar di Era Digital | 3 |

Manifest: [`semester-03/manifest.json`](packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-03/manifest.json)

Semester 3 direview ulang terhadap Katalog Kurikulum UT 2026/2027 edisi Juli 2026, Pedoman Sistem Penyelenggaraan 2026/2027, dan halaman BMP aktif. Review ini penting karena beberapa metadata sudah berbeda dari tahun sebelumnya, terutama AKM II yang sekarang memakai `EACC4205` dan berstatus BP/BPro.

## Mulai dari satu mata kuliah

Tidak perlu menyiapkan satu semester sekaligus.

1. buka [site Ramu](https://man612.github.io/ramu/);
2. pilih pack yang sesuai;
3. pilih satu mata kuliah;
4. buat ChatGPT Project dengan nama yang ditampilkan;
5. pasang Project Instructions;
6. unggah course pack sebagai Project Source;
7. mulai gunakan Project tersebut.

Kalau pola ini terasa berguna, baru tambahkan mata kuliah lain. Progress setup di website disimpan lokal di browser berdasarkan `pack id`.

Panduan lengkap: [`docs/PANDUAN-SETUP-CHATGPT.md`](docs/PANDUAN-SETUP-CHATGPT.md).

## Struktur pack

`packs/index.json` menjadi katalog utama. Setiap entry menunjuk ke `manifest.json`, lalu manifest menghubungkan course pack, source registry, Project Instructions, dan eval suite yang diperlukan.

```text
packs/
├── index.json
└── universitas-terbuka/
    ├── source-registry.json
    ├── evals/
    └── s1-akuntansi/
        └── 2026-2027/
            ├── semester-02/
            └── semester-03/
```

Tooling membaca katalog dan manifest, jadi penambahan pack tidak membutuhkan daftar semester yang di-hardcode ke validator atau website.

Periode akademik memakai dua field:

- `period_id` untuk identity mesin, misalnya `semester-03` atau `term-fall`;
- `period_label` untuk label pengguna, misalnya `Semester 3` atau `Fall Term`.

Dengan model ini, struktur yang sama tetap bisa dipakai institusi yang menggunakan trimester, quarter, term, atau sistem periode lain.

Nama Project memakai `period_label` lengkap, misalnya `Semester 3 • AKM II`. Bentuk `S2`/`S3` dihindari pada UI karena mudah terbaca sebagai jenjang pendidikan; singkatan tetap dipakai pada ID internal seperti `.s3` atau versi `2026-2027.s3.1`.

## Eval yang bisa dikomposisi

Setiap pack menyusun eval dari aturan paling umum ke yang paling spesifik:

```text
core
  ↓
institution      (opsional)
  ↓
program          (opsional)
  ↓
pack
```

Pack UT yang aktif saat ini memakai:

```text
core → universitas-terbuka → semester-02
core → universitas-terbuka → semester-03
```

`core` memuat failure mode yang berlaku luas, misalnya sitasi palsu, prompt injection, context leak, source freshness, learner state, dan academic integrity. Suite institusi menyimpan aturan yang memang khas UT, seperti konflik katalog pusat dengan halaman regional. Skenario yang hanya masuk akal untuk mata kuliah/periode tertentu tetap berada dekat pack-nya.

Validator memastikan urutan suite benar, identity antardokumen cocok, dan ID regression case tidak saling menimpa.

Detail: [`evals/README.md`](evals/README.md).

## Validasi

Sebagian besar pemeriksaan bisa dijalankan tanpa OpenAI API.

```bash
python scripts/validate_repo.py
python scripts/validate_display_names.py
python scripts/validate_site.py
python scripts/check_source_freshness.py
python scripts/run_behavior_evals.py --dry-run \
  --pack id.ut.accounting-s1.2026-2027.s3
```

Manual Eval Kit menghasilkan checklist untuk pengujian langsung di ChatGPT Projects:

```bash
python scripts/prepare_manual_eval.py \
  --pack id.ut.accounting-s1.2026-2027.s3
```

Automated behavior eval melalui API tetap tersedia sebagai QA tambahan, tetapi tidak menjadi syarat untuk memakai Ramu atau menjalankan static CI.

## Sumber dan perubahan yang perlu diawasi

Registry source dapat hidup di scope global, institusi, program, atau pack. Setiap entry mencatat antara lain `authority`, `canonical_for`, `verified_at`, `review_interval_days`, `watch`, dan `status`.

Source Watch memeriksa umur review dan reachability URL. URL yang masih hidup tidak otomatis berarti isinya masih benar; sebaliknya, URL yang gagal dibuka juga belum membuktikan faktanya berubah. Tanggal verifikasi baru diperbarui setelah sumbernya benar-benar direview.

Detail pendekatan ini ada di [`docs/SUMBER-DAN-VALIDASI.md`](docs/SUMBER-DAN-VALIDASI.md).

## Status pack

- `source-verified` — sumber utama sudah diperiksa; behavior belum diklaim selesai sepenuhnya;
- `verified` — source dan behavior validation yang relevan sudah direview;
- `community` — kontribusi komunitas yang belum mencapai status maintained/verified;
- `experimental` — masih dalam tahap pengujian;
- `deprecated` — sudah digantikan atau tidak lagi direkomendasikan untuk penggunaan baru.

Status tersebut adalah snapshot terhadap versi pack, tanggal, dan environment yang diuji. Ia bukan jaminan bahwa model AI akan selalu menghasilkan jawaban yang benar.

## Batas proyek

Ramu fokus pada konfigurasi workspace belajar dan cara mengujinya. Ia tidak ditujukan untuk menyimpan bank jawaban tugas, menggantikan LMS kampus, menyalin materi berhak cipta, atau menjanjikan model AI kebal terhadap error dan prompt injection.

Pack `maintainer: ramu` berarti pack tersebut dipelihara di repository utama. Istilah itu tidak berarti pack diterbitkan atau disahkan oleh universitas. Proyek ini independen dari Universitas Terbuka, institusi pendidikan lain, dan OpenAI.

## Berkontribusi

Issue dan PR terbuka untuk bug, source yang berubah, perbaikan dokumentasi, eval baru, tooling, atau pack tambahan. Mulai dari [`CONTRIBUTING.md`](CONTRIBUTING.md).

Untuk masalah keamanan, lihat [`SECURITY.md`](SECURITY.md). Untuk pertanyaan umum, lihat [`SUPPORT.md`](SUPPORT.md).

## Lisensi

Kode dan dokumentasi repository menggunakan [MIT License](LICENSE). Materi kuliah, BMP, rubrik, dan source eksternal tetap mengikuti hak cipta serta ketentuan pemiliknya masing-masing.
