# Arah Proyek

Dokumen ini menjelaskan bentuk Ramu sebagai proyek: apa yang ingin dijaga, bagaimana pack disusun, dan bagian mana yang sebaiknya tetap generik ketika periode atau institusi baru ditambahkan.

## Tujuan

Ramu menyiapkan workspace akademik yang bisa dipasang ke platform AI tanpa mengharuskan pengguna memahami prompt engineering atau struktur repository.

Implementasi saat ini memakai **ChatGPT Projects**. Core, pack, source registry, dan eval sengaja disimpan sebagai artefak terpisah dari UI produk, sehingga bagian yang masih relevan dapat dipakai kembali bila platform utama berubah di masa depan.

## Dua lapisan utama

Secara arsitektur ada dua lapisan besar:

1. **Core** — prinsip, protocol, learner-state contract, aturan sumber, dan failure mode yang berlaku luas.
2. **Pack** — konteks institusi, program, tahun akademik, periode, mata kuliah, sumber, versi, dan eval yang memang spesifik pada konteks tersebut.

Eval di dalam pack dapat dikomposisi dari beberapa scope:

```text
core → institution → program → pack
```

`institution` dan `program` opsional. Aturan ditempatkan pada scope paling sempit yang masih benar-benar reusable, supaya case yang sama tidak perlu disalin ke setiap semester.

## Katalog pack

`packs/index.json` adalah pintu masuk tooling. Setiap entry menunjuk ke satu `manifest.json`, lalu validator, website, Manual Eval Kit, dan behavior eval membaca detail pack dari sana.

Struktur UT S1 Akuntansi saat ini:

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

Path tersebut adalah bentuk pack UT yang tersedia sekarang, bukan template wajib untuk seluruh institusi.

## Unit utama

- **Pack catalog** — daftar pack yang bisa ditemukan tooling dan site.
- **Manifest** — identity, periode, daftar mata kuliah, source registry, eval suite, versi, dan metadata pack.
- **Course pack** — konteks dan workflow khusus satu mata kuliah.
- **Project Instructions** — aturan runtime yang dipasang ke ChatGPT Project.
- **Source registry** — sumber yang dipakai beserta authority, fungsi, freshness, dan claim penting.
- **Eval suite** — regression case pada scope core, institusi, program, atau pack.
- **Site** — antarmuka untuk memilih pack, menyalin instruksi, dan mengambil course pack.

## Identity mesin dan label manusia

Identity mesin dibuat stabil dan terpisah dari label yang dilihat pengguna. Contoh:

```text
institution_id: universitas-terbuka
institution:    Universitas Terbuka

program_id:     universitas-terbuka.s1-akuntansi
program:        S1 Akuntansi
```

Label dapat diperbaiki tanpa mengganti ID. Sebaliknya, ID yang sudah merujuk satu entitas tidak dipakai ulang untuk entitas lain.

Identity juga dipakai saat menyusun eval dan registry:

- scope `institution` merujuk `institution_id`;
- scope `program` merujuk `program_id`;
- scope `pack` merujuk `id` pack;
- scoped source registry membawa identity yang sesuai dengan pack yang menggunakannya.

Validator lintas-file memeriksa hubungan ini supaya sebuah pack tidak tanpa sengaja menarik registry atau suite milik konteks lain.

## Periode akademik

Periode memakai dua metadata:

```text
period_id:    semester-02
period_label: Semester 2
```

`period_id` bersifat machine-safe dan stabil. `period_label` mengikuti istilah yang benar-benar digunakan institusi dan menjadi prefix nama Project.

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

Dengan begitu tooling tidak perlu berasumsi bahwa setiap institusi memakai semester.

## Komposisi eval

Manifest menyusun suite dari aturan paling umum menuju paling spesifik:

```text
core
 ↓
institution   (opsional)
 ↓
program       (opsional)
 ↓
pack
```

Pack UT yang tersedia sekarang memakai:

```text
core → universitas-terbuka → id.ut.accounting-s1.2026-2027.s2
core → universitas-terbuka → id.ut.accounting-s1.2026-2027.s3
```

Konflik katalog pusat dengan halaman regional UT, misalnya, berada pada suite institusi karena masalah itu dapat muncul pada lebih dari satu periode. Sebaliknya, current-vs-old metadata AKM II Semester 3 tetap berada pada pack Semester 3 karena konteksnya memang spesifik.

Validator menjaga beberapa invariant penting:

- core berada di awal dan pack di akhir;
- scope tidak mundur dari yang lebih spesifik ke yang lebih umum;
- `scope_ref` cocok dengan identity manifest;
- ID case tetap unik setelah seluruh suite digabung;
- contract dan behavior case tetap berpasangan.

Behavior `defaults` boleh dioverride oleh suite yang lebih spesifik, tetapi regression case dengan ID yang sama tidak boleh tertimpa diam-diam.

## Schema dan semantic validation

Validasi dibagi dua karena masalah yang diperiksa juga berbeda.

**JSON Schema Draft 2020-12** memeriksa bentuk katalog, manifest, source registry, contract, dan behavior file. Schema-nya sendiri ikut divalidasi terhadap meta-schema.

**Semantic/cross-file validation** memeriksa hubungan yang tidak cukup dinyatakan dalam satu JSON file: identity catalog↔manifest, scoped registry/eval, keberadaan file, source dependency, total SKS, suite ordering, duplicate case ID, dan wiring contract↔behavior.

Keduanya dijalankan di CI.

## Maintainer pack

Field `maintainer` menunjukkan siapa yang memelihara pack di repository:

- `ramu` — **Ramu Maintained**, direview dan dipelihara di repository utama;
- `community` — kontribusi komunitas dengan ownership/review yang harus terlihat jelas.

Status ini tidak menyatakan bahwa pack resmi diterbitkan universitas. Source resmi tetap dinilai terpisah dari siapa yang memelihara pack.

## Versioning

Data akademik selalu dipasangkan dengan tahun akademik, periode, `pack_version`, dan tanggal verifikasi. Jika kurikulum berubah, perubahan masuk ke jalur tahun/periode/versi yang sesuai; pack lama tetap dapat ditelusuri sebagai snapshot.

Beberapa versi memiliki fungsi berbeda:

- `packs/index.json.version` untuk kontrak katalog;
- `schema_version` untuk bentuk manifest;
- `contract_version` untuk kontrak evaluasi;
- `pack_version` untuk isi/config course pack yang dipakai pengguna.

Perubahan metadata internal tidak otomatis berarti course pack perlu versi baru. Sebaliknya, perubahan yang memengaruhi isi/config yang benar-benar dipakai perlu dicatat pada `pack_version`.

## Status pack

- `source-verified` — data dan aturan utama sudah diperiksa terhadap sumber primer; behavior belum diklaim selesai sepenuhnya;
- `verified` — source dan behavior validation yang relevan sudah direview sesuai standar release saat itu;
- `community` — kontribusi pihak lain yang belum mencapai level maintained/verified;
- `experimental` — format atau workflow masih diuji;
- `deprecated` — sudah digantikan atau tidak lagi direkomendasikan untuk penggunaan baru.

`verified` tetap sebuah snapshot terhadap versi, tanggal, dan environment yang diuji. Bukan janji bahwa output model akan selalu sama atau selalu benar.

## Validasi tanpa API

Penggunaan normal dan static validation tidak membutuhkan OpenAI API.

- JSON Schema + semantic validation berjalan lokal/CI;
- manual validation dijalankan langsung di ChatGPT Projects;
- automated behavior eval melalui API tersedia sebagai QA tambahan.

Manual Eval Kit memakai suite yang sama untuk menghasilkan checklist tanpa API.

## Di luar ruang lingkup

Ramu tidak diarahkan menjadi bank jawaban tugas, LMS pengganti kampus, tempat menyimpan materi berhak cipta, atau sistem yang mengklaim AI selalu benar. Fokusnya tetap pada workspace belajar, sumber yang bisa ditelusuri, dan cara menguji perilaku penting saat pack berkembang.
