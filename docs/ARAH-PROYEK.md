# Arah Proyek

## Tujuan

Ramu menyediakan konfigurasi workspace akademik yang bisa dipasang ke platform AI tanpa memaksa mahasiswa belajar prompt engineering.

Implementasi pertama memakai **ChatGPT Projects**, tetapi format core dan pack tidak dibuat sebagai dokumentasi produk OpenAI semata. Jika platform utama berubah, course context, source governance, dan aturan belajar tetap dapat digunakan kembali melalui adapter/panduan baru.

## Arsitektur

Ramu dibagi menjadi dua lapisan besar:

1. **Core** — prinsip, protocol, learner-state contract, source rules, dan eval universal yang seharusnya dapat dipakai lintas kampus/prodi.
2. **Pack** — konteks institusi + program + tahun akademik + semester beserta mata kuliah, sumber, versi, dan eval khususnya.

`packs/index.json` adalah katalog machine-readable. Setiap entry menunjuk satu `manifest.json`. Tooling tidak boleh mengunci path satu semester tertentu; validator, website, manual eval, dan automated behavior eval harus menemukan pack melalui katalog/manifest.

```text
packs/
├── index.json
├── universitas-terbuka/
│   ├── source-registry.json
│   └── s1-akuntansi/
│       └── 2026-2027/
│           ├── semester-02/
│           └── semester-03/        # saat tersedia
└── universitas-lain/               # saat ada pack terverifikasi/request
```

## Unit utama

- **Core** — prinsip umum yang jarang berubah.
- **Pack catalog** — daftar pack yang dapat ditemukan tooling/site.
- **Pack manifest** — metadata institusi/program/semester, course list, source registry, eval suite, dan version.
- **Course pack** — konfigurasi siap upload untuk satu mata kuliah.
- **Project Instructions** — perilaku runtime yang ditempel ke Project.
- **Core eval** — failure mode universal seperti hallucinated citation, prompt injection, dan state/version conflict.
- **Pack eval** — behavior yang hanya masuk akal untuk mata kuliah/institusi tertentu.
- **Source registry** — dapat berscope global, institusi, program, atau pack agar tidak menjadi satu file raksasa.
- **Site** — membaca katalog + manifest, bukan hardcode semester tertentu.

## Maintainer pack

Field `maintainer` membedakan asal pemeliharaan tanpa memakai istilah “official” yang bisa disalahartikan sebagai resmi dari kampus:

- `ramu` — **Ramu Maintained**, dipelihara/review langsung dalam repository utama;
- `community` — kontribusi komunitas yang ownership/review-nya harus terlihat jelas.

Status sumber dan status maintainer adalah dua hal berbeda. Community pack tetap bisa memiliki source resmi, dan Ramu Maintained pack tetap tidak boleh mengklaim sebagai layanan resmi universitas.

## Prinsip versioning

Data akademik selalu ditulis bersama tahun akademik, `pack_version`, dan tanggal verifikasi. Jika kurikulum berubah, pack baru dibuat pada jalur versi/tahun/semester yang sesuai; pack lama tidak diam-diam ditimpa seolah masih berlaku.

Jika dua course pack untuk konteks yang sama terpasang sekaligus, versi yang sesuai manifest aktif diprioritaskan dan versi lama sebaiknya dihapus dari Project Sources.

## Status pack

- `source-verified` — data dan aturan utama sudah diperiksa terhadap sumber primer, tetapi behavior belum dinyatakan terverifikasi penuh.
- `verified` — sumber + behavior validation yang relevan sudah direview sesuai standar release saat itu.
- `community` — kontribusi pihak lain yang belum memenuhi level maintained/verified penuh.
- `experimental` — format/workflow/pack masih diuji.
- `deprecated` — pack sudah digantikan atau tidak lagi layak direkomendasikan untuk penggunaan baru.

Status `verified` tetap berupa snapshot terhadap pack version + tanggal + environment/model/product state yang diuji, bukan janji keluaran AI selalu sama selamanya.

## Validasi tanpa dan dengan API

Ramu tidak membutuhkan OpenAI API untuk dipakai mahasiswa.

- static validation: otomatis dan gratis;
- manual validation di ChatGPT Projects: gratis dan menguji runtime produk yang sebenarnya;
- automated API behavior eval: opsional sebagai regression/benchmark tambahan ketika API tersedia.

## Bukan target Ramu

- menyimpan jawaban tugas massal;
- menyalin BMP/materi berhak cipta;
- menjadi LMS pengganti kampus;
- menebak nilai akhir mahasiswa;
- menjanjikan keluaran AI selalu benar atau kebal prompt injection;
- mengunci pengguna ke satu model, plan, atau vendor untuk selamanya.
