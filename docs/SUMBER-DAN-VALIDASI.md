# Sumber dan Validasi

Ramu membedakan **sumber resmi**, **literatur akademik**, dan **sinyal komunitas**. Ketiganya berguna, tetapi fungsinya tidak sama dan tidak disimpan selamanya dalam satu registry raksasa.

## Registry berscope

Source machine-readable dibagi menurut scope:

- [`../sources/registry.json`](../sources/registry.json) — source global/runtime seperti dokumentasi platform AI;
- `packs/<institusi>/source-registry.json` — source institusi;
- registry program/pack dapat ditambahkan bila memang diperlukan.

Setiap `manifest.json` pack menyebut `source_registries` yang menjadi dependency. Validator memastikan source yang dirujuk manifest benar-benar ada dan ID source tidak duplikat lintas registry.

Setiap entry source memiliki:

- `authority` — penerbit/otoritas;
- `canonical_for` — jenis klaim yang boleh menjadikannya sumber utama;
- `verified_at` — kapan terakhir diperiksa manusia;
- `review_interval_days` — kapan perlu review ulang;
- `watch` — apakah source watch mencoba URL;
- `status` — `active`, `secondary`, atau `signal-only`.

Dengan cara ini, “domain resmi” tidak otomatis berarti “sumber kanonik untuk semua klaim”.

## Contoh pack pertama: UT S1 Akuntansi 2026/2027 Semester 2

Untuk data kurikulum/aturan UT, prioritasnya:

1. katalog/pedoman pusat Universitas Terbuka untuk tahun akademik yang sesuai;
2. laman fakultas/program studi pusat;
3. laman UT Daerah sebagai pelengkap bila tidak bertentangan dengan source kanonik;
4. forum/komunitas sebagai sinyal masalah UX, bukan aturan akademik.

Registry institusinya berada di [`../packs/universitas-terbuka/source-registry.json`](../packs/universitas-terbuka/source-registry.json).

Sumber utama pack saat verifikasi 14 Agustus 2026:

- **Katalog Kurikulum Program Studi FEB, FHISIP, FKIP, FST UT 2026/2027**, cetakan Juli 2026;
- **Pedoman Sistem Penyelenggaraan Universitas Terbuka 2026/2027**, Juni 2026;
- laman resmi Program Studi S1 Akuntansi FEB UT.

Katalog pusat mencatat Semester 2 sebanyak **16 SKS**:

- EACC4104 Perpajakan — 3 SKS;
- EACC4103 Akuntansi Keuangan Menengah I — 3 SKS;
- EMBS4210 Manajemen Keuangan — 3 SKS;
- ECON4102 Pengantar Ekonomi Mikro — 3 SKS;
- EMBS4101 Manajemen — 4 SKS.

Katalog juga menandai EACC4103 AKM I sebagai BP/BPro. Detail akademik seperti ini milik pack, bukan core Ramu; pack periode/program/universitas lain harus mempunyai source dan verifikasi sendiri.

Pack tersebut memakai `period_id: semester-02` dan `period_label: Semester 2`. Field generic Ramu tidak bernama `semester`; institusi yang memakai trimester, quarter, term, atau academic session lain tetap menggunakan `period_id` + `period_label` sesuai sistem mereka.

## Contoh konflik source resmi

Saat validasi awal ditemukan halaman UT Banjarmasin masih berbeda dengan katalog pusat untuk beberapa data Semester 2. Karena registry menandai halaman regional sebagai `secondary` dan katalog pusat sebagai source kanonik untuk struktur kurikulum, Ramu tidak menggabungkan kedua nilai secara diam-diam.

Failure mode tersebut sekarang menjadi **regression case tingkat institusi Universitas Terbuka**, bukan case yang harus dicopy ke setiap periode. Pack UT lain dapat reuse suite institusi yang sama; universitas lain dapat mendefinisikan hierarchy source/eval mereka sendiri tanpa mewarisi aturan UT.

Konflik source juga bisa terjadi **di dalam authority yang sama**. Pada review 28 Agustus 2026, artikel khusus Study Mode milik OpenAI menyatakan Study tidak tersedia di Projects, sementara artikel Projects masih mencantumkan Study Mode pada daftar tools. Ramu tidak memilih salah satunya secara diam-diam untuk membuat klaim integrasi yang pasti; konflik itu dicatat di registry dan fitur tersebut tidak dijadikan dependency runtime sampai dokumentasinya konsisten.

## Source freshness

`python scripts/check_source_freshness.py` menemukan seluruh registry global dan `packs/**/source-registry.json`, lalu memeriksa umur verifikasi dan—untuk `watch: true`—reachability URL.

Workflow **Source Freshness Watch** berjalan mingguan. Source aktif yang overdue atau watched URL yang gagal sesuai gate akan meminta review. Namun:

- URL hidup bukan bukti isi masih terbaru;
- URL gagal bukan bukti fakta berubah;
- perubahan HTML/hash bukan otomatis perubahan aturan;
- `verified_at` hanya diperbarui setelah maintainer benar-benar membaca/membandingkan source.

## Validasi pack, period metadata, dan eval suites

`python scripts/validate_repo.py` memeriksa semua manifest yang terdaftar di `packs/index.json`, `period_id`/`period_label`, source dependency, course file, total SKS, version marker, Project Instructions, serta seluruh ordered `eval_suites` yang dipakai pack.

`period_id` harus machine-safe dan sama antara katalog dengan manifest. `period_label` wajib eksplisit untuk UI. Site validator juga menolak asumsi `item.semester`/`manifest.semester` atau fallback yang membentuk `Semester ...`, supaya generic tooling tidak kembali mengunci satu jenis kalender akademik.

Eval dapat disusun dari scope paling umum ke paling spesifik:

```text
core → institution → program → pack
```

Scope `institution` dan `program` bersifat opsional. Validator memastikan core berada di awal, pack berada di akhir, scope tidak mundur, `scope_ref` cocok, ID case tidak duplikat setelah merge, dan setiap contract case mempunyai behavior case yang sesuai.

CI kemudian menjalankan dry-run eval **per pack**. Jadi ketika periode berikutnya atau institusi baru ditambahkan ke katalog, pack tersebut ikut menjadi bagian validation matrix tanpa menambah path hardcode di workflow.

## ChatGPT/OpenAI sebagai source produk

Fitur ChatGPT dapat berubah lebih cepat daripada kurikulum akademik sehingga dokumentasi produk berada di global registry dengan interval review lebih pendek. Ramu tidak menjadikan nama model, Study Mode, atau satu detail UI sebagai dependency permanen bila workflow inti dapat dibuat lebih netral.

Pada review **28 Agustus 2026**:

- dokumentasi Projects tetap menjadi source utama untuk workspace Project, files/sources, Project Instructions, dan memory;
- Project memory saat ini dapat dipilih saat membuat Project dan dapat diubah kemudian melalui **Project settings → Memory**; perubahan dapat memerlukan waktu beberapa jam untuk berlaku;
- artikel khusus Study Mode menyatakan Study tidak tersedia di Projects, tetapi artikel Projects masih mencantumkan Study Mode sebagai tool—sehingga status integrasinya diperlakukan sebagai **unresolved official-doc conflict**;
- Data Controls FAQ tetap menjadi source utama untuk pengaturan penggunaan percakapan/data ChatGPT.

Karena konflik tersebut, Ramu tidak menyuruh pengguna mengaktifkan Study Mode di dalam Project dan tidak menjadikannya bagian dari kontrak runtime. Guardrail belajar Ramu berasal dari Project Instructions, protocols, course context, dan eval contract sendiri.

Source produk yang direview ada di [`../sources/registry.json`](../sources/registry.json). Tanggal verifikasi source harus dibaca sebagai snapshot, bukan cap “benar selamanya”.
