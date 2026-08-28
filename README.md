<p align="center">
  <img src=".github/assets/hero-light.svg#gh-light-mode-only" alt="Ramu — structured AI learning workspace untuk ChatGPT Projects" width="100%">
  <img src=".github/assets/hero-dark.svg#gh-dark-mode-only" alt="Ramu — structured AI learning workspace untuk ChatGPT Projects" width="100%">
</p>

<p align="center">
  <strong>Structured AI learning workspace untuk ChatGPT Projects.</strong><br>
  Source grounding, pedagogical guardrails, learning context, dan behavior eval dalam satu framework yang bisa diperiksa ulang.
</p>

<p align="center">
  <a href="https://man612.github.io/ramu/"><strong>Buka Ramu</strong></a>
  ·
  <a href="https://man612.github.io/ramu/setup.html">Coba setup</a>
  ·
  <a href="docs/LANDASAN-PEMBELAJARAN.md">Landasan pembelajaran</a>
  ·
  <a href="docs/PILOT-PUBLIC-BETA.md">Pilot public beta</a>
</p>

<p align="center">
  <img alt="GitHub Pages" src="https://img.shields.io/github/actions/workflow/status/man612/ramu/pages.yml?label=pages&style=flat-square">
  <img alt="Validasi Ramu" src="https://img.shields.io/github/actions/workflow/status/man612/ramu/validate.yml?label=contracts&style=flat-square">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-4C6B58?style=flat-square">
  <img alt="Status" src="https://img.shields.io/badge/status-public%20beta-BB8C51?style=flat-square">
  <img alt="Paket pertama" src="https://img.shields.io/badge/paket-UT%20S1%20Akuntansi-405A46?style=flat-square">
</p>

---

## Ramu itu apa?

Ramu adalah **framework konfigurasi untuk ChatGPT Projects** agar setiap mata kuliah memiliki konteks, sumber, aturan belajar, dan cara pemeriksaan yang jelas.

Ramu bukan aplikasi pengganti ChatGPT, bukan model AI baru, dan bukan kumpulan jawaban tugas. Yang diatur Ramu adalah **cara workspace belajar dibentuk dan diuji**: source mana yang dipercaya, informasi apa yang belum diketahui, kapan mahasiswa perlu mencoba sendiri, bagaimana jawaban diperiksa, dan failure mode apa yang harus ditangkap oleh eval.

> Nama **Ramu** berasal dari kata *meramu*: menyatukan konteks, sumber, materi, aturan belajar, dan pemeriksaan menjadi satu ruang belajar yang siap dipakai.

### Masalah yang ingin diselesaikan

ChatGPT biasa sudah bisa menjelaskan materi. Masalahnya, percakapan kuliah yang berjalan lama mudah kehilangan struktur: mata kuliah tercampur, aturan tugas harus dijelaskan ulang, sumber terbaru bercampur dengan materi lama, dan AI dapat terlalu cepat menjadi mesin jawaban.

Ramu menambahkan lapisan yang lebih disiplin:

| Lapisan | Yang dijaga |
|---|---|
| **Referensi** | sumber resmi, prioritas source, tanggal verifikasi, dan freshness |
| **Instruksi** | aturan tugas, rubrik, guardrail, dan cara tutor merespons |
| **Zona konteks** | satu mata kuliah berada di Project-nya sendiri |
| **Materi** | BMP/materi/screenshot/PDF milik mahasiswa digunakan saat relevan |
| **Asesmen** | jawaban, hitungan, sumber, dan pemahaman diperiksa sebelum dianggap selesai |

Folder `protocols`, `learning`, `sources`, `schemas`, dan `evals` adalah lapisan desain/pemeriksaan di belakang runtime. Pengguna sehari-hari cukup memasang **Project Instructions + satu course pack** pada Project mata kuliah.

## Coba dulu satu mata kuliah

Jangan setup seluruh semester hanya untuk mengetahui apakah Ramu cocok.

**Jalur tercepat:**

1. buka [panduan setup](https://man612.github.io/ramu/setup.html);
2. pilih **satu** mata kuliah yang ingin dicoba;
3. buat ChatGPT Project untuk mata kuliah tersebut;
4. pasang `PROJECT-INSTRUCTIONS.md` melalui Project settings;
5. unggah satu course pack melalui Sources;
6. mulai dengan permintaan normal seperti `aku belum paham bagian ini`, `cek jawabanku`, atau `bantu aku latihan tanpa langsung kasih kunci`.

Kalau satu Project sudah terasa berguna, baru pasang mata kuliah lain. Ini sengaja menjadi pola onboarding public beta supaya pengguna merasakan manfaat sebelum melakukan setup lebih banyak.

## Paket yang tersedia sekarang

Paket pertama dibuat untuk **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**.

| Project | Mata kuliah | SKS |
|---|---|---:|
| `S2 • Perpajakan` | EACC4104 Perpajakan | 3 |
| `S2 • AKM I` | EACC4103 Akuntansi Keuangan Menengah I | 3 |
| `S2 • Manajemen Keuangan` | EMBS4210 Manajemen Keuangan | 3 |
| `S2 • Ekonomi Mikro` | ECON4102 Pengantar Ekonomi Mikro | 3 |
| `S2 • Manajemen` | EMBS4101 Manajemen | 4 |

Sumber akademik utama paket sudah dicocokkan dengan katalog/pedoman resmi yang tercatat di [`sources/registry.json`](sources/registry.json). Materi kuliah berhak cipta tidak disalin ke repo; mahasiswa menambahkan materi yang memang mereka miliki/berhak akses ke Project masing-masing.

## Apa yang terjadi saat dipakai?

Contoh sederhananya:

**Tanpa struktur khusus**

```text
mahasiswa → kirim soal → AI mencoba menjawab dari konteks yang tersedia
```

**Dengan Ramu**

```text
mahasiswa
   ↓
Project mata kuliah
   ↓
Project Instructions + course pack
   ↓
cek konteks / source / informasi yang hilang
   ↓
pilih mode: belajar, tugas, review, atau latihan
   ↓
beri bantuan bertahap / minta percobaan mahasiswa
   ↓
verifikasi jawaban dan source
   ↓
simpan konteks belajar penting bila diperlukan
```

Ramu tidak menjamin setiap model selalu mengikuti alur ini. Karena itu perilaku penting dibuat sebagai kontrak dan behavior eval, bukan hanya ditulis di README.

## Model AI tidak di-hardcode

Ramu sengaja **tidak menetapkan satu nama model sebagai dependency permanen**.

Katalog model, model default setiap paket ChatGPT, batas penggunaan, dan model API dapat berubah. Project Instructions/course pack harus tetap masuk akal ketika model berganti. Untuk behavior eval nyata, model kandidat dan model judge dipilih **secara eksplisit saat run** dan dicatat di artifact hasil.

Konsekuensinya:

- perubahan model default ChatGPT tidak membutuhkan perubahan course pack hanya karena namanya berganti;
- hasil eval selalu menyebut model yang benar-benar diuji;
- candidate dan judge dapat dipilih terpisah;
- jika candidate dan judge sama, runner memberi warning karena hasil tersebut sebaiknya tidak menjadi satu-satunya bukti validasi.

## Belajarnya tidak cuma “tanya → dapat jawaban”

Ramu menggunakan bantuan bertahap: memberi penjelasan/petunjuk secukupnya, memberi kesempatan mencoba, mengoreksi miskonsepsi, lalu mengurangi bantuan ketika mahasiswa mulai mampu. Untuk latihan ujian, pertanyaan dapat diberikan sebelum kunci dan topik yang masih rapuh dapat masuk ke review queue.

Desain ini bertujuan membuat AI membantu **proses belajar**, bukan otomatis menggantikan proses tersebut. Dasar riset, interpretasi, dan keterbatasannya dibahas di [`docs/LANDASAN-PEMBELAJARAN.md`](docs/LANDASAN-PEMBELAJARAN.md).

Ramu tidak mengklaim penelitian tersebut membuktikan Ramu efektif. Efektivitas framework tetap harus diuji melalui behavior eval dan penggunaan nyata.

## Struktur repo

```text
ramu/
├── core/        prinsip dasar Ramu
├── protocols/   spesifikasi perilaku belajar, tugas, review, dan latihan
├── learning/    template desain state belajar
├── packs/       paket kampus / program studi / semester
├── sources/     registry sumber dan kebijakan freshness
├── evals/       contract + behavior eval
├── schemas/     kontrak data terstruktur
├── scripts/     validator, freshness check, dan behavior runner
├── docs/        panduan, riset, validasi, dan pilot
├── site/        GitHub Pages
└── .github/     workflow, issue templates, dan aset
```

## Yang diuji otomatis

CI rutin menjalankan:

```bash
python scripts/validate_repo.py
python scripts/run_behavior_evals.py --dry-run
python scripts/check_source_freshness.py
```

Validator memeriksa antara lain:

- total SKS dan file mata kuliah pada manifest;
- `pack_version` dan metadata verifikasi course pack;
- struktur source registry;
- ID eval yang unik;
- learner-state templates dan format runtime **Catatan Belajar Terbaru**;
- contract marker pada Project Instructions/protokol/course pack;
- seluruh behavior case memiliki context file yang valid.

Contract test **bukan bukti bahwa model selalu berperilaku benar**. Tujuannya mencegah regresi struktural, misalnya guardrail “jangan mengarang DOI”, “jangan menebak screenshot”, atau “bedakan modul dengan aturan terbaru” hilang tanpa sengaja.

## Behavior eval nyata

Workflow **Behavior Evals** adalah gate manual karena memakai API dan hasil model bersifat probabilistik.

Saat dijalankan, maintainer memilih:

- model kandidat;
- model judge;
- case yang akan diuji (`all` atau subset seperti `E01,E05,E08`);
- minimum pass rate.

Run menghasilkan respons kandidat, hasil judge, skor, penggunaan token, summary, dan artifact JSON untuk audit.

**Status public beta saat ini:** wiring/dataset eval divalidasi oleh CI, tetapi hasil behavior eval nyata belum boleh dianggap bukti stabilitas sebelum workflow tersebut benar-benar dijalankan dan hasilnya direview. Panduan eval ada di [`evals/behavior/README.md`](evals/behavior/README.md).

## Source freshness

`sources/registry.json` membedakan sumber kanonik, sumber sekunder, dan community signal. Setiap sumber memiliki tanggal verifikasi dan interval review.

Workflow mingguan memeriksa dua hal:

1. apakah sumber aktif sudah melewati jadwal review;
2. apakah watched URL masih dapat dijangkau.

URL yang tidak dapat dijangkau memicu review, tetapi **tidak otomatis dianggap bukti bahwa isi/fakta sumber berubah**.

Dokumentasi produk yang cepat berubah memakai interval review lebih pendek daripada katalog akademik tahunan.

## Status kesiapan

| Area | Status |
|---|---|
| Source akademik paket awal | terverifikasi terhadap sumber yang dicatat |
| Static contracts / dry-run eval | otomatis di CI |
| Source freshness monitoring | otomatis mingguan |
| Behavior eval nyata | tersedia, perlu dijalankan dan direview |
| Pilot pengguna | public beta; protokol tersedia |
| License | MIT |
| Stabil / fully validated | **belum diklaim** |

Public beta berarti Ramu sudah cukup terstruktur untuk dicoba pengguna lain sambil failure mode dikumpulkan. Itu bukan janji bahwa semua model, semua jenis tugas, atau semua kondisi Project sudah tervalidasi.

Lihat [`docs/PILOT-PUBLIC-BETA.md`](docs/PILOT-PUBLIC-BETA.md) untuk cara menguji activation, setup friction, return use, dan behavior failure pada pengguna nyata.

## Berkontribusi

Kontribusi dokumentasi, source update, behavior eval, tooling, dan course pack baru diterima melalui pull request. Baca [`CONTRIBUTING.md`](CONTRIBUTING.md) sebelum mengirim perubahan.

Masalah keamanan/prompt injection/secret handling dibahas di [`SECURITY.md`](SECURITY.md).

Ramu dilisensikan dengan [MIT License](LICENSE).

---

<p align="center">
  <b>Mulai kecil → <a href="https://man612.github.io/ramu/setup.html">pasang satu mata kuliah dulu</a></b>
</p>

<p align="center">
  <sub>Proyek independen. Bukan layanan resmi Universitas Terbuka maupun OpenAI.</sub>
</p>
