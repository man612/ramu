# Arah Proyek

## Tujuan

Ramu menyediakan konfigurasi workspace akademik yang bisa dipasang ke platform AI tanpa memaksa mahasiswa belajar prompt engineering.

Implementasi pertama memakai **ChatGPT Projects**, tetapi format core dan pack tidak dibuat sebagai dokumentasi produk OpenAI semata. Jika platform utama berubah, course context, source governance, aturan belajar, dan kontrak evaluasi tetap dapat digunakan kembali melalui adapter/panduan baru.

## Arsitektur

Secara produk, Ramu tetap punya dua lapisan besar:

1. **Core** — prinsip, protocol, learner-state contract, source rules, dan failure mode universal yang seharusnya dapat dipakai lintas kampus/prodi.
2. **Pack** — konteks institusi + program + tahun akademik + periode beserta mata kuliah, sumber, versi, dan wiring evaluasinya.

Di dalam pack, evaluasi tidak lagi diasumsikan hanya `core + pack`. Manifest menyusun **ordered `eval_suites`** agar rule yang reusable dapat ditempatkan pada scope yang tepat: `core → institution → program → pack`.

`packs/index.json` adalah katalog machine-readable. Setiap entry menunjuk satu `manifest.json`. Tooling tidak boleh mengunci path atau jenis periode tertentu; validator, website, manual eval, dan automated behavior eval harus menemukan pack melalui katalog/manifest.

```text
packs/
├── index.json
├── universitas-terbuka/
│   ├── source-registry.json
│   ├── evals/                         # rule/eval reusable untuk UT
│   └── s1-akuntansi/
│       └── 2026-2027/
│           ├── semester-02/
│           └── semester-03/           # saat tersedia
└── universitas-lain/                  # saat ada pack terverifikasi/request
```

Folder `semester-02/` di atas adalah identitas pack UT sekarang, bukan struktur yang diwajibkan Ramu untuk semua institusi.

## Unit utama

- **Core** — prinsip umum yang jarang berubah.
- **Pack catalog** — daftar pack yang dapat ditemukan tooling/site.
- **Pack manifest** — metadata institusi/program/periode, course list, source registry, ordered `eval_suites`, dan version.
- **Period metadata** — `period_id` untuk mesin + `period_label` untuk manusia; tidak ada field universal `semester`.
- **Course pack** — konfigurasi siap upload untuk satu mata kuliah.
- **Project Instructions** — perilaku runtime yang ditempel ke Project.
- **Eval suite `core`** — failure mode universal seperti hallucinated citation, prompt injection, source freshness, dan state/version conflict.
- **Eval suite `institution`** — rule yang berlaku lintas pack pada satu institusi, misalnya cara menyelesaikan konflik source pusat-vs-regional UT.
- **Eval suite `program`** — rule reusable pada satu program studi bila memang ada failure mode yang tidak layak dinaikkan ke institusi.
- **Eval suite `pack`** — behavior yang benar-benar spesifik periode/mata kuliah pada pack aktif.
- **Source registry** — dapat berscope global, institusi, program, atau pack agar tidak menjadi satu file raksasa.
- **Site** — membaca katalog + manifest, bukan hardcode satu semester/jenis kalender tertentu.

## Kontrak periode akademik

Ramu membedakan identitas mesin dari label pengguna:

```text
period_id:    semester-02
period_label: Semester 2
```

Pack lain dapat memakai bentuk seperti:

```text
period_id:    trimester-01
period_label: Trimester 1
```

atau:

```text
period_id:    term-fall
period_label: Fall Term
```

`period_id` harus lower-case/machine-safe dan stabil untuk tooling. `period_label` mengikuti istilah resmi/manusiawi yang digunakan institusi dan menjadi prefix nama Project. Generic tooling tidak boleh menyimpulkan bahwa seluruh academic period adalah semester.

## Komposisi eval

Setiap manifest menyusun suite dari scope paling umum ke paling spesifik.

```text
core
 ↓
institution   (opsional)
 ↓
program       (opsional)
 ↓
pack
```

Pack UT S1 Akuntansi Semester 2 saat ini memakai:

```text
core → universitas-terbuka → semester-02
```

Contohnya, regression case konflik katalog pusat dan halaman regional UT berada pada suite institusi Universitas Terbuka. Semester 3 UT nanti dapat memakai suite yang sama tanpa menyalin case tersebut. Sebaliknya, universitas lain tidak ikut membawa rule UT.

Validator menjaga beberapa invariant:

- suite core harus menjadi lapisan pertama;
- suite pack harus menjadi lapisan terakhir;
- scope tidak boleh mundur dari yang lebih spesifik ke lebih umum;
- `scope_ref` harus cocok dengan identitas scope yang dipakai;
- ID case harus tetap unik setelah seluruh suite digabung;
- behavior dan contract case harus tetap berpasangan.

Behavior defaults boleh dioverride oleh suite yang lebih spesifik dan muncul kemudian, tetapi regression case yang memiliki ID sama tidak boleh ditimpa diam-diam.

## Maintainer pack

Field `maintainer` membedakan asal pemeliharaan tanpa memakai istilah “official” yang bisa disalahartikan sebagai resmi dari kampus:

- `ramu` — **Ramu Maintained**, dipelihara/review langsung dalam repository utama;
- `community` — kontribusi komunitas yang ownership/review-nya harus terlihat jelas.

Status sumber dan status maintainer adalah dua hal berbeda. Community pack tetap bisa memiliki source resmi, dan Ramu Maintained pack tetap tidak boleh mengklaim sebagai layanan resmi universitas.

## Prinsip versioning

Data akademik selalu ditulis bersama tahun akademik, `period_id`/`period_label`, `pack_version`, dan tanggal verifikasi. Jika kurikulum berubah, pack baru dibuat pada jalur versi/tahun/periode yang sesuai; pack lama tidak diam-diam ditimpa seolah masih berlaku.

`schema_version` berubah bila bentuk kontrak manifest berubah. `contract_version` dapat berubah ketika wiring/format kontrak evaluasi berubah. `pack_version` mengikuti isi/config course pack yang benar-benar dipakai mahasiswa. Karena itu migrasi metadata seperti `semester` → `period_id` tidak otomatis berarti course pack mahasiswa perlu versi baru.

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

Static CI memeriksa period metadata, menggabungkan ordered eval suites setiap pack, dan memeriksa wiring seluruh case. Manual Eval Kit menggunakan suite yang sama untuk menghasilkan checklist tanpa API.

## Bukan target Ramu

- menyimpan jawaban tugas massal;
- menyalin BMP/materi berhak cipta;
- menjadi LMS pengganti kampus;
- menebak nilai akhir mahasiswa;
- menjanjikan keluaran AI selalu benar atau kebal prompt injection;
- mengunci pengguna ke satu sistem kalender akademik, model, plan, fitur tambahan, atau vendor untuk selamanya.
