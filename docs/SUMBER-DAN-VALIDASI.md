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

## Claim-level evidence

Source yang sama dapat memuat beberapa klaim dengan umur dan tingkat kepastian berbeda. Bahkan dokumentasi resmi dalam authority yang sama dapat tidak sinkron. Karena itu registry juga dapat menyimpan `claims` terpisah.

Setiap claim mencatat:

- `status`: `confirmed`, `conflicted`, `needs-review`, atau `deprecated`;
- `summary`: klaim yang sedang dinilai;
- `evidence`: source ID, locator/bagian dokumen, dan observation yang benar-benar ditemukan saat review;
- `reviewed_at` + `review_interval_days` khusus claim tersebut;
- `operational_policy` untuk claim `conflicted`, supaya runtime/UX Ramu tetap punya fallback yang aman tanpa berpura-pura konflik sudah selesai.

Dengan struktur ini, Ramu dapat mengatakan “dua halaman resmi masih berbeda” tanpa harus menjadikan seluruh domain/source sebagai tidak tepercaya.

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

Konflik source juga bisa terjadi **di dalam authority yang sama**. Pada review 29 Agustus 2026, dua kasus produk OpenAI masih relevan:

- artikel khusus Study Mode menyatakan Study tidak tersedia di Projects, sementara artikel Projects masih mencantumkan Study Mode pada daftar tools;
- release notes dan guidance Projects terbaru menyatakan memory existing Project dapat diubah lewat Project settings, tetapi bagian FAQ Projects yang masih terindeks juga menyimpan wording lama bahwa Project lama harus dibuat ulang untuk memakai project-only memory.

Ramu tidak memilih salah satu wording secara diam-diam. Kedua kasus disimpan sebagai claim `conflicted` dengan evidence dan fallback operasional. Study Mode tidak menjadi dependency runtime; untuk memory, setup Project baru memilih Project-only sejak awal, sedangkan Project lama mencoba menu Memory dan membuat Project baru bila opsi itu belum tersedia pada akun/app tersebut.

## Source freshness

`python scripts/check_source_freshness.py` menemukan seluruh registry global dan `packs/**/source-registry.json`, lalu memeriksa source **dan claim**.

Workflow **Source Freshness Watch** berjalan mingguan. Gate sekarang mencakup:

- umur `verified_at` source;
- reachability URL untuk `watch: true`;
- keberadaan source ID yang dipakai evidence claim;
- `operational_policy` untuk conflict claim;
- umur `reviewed_at` claim.

Source/claim yang overdue meminta review. Namun:

- URL hidup bukan bukti isi masih terbaru;
- URL gagal bukan bukti fakta berubah;
- perubahan HTML/hash bukan otomatis perubahan aturan;
- satu halaman resmi dapat memuat bagian dengan freshness berbeda;
- `verified_at`/`reviewed_at` hanya diperbarui setelah maintainer benar-benar membaca evidence yang relevan.

Ramu sengaja tidak memakai hash HTML mentah sebagai kebenaran semantik untuk halaman produk dinamis. Hash mudah berubah karena markup/navigation tanpa perubahan fakta, sementara perubahan fakta juga dapat terjadi pada URL yang sama.

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

Pada review **29 Agustus 2026**:

- dokumentasi Projects tetap menjadi source utama untuk workspace Project, files/sources, Project Instructions, dan memory;
- release notes OpenAI ditambahkan sebagai source resmi untuk kronologi perubahan produk;
- existing-Project memory diperlakukan sebagai claim conflicted karena guidance terbaru dan FAQ lama belum sepenuhnya sinkron;
- Study Mode di dalam Projects tetap claim conflicted antara artikel Study Mode dan artikel Projects;
- Data Controls FAQ tetap menjadi source utama untuk pengaturan penggunaan percakapan/data ChatGPT;
- label tombol Project Sources dapat berubah, sehingga setup Ramu menjelaskan fungsi dan memberi contoh label tanpa menjadikannya kontrak permanen.

Karena konflik tersebut, Ramu tidak menyuruh pengguna mengaktifkan Study Mode di dalam Project dan tidak menjadikannya bagian dari kontrak runtime. Guardrail belajar Ramu berasal dari Project Instructions, protocols, course context, dan eval contract sendiri.

Source/claim produk yang direview ada di [`../sources/registry.json`](../sources/registry.json). Tanggal verifikasi source dan review claim harus dibaca sebagai snapshot, bukan cap “benar selamanya”.
