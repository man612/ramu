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

## Source hierarchy Universitas Terbuka

Untuk data kurikulum/aturan UT, prioritasnya:

1. katalog/pedoman pusat Universitas Terbuka untuk tahun akademik yang sesuai;
2. laman fakultas/program studi pusat dan halaman BMP resmi;
3. laman UT Daerah sebagai pelengkap bila tidak bertentangan dengan source kanonik;
4. forum/komunitas sebagai sinyal masalah UX, bukan aturan akademik.

Registry institusinya berada di [`../packs/universitas-terbuka/source-registry.json`](../packs/universitas-terbuka/source-registry.json).

Sumber pusat 2026/2027 yang menjadi dependency pack UT saat review 3 September 2026:

- **Katalog Kurikulum Program Studi FEB, FHISIP, FKIP, FST UT 2026/2027**, cetakan Juli 2026;
- **Pedoman Sistem Penyelenggaraan Universitas Terbuka 2026/2027**, Juni 2026;
- laman resmi Program Studi S1 Akuntansi FEB UT.

Halaman regional tetap dicatat sebagai `secondary`. Pada review Semester 3, halaman UT Daerah yang masih memuat metadata AKM II lama menjadi bukti nyata bahwa domain resmi regional dapat tertinggal dari katalog pusat. Karena itu regression E14 sekarang bersifat **period-neutral**: source regional tidak menjadi kanonik untuk struktur kurikulum atau metadata mata kuliah ketika berbeda dari katalog pusat.

## Pack UT S1 Akuntansi 2026/2027

### Semester 2

Katalog pusat mencatat Semester 2 sebanyak **16 SKS**:

- EACC4104 Perpajakan — 3 SKS;
- EACC4103 Akuntansi Keuangan Menengah I — 3 SKS;
- EMBS4210 Manajemen Keuangan — 3 SKS;
- ECON4102 Pengantar Ekonomi Mikro — 3 SKS;
- EMBS4101 Manajemen — 4 SKS.

Katalog menandai EACC4103 AKM I sebagai BP/BPro. Detail akademik seperti ini milik pack, bukan core Ramu.

### Semester 3

Semester 3 adalah **real second-pack test** pertama Ramu. Katalog pusat Juli 2026 mencatat **20 SKS**:

- EACC4206 Laboratorium Perpajakan — 2 SKS — II.1 — BPr/BPro;
- MKDI4203 Kewirausahaan di Era Digital — 3 SKS — I.1;
- EMBS4326 Akuntansi Manajemen — 3 SKS — I.2 — T;
- EACC4207 Sistem Informasi Akuntansi — 3 SKS — I.3 — T;
- MKDI4201 Bahasa Inggris — 3 SKS — II.2 — T;
- EACC4205 Akuntansi Keuangan Menengah II — 3 SKS — II.3 — BP/BPro;
- MKDI4202 Belajar di Era Digital — 3 SKS — II.5 — WT.

Review tidak memakai Semester 3 tahun sebelumnya sebagai template fakta. Perbandingan current-vs-old menemukan perubahan operasional yang material:

- **EACC4205 AKM II** current 2026/2027 memakai BMP baru `EACC4205` Edisi 1 tahun 2026 dan berstatus BP/BPro; metadata historis `EKMA4313 Edisi 3` tidak dipakai sebagai current truth;
- **EACC4206 Laboratorium Perpajakan** current slot ujian II.1, BPr/BPro, dan mempunyai prasyarat EACC4104 Perpajakan;
- **MKDI4201 Bahasa Inggris** current row S1 Akuntansi mencantumkan T;
- **MKDI4202 Belajar di Era Digital** current row mencantumkan WT.

Pedoman 2026/2027 mengonfirmasi EACC4205 dan EACC4206 berada dalam kelompok praktik/berpraktik S1 Akuntansi. Pembelajaran diarahkan pada PRATON, studi kasus/problem solving berkesinambungan; untuk pola BPro terkait, PRATON berkontribusi 60%, UAS 40%, dan mahasiswa minimal mengerjakan 5 dari 8 tugas.

Semester 3 mempunyai registry pack sendiri di [`../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-03/source-registry.json`](../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-03/source-registry.json). Registry tersebut menyimpan tujuh halaman BMP aktif Perpustakaan UT serta claim eksplisit untuk perubahan AKM II dan aturan Lab Perpajakan/PRATON.

Pack tetap tidak menyalin BMP atau materi berhak cipta ke repository.

## Period metadata

Pack Semester 2 memakai `period_id: semester-02` dan `period_label: Semester 2`; Semester 3 memakai `semester-03` + `Semester 3`.

Field generic Ramu tidak bernama `semester`. Institusi yang memakai trimester, quarter, term, atau academic session lain tetap menggunakan `period_id` + `period_label` sesuai sistem mereka.

## Konflik source resmi

Failure mode source pusat vs regional adalah regression case tingkat **institusi Universitas Terbuka**, bukan case yang dicopy ke setiap periode. Pack UT lain reuse suite institusi yang sama; universitas lain dapat mendefinisikan hierarchy source/eval mereka sendiri tanpa mewarisi aturan UT.

Konflik juga dapat terjadi di dalam authority yang sama. Karena itu status claim hanya diubah setelah evidence current benar-benar direview.

Pada review dokumentasi OpenAI **3 September 2026**, dua konflik produk yang sebelumnya dicatat sudah dapat ditutup berdasarkan guidance resmi current:

- eligible existing Project dapat mengubah memory melalui **Project settings → Memory**; shared Project tetap project-only;
- Study Mode **tidak berlaku pada Project conversations** menurut artikel Study Mode dan guidance Projects current.

Ramu tetap tidak menjadikan Study Mode dependency. Data Controls untuk akun personal tetap diperlakukan sebagai pilihan akun pengguna, bukan syarat Ramu.

## Source freshness

`python scripts/check_source_freshness.py` menemukan seluruh registry global dan `packs/**/source-registry.json`, lalu memeriksa source **dan claim**.

Workflow **Source Freshness Watch** berjalan mingguan. Gate mencakup:

- umur `verified_at` source;
- reachability URL untuk `watch: true`;
- retry terbatas agar kegagalan jaringan sesaat tidak langsung menjadi failure final;
- keberadaan source ID yang dipakai evidence claim;
- `operational_policy` untuk conflicted claim;
- umur `reviewed_at` claim.

Source/claim yang overdue meminta review. Watched URL yang tetap gagal setelah retry juga meminta review ketika scheduled workflow memakai `--fail-on-network`. Output checker dibawa ke GitHub Actions Job Summary dan issue review supaya source/error yang bermasalah dapat diidentifikasi.

Namun:

- URL hidup bukan bukti isi masih terbaru;
- URL gagal bukan bukti fakta berubah;
- perubahan HTML/hash bukan otomatis perubahan aturan;
- satu halaman resmi dapat memuat bagian dengan freshness berbeda;
- `verified_at`/`reviewed_at` hanya diperbarui setelah maintainer benar-benar membaca evidence yang relevan.

Ramu sengaja tidak memakai hash HTML mentah sebagai kebenaran semantik untuk halaman dinamis.

## Validasi pack, period metadata, dan eval suites

`python scripts/validate_repo.py` memeriksa semua manifest yang terdaftar di `packs/index.json`, `period_id`/`period_label`, source dependency, course file, total SKS, version marker, Project Instructions, serta seluruh ordered `eval_suites` yang dipakai pack.

`period_id` harus machine-safe dan sama antara katalog dengan manifest. `period_label` wajib eksplisit untuk UI. Site validator juga menolak asumsi `item.semester`/`manifest.semester` atau fallback yang membentuk `Semester ...`, supaya generic tooling tidak kembali mengunci satu jenis kalender akademik.

Eval dapat disusun dari scope paling umum ke paling spesifik:

```text
core → institution → program → pack
```

Scope `institution` dan `program` bersifat opsional. Validator memastikan core berada di awal, pack berada di akhir, scope tidak mundur, `scope_ref` cocok, ID case tidak duplikat setelah merge, dan setiap contract case mempunyai behavior case yang sesuai.

Semester 3 menambahkan regression E17–E24 untuk failure mode yang memang pack-specific: tax-currentness, AKM II old-vs-current metadata, state kasus PRATON, SIA requirement/control, relevant cost, business evidence, language tutoring, dan ketidakpastian policy GenAI.

CI menjalankan dry-run eval **per pack** melalui matrix yang dibangun dari `packs/index.json`. Jadi penambahan Semester 3 harus menghasilkan job eval-wiring kedua tanpa menulis path baru di workflow.

## ChatGPT/OpenAI sebagai source produk

Fitur ChatGPT berubah lebih cepat daripada kurikulum akademik sehingga dokumentasi produk berada di global registry dengan interval review lebih pendek. Ramu tidak menjadikan nama model, Study Mode, atau satu detail UI sebagai dependency permanen bila workflow inti dapat dibuat lebih netral.

Pada review **3 September 2026**:

- dokumentasi Projects menjadi source utama untuk workspace Project, files/sources, Project Instructions, dan memory;
- release notes dipakai untuk kronologi perubahan produk;
- existing-Project memory saat ini berstatus `confirmed` dapat diubah untuk eligible Project;
- Study Mode di Project conversations saat ini berstatus `confirmed` tidak tersedia;
- Data Controls FAQ tetap menjadi source utama untuk pengaturan penggunaan percakapan/data ChatGPT;
- label tombol Project Sources dapat berubah, sehingga setup Ramu menjelaskan fungsi tanpa menjadikan satu label UI sebagai kontrak permanen.

Source/claim produk yang direview ada di [`../sources/registry.json`](../sources/registry.json). Tanggal verifikasi source dan review claim harus dibaca sebagai snapshot, bukan cap “benar selamanya”.
