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

## Multi-pack dari awal

Pack pertama Ramu adalah **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**. Namun tooling tidak mengunci Semester 2 sebagai satu-satunya bentuk Ramu.

```text
packs/
├── index.json
├── universitas-terbuka/
│   ├── source-registry.json
│   └── s1-akuntansi/
│       └── 2026-2027/
│           ├── semester-02/
│           └── semester-03/        # ketika tersedia
└── institusi-lain/                 # ketika ada pack yang layak ditambahkan
```

[`packs/index.json`](packs/index.json) adalah katalog machine-readable. Setiap entry menunjuk `manifest.json` pack. Validator, GitHub Pages, Manual Eval Kit, dan Behavior Evals menemukan pack melalui katalog/manifest—bukan melalui path Semester 2 yang ditulis di source code.

Pack membedakan dua hal:

- `maintainer: ramu` → **Ramu Maintained**;
- `maintainer: community` → **Community maintained**.

Istilah “maintained” dipakai agar tidak memberi kesan pack tersebut resmi diterbitkan universitas. Ramu tetap proyek independen.

## Paket yang tersedia sekarang

Pack awal saat ini berisi:

| Project | Mata kuliah | SKS |
|---|---|---:|
| `S2 • Perpajakan` | EACC4104 Perpajakan | 3 |
| `S2 • AKM I` | EACC4103 Akuntansi Keuangan Menengah I | 3 |
| `S2 • Manajemen Keuangan` | EMBS4210 Manajemen Keuangan | 3 |
| `S2 • Ekonomi Mikro` | ECON4102 Pengantar Ekonomi Mikro | 3 |
| `S2 • Manajemen` | EMBS4101 Manajemen | 4 |

Data pack dan source dependency ada di [`packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/manifest.json`](packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/manifest.json). Source UT berada di registry institusi, sementara source runtime seperti dokumentasi ChatGPT berada di global registry.

Materi kuliah berhak cipta tidak disalin ke repository.

## Mulai dari satu mata kuliah

Tidak perlu setup seluruh semester untuk mencoba Ramu.

1. buka [site Ramu](https://man612.github.io/ramu/);
2. pilih pack yang sesuai;
3. pilih satu mata kuliah;
4. buat ChatGPT Project;
5. pasang Project Instructions melalui Project settings;
6. unggah satu course pack melalui Sources;
7. mulai belajar seperti biasa.

Kalau satu Project terasa berguna, baru tambahkan Project lain. Progress setup disimpan lokal di browser berdasarkan `pack id`, bukan dikirim ke server Ramu.

## Core vs pack

Ramu memisahkan aturan yang universal dari konteks akademik tertentu.

```text
core / protocols / learning
        ↓
   core behavior eval
        +
pack manifest / Project Instructions / courses / sources
        ↓
   pack behavior eval
        ↓
  satu suite untuk pack yang dipilih
```

**Core eval** menangkap failure mode yang seharusnya berlaku luas: data yang hilang, sitasi palsu, integritas tugas, retrieval practice, learner state, source freshness, prompt injection, dan konflik versi pack.

**Pack eval** menangkap perilaku yang hanya bermakna pada konteks tertentu. Pada UT S1 Akuntansi Semester 2 contohnya: pajak lama vs aturan terbaru, jurnal AKM I, source UT pusat vs regional, dan context isolation antarmata kuliah.

Dengan begitu Semester 3 atau universitas lain tidak perlu menyalin seluruh eval universal.

## Tidak punya API tetap bisa diuji

Ramu memiliki tiga lapisan validation:

| Jalur | API? | Fungsi |
|---|---:|---|
| **Static CI** | tidak | manifest, pack catalog, source registry, contract marker, site wiring |
| **Manual Behavior Validation** | tidak | menjalankan case langsung di ChatGPT Projects asli |
| **Automated Behavior Eval** | ya, opsional | regression/benchmark melalui Responses API + model judge |

Static validation lokal:

```bash
python scripts/validate_repo.py
python scripts/validate_site.py
python scripts/check_source_freshness.py
python scripts/run_behavior_evals.py --dry-run \
  --pack id.ut.accounting-s1.2026-2027.s2
```

Membuat checklist manual tanpa API:

```bash
python scripts/prepare_manual_eval.py \
  --pack id.ut.accounting-s1.2026-2027.s2
```

Atau gunakan **Actions → Manual Eval Kit**. Workflow tersebut tidak membutuhkan secret dan hanya menghasilkan checklist dari core + pack eval yang sama.

Automated API eval tetap tersedia bila suatu saat API digunakan:

```bash
python scripts/run_behavior_evals.py \
  --pack id.ut.accounting-s1.2026-2027.s2 \
  --candidate-model <candidate> \
  --grader-model <judge>
```

Ramu sengaja tidak mengunci nama model permanen.

## Source governance

Registry source berscope:

```text
sources/registry.json                     global/runtime
packs/<institusi>/source-registry.json    institusi
...                                       program/pack bila diperlukan
```

Setiap pack menyebut `source_registries` yang menjadi dependency-nya. Source mempunyai `authority`, `canonical_for`, `verified_at`, `review_interval_days`, `watch`, dan `status`.

Source Watch mencari seluruh registry tersebut. URL yang hidup bukan bukti fakta masih terbaru; URL yang gagal juga bukan bukti fakta berubah. Update `verified_at` harus mengikuti review manusia.

## CI yang tumbuh bersama jumlah pack

`Validate Ramu` memiliki dua tahap utama:

1. validasi katalog/manifest/source/site secara keseluruhan;
2. matrix dry-run untuk setiap pack di `packs/index.json`.

Job akhir selalu bernama **`validate`**, sehingga branch protection dapat memakai satu required status check walaupun jumlah pack bertambah.

Dependency GitHub Actions yang dipakai workflow dipin ke full commit SHA agar tag dependency tidak menjadi bagian supply-chain yang dapat bergerak diam-diam.

## Status pack

- `source-verified` — source utama sudah diperiksa, behavior belum diklaim penuh;
- `verified` — source + behavior validation relevan telah direview sesuai standar release saat itu;
- `community` — kontribusi komunitas yang belum mencapai status maintained/verified;
- `experimental` — masih diuji;
- `deprecated` — tidak direkomendasikan untuk penggunaan baru.

Status `verified` tetap snapshot terhadap **pack version + tanggal + runtime/product/model yang diuji**, bukan jaminan AI selalu benar.

## Prompt injection

Project Source, PDF, web, screenshot, dan metadata diperlakukan sebagai **content**, bukan otomatis sebagai instruksi yang boleh menimpa Project Instructions. Ramu memiliki contract/eval untuk source injection, tetapi tidak mengklaim “prompt-injection proof”. Failure baru yang ditemukan pengguna sebaiknya diubah menjadi regression case.

## Struktur repository

```text
ramu/
├── core/          prinsip universal
├── protocols/     belajar, tugas, review, latihan
├── learning/      learner-state contracts/templates
├── packs/         catalog + institusi/program/semester/course pack
├── sources/       source global + freshness policy
├── evals/         core eval, manual tooling docs, results ignored
├── schemas/       kontrak katalog/manifest/registry/eval
├── scripts/       discovery, validator, freshness, eval runner
├── docs/          riset, arah proyek, validasi, pilot
├── site/          GitHub Pages catalog-driven
└── .github/       CI, manual/API eval, source watch, Pages
```

## Menambah Semester 3 / program / universitas lain

Prinsipnya bukan mengedit `app.js` atau validator. Buat pack + manifest + source/eval yang relevan, lalu daftarkan ke `packs/index.json`. Panduan contributor ada di [`CONTRIBUTING.md`](CONTRIBUTING.md).

Validator akan menolak manifest yang tidak terdaftar, entry katalog yang menunjuk file hilang, ID source/eval duplikat, course yang tidak self-describing, atau wiring eval yang tidak lengkap.

## Landasan dan batas klaim

Desain belajar Ramu mengambil inspirasi dari riset active learning, tutoring, self-regulated learning, retrieval practice, dan guardrails penggunaan generative AI. Referensi dan batas interpretasinya ada di [`docs/LANDASAN-PEMBELAJARAN.md`](docs/LANDASAN-PEMBELAJARAN.md).

Riset tersebut bukan bukti bahwa Ramu sendiri otomatis efektif. Public beta tetap membutuhkan penggunaan nyata, manual behavior validation, dan pengumpulan failure mode. Lihat [`docs/PILOT-PUBLIC-BETA.md`](docs/PILOT-PUBLIC-BETA.md).

## Kontribusi dan keamanan

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
