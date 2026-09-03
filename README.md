<p align="center">
  <img src=".github/assets/hero-light.svg#gh-light-mode-only" alt="Ramu — structured AI learning workspace untuk ChatGPT Projects" width="100%">
  <img src=".github/assets/hero-dark.svg#gh-dark-mode-only" alt="Ramu — structured AI learning workspace untuk ChatGPT Projects" width="100%">
</p>

<p align="center">
  <strong>Structured AI learning workspace untuk ChatGPT Projects.</strong><br>
  Source grounding, learning guardrails, context isolation, source governance, dan eval yang dapat diperiksa ulang.
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

## Ramu itu apa?

Ramu adalah **framework workspace belajar untuk ChatGPT Projects**. Satu mata kuliah ditempatkan di satu Project yang memiliki Project Instructions, course pack, source yang sesuai, dan guardrail belajar.

Ramu bukan model AI, bukan LMS, bukan backend yang menerima file mahasiswa, dan bukan kumpulan jawaban tugas. Website Ramu bersifat statis; materi pribadi tetap ditambahkan pengguna langsung ke ChatGPT Project masing-masing.

> Nama **Ramu** berasal dari kata *meramu*: menyatukan konteks, sumber, materi, aturan belajar, dan pemeriksaan menjadi ruang belajar yang siap dipakai.

## Kenapa tidak cukup chat biasa?

AI sudah mampu menjelaskan materi, tetapi workspace kuliah yang berjalan lama memiliki masalah lain: konteks antarmata kuliah bisa bercampur, aturan tugas terlupa, source lama dipakai seolah terbaru, versi course pack konflik, atau AI terlalu cepat memberi jawaban akhir.

Ramu menjaga lima lapisan:

| Lapisan | Yang dijaga |
|---|---|
| **Referensi** | otoritas source, canonical source, tanggal verifikasi, freshness |
| **Instruksi** | aturan kampus/tutor/rubrik, integritas, prompt-injection boundary |
| **Zona konteks** | mata kuliah dan learner state tidak tercampur |
| **Materi** | BMP/materi/screenshot/PDF dipakai sebagai content, bukan instruksi liar |
| **Asesmen** | bantuan bertahap, checking, review queue, behavior contract |

## Multi-pack yang benar-benar dipakai

Pack pertama Ramu adalah **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**. Semester 3 sekarang menjadi **real second pack** pertama yang menggunakan discovery, source governance, site, dan validation matrix yang sama tanpa hardcode path baru.

```text
packs/
├── index.json
├── universitas-terbuka/
│   ├── source-registry.json
│   ├── evals/                     # rule reusable untuk semua pack UT
│   └── s1-akuntansi/
│       └── 2026-2027/
│           ├── semester-02/
│           └── semester-03/
└── institusi-lain/                # ketika ada pack yang layak ditambahkan
```

[`packs/index.json`](packs/index.json) adalah katalog machine-readable. Setiap entry menunjuk `manifest.json` pack. Validator, GitHub Pages, Manual Eval Kit, dan Behavior Evals menemukan pack melalui katalog/manifest—bukan melalui path Semester 2/3 yang ditulis di source code.

Pack membedakan dua hal:

- `maintainer: ramu` → **Ramu Maintained**;
- `maintainer: community` → **Community maintained**.

Istilah “maintained” dipakai agar tidak memberi kesan pack tersebut resmi diterbitkan universitas. Ramu tetap proyek independen.

### Periode akademik yang tidak mengunci “semester”

Manifest/katalog punya dua metadata periode yang sengaja dipisahkan:

- `period_id` → identifier machine-safe dan stabil, misalnya `semester-02`, `semester-03`, `trimester-01`, atau `term-fall`;
- `period_label` → label yang benar-benar ditampilkan ke manusia, misalnya `Semester 2`, `Semester 3`, `Trimester 1`, atau `Fall Term`.

Ramu **tidak memiliki field universal bernama `semester`**. Semester hanyalah salah satu bentuk academic period. Pack UT saat ini memakai `semester-02` dan `semester-03`; institusi yang memakai trimester, quarter, term, summer session, atau struktur lain tidak perlu dipaksa ke konsep semester.

Nama Project harus diawali `period_label`, misalnya `Semester 3 • AKM II`, **bukan** `S3 • AKM II`. Singkatan `S2`/`S3` mudah dibaca sebagai jenjang pendidikan. Identifier internal seperti `.s2`, `.s3`, folder `semester-03/`, atau versi `2026-2027.s3.1` tetap boleh ringkas karena itu identity mesin, bukan label pengguna.

## Paket yang tersedia sekarang

### UT S1 Akuntansi 2026/2027 — Semester 2

| Project | Mata kuliah | SKS |
|---|---|---:|
| `Semester 2 • Perpajakan` | EACC4104 Perpajakan | 3 |
| `Semester 2 • AKM I` | EACC4103 Akuntansi Keuangan Menengah I | 3 |
| `Semester 2 • Manajemen Keuangan` | EMBS4210 Manajemen Keuangan | 3 |
| `Semester 2 • Ekonomi Mikro` | ECON4102 Pengantar Ekonomi Mikro | 3 |
| `Semester 2 • Manajemen` | EMBS4101 Manajemen | 4 |

Total **16 SKS**. Manifest: [`semester-02/manifest.json`](packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/manifest.json).

### UT S1 Akuntansi 2026/2027 — Semester 3

| Project | Mata kuliah | SKS |
|---|---|---:|
| `Semester 3 • Lab Perpajakan` | EACC4206 Laboratorium Perpajakan | 2 |
| `Semester 3 • Kewirausahaan Digital` | MKDI4203 Kewirausahaan di Era Digital | 3 |
| `Semester 3 • Akuntansi Manajemen` | EMBS4326 Akuntansi Manajemen | 3 |
| `Semester 3 • SIA` | EACC4207 Sistem Informasi Akuntansi | 3 |
| `Semester 3 • Bahasa Inggris` | MKDI4201 Bahasa Inggris | 3 |
| `Semester 3 • AKM II` | EACC4205 Akuntansi Keuangan Menengah II | 3 |
| `Semester 3 • Belajar di Era Digital` | MKDI4202 Belajar di Era Digital | 3 |

Total **20 SKS**. Manifest: [`semester-03/manifest.json`](packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-03/manifest.json).

Semester 3 diverifikasi ulang terhadap **Katalog Kurikulum UT 2026/2027 edisi Juli 2026**, Pedoman Sistem Penyelenggaraan 2026/2027, dan halaman BMP aktif. Pack tidak menyalin metadata lama secara otomatis: AKM II current sudah memakai `EACC4205` baru dan BP/BPro, bukan metadata historis `EKMA4313`.

Source UT pusat berada di registry institusi. Semester 3 juga mempunyai registry pack sendiri untuk halaman BMP dan claim yang memang spesifik pada periodenya. Materi kuliah berhak cipta tidak disalin ke repository.

## Mulai dari satu mata kuliah

Tidak perlu setup seluruh periode untuk mencoba Ramu.

1. buka [site Ramu](https://man612.github.io/ramu/);
2. pilih pack yang sesuai;
3. pilih satu mata kuliah;
4. buat ChatGPT Project dengan nama yang diberikan manifest;
5. pasang Project Instructions melalui Project settings;
6. unggah satu course pack melalui Sources;
7. mulai belajar seperti biasa.

Kalau satu Project terasa berguna, baru tambahkan Project lain. Progress setup disimpan lokal di browser berdasarkan `pack id`, bukan dikirim ke server Ramu.

## Composable eval suites

Ramu tidak lagi menganggap eval hanya terdiri dari `core + pack`. Setiap manifest menyusun ordered `eval_suites` dari aturan paling umum menuju paling spesifik:

```text
core
  ↓
institution      (opsional)
  ↓
program          (opsional)
  ↓
pack
```

Dua pack UT yang tersedia saat ini mempunyai wiring:

```text
core → universitas-terbuka → semester-02
core → universitas-terbuka → semester-03
```

**Core eval** menangkap failure mode lintas seluruh Ramu: data yang hilang, sitasi palsu, integritas tugas, retrieval practice, learner state, source freshness, prompt injection, dan konflik versi pack.

**Institution eval** menangkap perilaku yang berlaku untuk banyak pack pada institusi yang sama. E14, misalnya, menguji konflik source pusat vs regional berdasarkan source registry Universitas Terbuka. Case ini period-neutral dan berada di `packs/universitas-terbuka/evals/`, bukan dicopy ke setiap semester.

**Program eval** disediakan untuk aturan yang suatu hari berlaku lintas periode pada satu program tetapi tidak otomatis berlaku ke program lain. Scope ini belum diperlukan oleh pack yang tersedia sekarang.

**Pack eval** menyimpan skenario yang benar-benar membutuhkan course/periode tertentu. Semester 2 memiliki case seperti aturan pajak vs BMP dan jurnal AKM I. Semester 3 menambahkan E17–E24 untuk tax-currentness, AKM II old-vs-current metadata, continuity kasus PRATON, SIA requirement/control, relevant cost, business evidence, language tutoring, dan uncertainty policy GenAI.

Suite yang lebih spesifik boleh mengubah default runtime behavior eval, tetapi **ID case tidak boleh mengganti/menimpa case suite sebelumnya**. Validator mewajibkan core pertama, pack terakhir, urutan scope tidak boleh mundur, dan ID case harus unik setelah seluruh suite digabung.

Detail format: [`evals/README.md`](evals/README.md).

## Tidak punya API tetap bisa diuji

Ramu memiliki tiga lapisan validation:

| Jalur | API? | Fungsi |
|---|---:|---|
| **Static CI** | tidak | manifest, pack catalog, period metadata, display naming, source registry, eval-suite wiring, contract marker, site wiring |
| **Manual Behavior Validation** | tidak | menjalankan case langsung di ChatGPT Projects asli |
| **Automated Behavior Eval** | ya, opsional | regression/benchmark melalui Responses API + model judge |

Static validation lokal:

```bash
python scripts/validate_repo.py
python scripts/validate_display_names.py
python scripts/validate_site.py
python scripts/check_source_freshness.py
python scripts/run_behavior_evals.py --dry-run \
  --pack id.ut.accounting-s1.2026-2027.s3
```

Membuat checklist manual tanpa API:

```bash
python scripts/prepare_manual_eval.py \
  --pack id.ut.accounting-s1.2026-2027.s3
```

Atau gunakan **Actions → Manual Eval Kit**. Workflow tersebut tidak membutuhkan secret dan menghasilkan checklist dari seluruh eval suite yang dideklarasikan pack. Checklist juga mencatat suite asal tiap case agar failure dapat diperbaiki pada scope yang benar.

Automated API eval tetap tersedia bila suatu saat API digunakan:

```bash
python scripts/run_behavior_evals.py \
  --pack id.ut.accounting-s1.2026-2027.s3 \
  --candidate-model <candidate> \
  --grader-model <judge>
```

Ramu sengaja tidak mengunci nama model permanen.

## Source governance

Registry source berscope:

```text
sources/registry.json                                      global/runtime
packs/<institusi>/source-registry.json                     institusi
packs/<institusi>/<program>/<tahun>/<periode>/source-registry.json  pack bila diperlukan
```

Setiap pack menyebut `source_registries` yang menjadi dependency-nya. Source mempunyai `authority`, `canonical_for`, `verified_at`, `review_interval_days`, `watch`, dan `status`.

Source Watch mencari seluruh registry tersebut. URL yang hidup bukan bukti fakta masih terbaru; URL yang gagal juga bukan bukti fakta berubah. Update `verified_at` harus mengikuti review manusia.

## CI yang tumbuh bersama jumlah pack

`Validate Ramu` memiliki dua tahap utama:

1. validasi katalog/manifest/period metadata/display name/source/site secara keseluruhan;
2. matrix dry-run untuk **setiap pack** di `packs/index.json`.

Job akhir selalu bernama **`validate`**, sehingga branch protection dapat memakai satu required status check walaupun jumlah pack bertambah. Penambahan Semester 3 harus menghasilkan matrix job kedua secara otomatis; workflow tidak diberi path S3 khusus.

Validator memastikan `period_id` machine-safe dan sama antara katalog/manifest, setiap `project_name` diawali `<period_label> • `, serta site generic tidak kembali membentuk label `Semester ...` dari field khusus semester. Validator eval memastikan suite mengikuti urutan `core → institution → program → pack`, metadata suite cocok dengan file contracts/behavior, dan tidak ada ID regression case yang saling menimpa.

Dependency GitHub Actions dipin ke full commit SHA agar tag dependency tidak menjadi bagian supply-chain yang dapat bergerak diam-diam.

## Status pack

- `source-verified` — source utama sudah diperiksa, behavior belum diklaim penuh;
- `verified` — source + behavior validation relevan telah direview sesuai standar release saat itu;
- `community` — kontribusi komunitas yang belum mencapai status maintained/verified;
- `experimental` — masih diuji;
- `deprecated` — tidak direkomendasikan untuk penggunaan baru.

Status `verified` tetap snapshot terhadap **pack version + contract version + tanggal + runtime/product/model yang diuji**, bukan jaminan AI selalu benar.

## Prompt injection

Project Source, PDF, web, screenshot, dan metadata diperlakukan sebagai **content**, bukan otomatis sebagai instruksi yang boleh menimpa Project Instructions. Ramu memiliki contract/eval untuk source injection, tetapi tidak mengklaim “prompt-injection proof”. Failure baru yang ditemukan pengguna sebaiknya diubah menjadi regression case.

## Struktur repository

```text
ramu/
├── core/          prinsip universal
├── protocols/     belajar, tugas, review, latihan
├── learning/      learner-state contracts/templates
├── packs/         catalog + institusi/program/periode/course pack + scoped eval
├── sources/       source global + freshness policy
├── evals/         core eval, manual tooling docs, results ignored
├── schemas/       kontrak katalog/manifest/registry/contracts/behavior eval
├── scripts/       discovery, validator, freshness, eval runner
├── docs/          riset, arah proyek, validasi, pilot, release process
├── site/          GitHub Pages catalog-driven
└── .github/       CI, manual/API eval, source watch, Pages
```

## Menambah periode / program / universitas lain

Prinsipnya bukan mengedit `app.js` atau validator. Buat pack + manifest + source yang relevan, tentukan `period_id` + `period_label`, pilih reusable eval suite yang memang berlaku, tambahkan suite pack-nya, lalu daftarkan ke `packs/index.json`. Semester 3 UT sekarang menjadi contoh nyata bahwa pack kedua dapat masuk lewat mekanisme tersebut; sistem kalender lain tetap menggunakan metadata periode mereka sendiri. Panduan contributor ada di [`CONTRIBUTING.md`](CONTRIBUTING.md).

Validator akan menolak manifest yang tidak terdaftar, entry katalog yang menunjuk file hilang, `period_id` tidak valid/berbeda dengan manifest, ID source/eval duplikat, course yang tidak self-describing, wiring suite yang tidak lengkap/urutannya salah, atau nama Project yang tidak sesuai label periode pack.

## Landasan dan batas klaim

Desain belajar Ramu mengambil inspirasi dari riset active learning, tutoring, self-regulated learning, retrieval practice, dan guardrails penggunaan generative AI. Referensi dan batas interpretasinya ada di [`docs/LANDASAN-PEMBELAJARAN.md`](docs/LANDASAN-PEMBELAJARAN.md).

Riset tersebut bukan bukti bahwa Ramu sendiri otomatis efektif. Public beta tetap membutuhkan penggunaan nyata, manual behavior validation, dan pengumpulan failure mode. Lihat [`docs/PILOT-PUBLIC-BETA.md`](docs/PILOT-PUBLIC-BETA.md).

## Release dan kontribusi

- [`CHANGELOG.md`](CHANGELOG.md)
- [`docs/RELEASE-PROCESS.md`](docs/RELEASE-PROCESS.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`SECURITY.md`](SECURITY.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- [MIT License](LICENSE)

---

<p align="center">
  <b>Pilih pack → coba satu mata kuliah → nilai perilakunya → perluas kalau memang berguna.</b>
</p>

<p align="center">
  <sub>Proyek independen. Bukan layanan resmi institusi pendidikan mana pun maupun OpenAI.</sub>
</p>