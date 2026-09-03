# Sumber dan Validasi

Sumber di repository dibedakan berdasarkan fungsi, bukan sekadar domain. Dokumen resmi, literatur akademik, halaman regional, dan diskusi komunitas bisa sama-sama berguna, tetapi tidak punya bobot yang sama untuk setiap klaim.

## Registry berdasarkan scope

Source machine-readable dapat berada di beberapa level:

- [`../sources/registry.json`](../sources/registry.json) — source global/runtime, misalnya dokumentasi platform AI;
- `packs/<institusi>/source-registry.json` — source yang berlaku pada tingkat institusi;
- registry program atau pack — dipakai bila sumbernya memang lebih sempit.

Setiap `manifest.json` menyebut `source_registries` yang menjadi dependency pack. Validator memeriksa keberadaan registry, kecocokan identity, dan keunikan source ID.

Entry source menyimpan beberapa metadata penting:

- `authority` — penerbit atau otoritas;
- `canonical_for` — jenis klaim yang boleh menjadikannya rujukan utama;
- `verified_at` — tanggal terakhir source benar-benar diperiksa;
- `review_interval_days` — interval review;
- `watch` — apakah URL ikut dipantau;
- `status` — `active`, `secondary`, atau `signal-only`.

Dengan model ini, sebuah halaman bisa resmi tetapi tetap hanya menjadi sumber sekunder untuk klaim tertentu.

## Evidence per klaim

Satu source dapat memuat beberapa klaim dengan tingkat kepastian dan umur yang berbeda. Dokumentasi resmi juga kadang tidak sinkron antarhalaman. Karena itu registry dapat menyimpan `claims` terpisah.

Setiap claim mencatat:

- `status`: `confirmed`, `conflicted`, `needs-review`, atau `deprecated`;
- `summary`: klaim yang sedang dinilai;
- `evidence`: source ID, locator, dan observation dari review;
- `reviewed_at` + `review_interval_days`;
- `operational_policy` untuk claim `conflicted`, agar workflow tetap punya fallback tanpa berpura-pura konfliknya sudah selesai.

Jadi konflik dua halaman resmi bisa dicatat sebagai konflik pada klaim tertentu tanpa menurunkan kepercayaan terhadap seluruh domain.

## Hierarki source Universitas Terbuka

Untuk data kurikulum dan aturan UT, urutan prioritasnya:

1. katalog/pedoman pusat UT untuk tahun akademik yang sesuai;
2. halaman fakultas/program studi pusat dan BMP resmi;
3. halaman UT Daerah sebagai pelengkap bila tidak bertentangan dengan source pusat;
4. forum/komunitas sebagai sinyal masalah atau pengalaman pengguna, bukan aturan akademik.

Registry institusi: [`../packs/universitas-terbuka/source-registry.json`](../packs/universitas-terbuka/source-registry.json).

Source pusat yang direview untuk pack 2026/2027 pada 3 September 2026:

- **Katalog Kurikulum Program Studi FEB, FHISIP, FKIP, FST UT 2026/2027**, cetakan Juli 2026;
- **Pedoman Sistem Penyelenggaraan Universitas Terbuka 2026/2027**, Juni 2026;
- halaman resmi Program Studi S1 Akuntansi FEB UT.

Halaman regional tetap dicatat karena berguna untuk mendeteksi drift. Pada review Semester 3, salah satu halaman UT Daerah masih menampilkan metadata AKM II lama. Regression E14 menangkap failure mode ini pada scope institusi: ketika metadata regional berbeda dari katalog pusat, struktur kurikulum dan metadata mata kuliah mengikuti source pusat yang current.

## UT S1 Akuntansi 2026/2027

### Semester 2

Katalog pusat mencatat **16 SKS**:

- EACC4104 Perpajakan — 3 SKS;
- EACC4103 Akuntansi Keuangan Menengah I — 3 SKS;
- EMBS4210 Manajemen Keuangan — 3 SKS;
- ECON4102 Pengantar Ekonomi Mikro — 3 SKS;
- EMBS4101 Manajemen — 4 SKS.

EACC4103 AKM I ditandai BP/BPro. Detail seperti ini disimpan di pack karena terkait langsung dengan periode dan mata kuliah.

### Semester 3

Katalog pusat Juli 2026 mencatat **20 SKS**:

- EACC4206 Laboratorium Perpajakan — 2 SKS — II.1 — BPr/BPro;
- MKDI4203 Kewirausahaan di Era Digital — 3 SKS — I.1;
- EMBS4326 Akuntansi Manajemen — 3 SKS — I.2 — T;
- EACC4207 Sistem Informasi Akuntansi — 3 SKS — I.3 — T;
- MKDI4201 Bahasa Inggris — 3 SKS — II.2 — T;
- EACC4205 Akuntansi Keuangan Menengah II — 3 SKS — II.3 — BP/BPro;
- MKDI4202 Belajar di Era Digital — 3 SKS — II.5 — WT.

Review Semester 3 dilakukan dari source current, bukan dengan menyalin tahun sebelumnya. Beberapa perbedaan yang memengaruhi pack:

- **EACC4205 AKM II** memakai BMP `EACC4205` Edisi 1 tahun 2026 dan berstatus BP/BPro; metadata historis `EKMA4313 Edisi 3` tidak dipakai sebagai current truth;
- **EACC4206 Laboratorium Perpajakan** memakai slot II.1, BPr/BPro, dengan prasyarat EACC4104;
- **MKDI4201 Bahasa Inggris** mencantumkan layanan T;
- **MKDI4202 Belajar di Era Digital** mencantumkan WT.

Pedoman 2026/2027 juga mengonfirmasi EACC4205 dan EACC4206 berada dalam kelompok praktik/berpraktik. Untuk pola BPro terkait, PRATON berkontribusi 60%, UAS 40%, dan minimal 5 dari 8 tugas perlu dikerjakan. Kasus PRATON dapat berkesinambungan sehingga state tugas sebelumnya tidak boleh diisi dengan tebakan.

Semester 3 memiliki registry pack sendiri di [`../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-03/source-registry.json`](../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-03/source-registry.json) untuk tujuh halaman BMP aktif dan claim yang memang spesifik pada periode tersebut.

Materi kuliah berhak cipta tidak disalin ke repository.

## Metadata periode

Semester 2 memakai:

```text
period_id: semester-02
period_label: Semester 2
```

Semester 3 memakai `semester-03` + `Semester 3`.

Tooling hanya bergantung pada `period_id` dan `period_label`. Institusi lain dapat memakai trimester, quarter, term, atau academic session tanpa perlu dipaksa ke field khusus semester.

## Konflik source resmi

Konflik pusat-vs-regional UT disimpan sebagai regression tingkat institusi supaya pack UT lain bisa memakai aturan yang sama tanpa menyalin case tersebut.

Konflik juga bisa muncul di dalam authority yang sama. Status claim baru diubah setelah evidence current direview.

Pada review dokumentasi OpenAI **3 September 2026**:

- eligible existing Project dapat mengubah memory melalui **Project settings → Memory**; shared Project tetap project-only;
- Study Mode tidak berlaku pada Project conversations menurut guidance resmi current.

Data Controls pada akun personal tetap merupakan pilihan akun pengguna dan bukan dependency setup.

## Source freshness

`python scripts/check_source_freshness.py` menemukan registry global dan `packs/**/source-registry.json`, lalu memeriksa source serta claim.

Workflow **Source Freshness Watch** berjalan mingguan dan memeriksa:

- umur `verified_at`;
- reachability URL untuk `watch: true`;
- retry terbatas untuk kegagalan jaringan sementara;
- keberadaan source ID yang dipakai evidence claim;
- `operational_policy` untuk conflicted claim;
- umur `reviewed_at` claim.

Source atau claim yang melewati interval review akan ditandai. Watched URL yang tetap gagal setelah retry juga menjadi bahan review ketika scheduled workflow berjalan dengan `--fail-on-network`.

Beberapa batas penting:

- URL hidup belum membuktikan isi masih terbaru;
- URL gagal belum membuktikan fakta berubah;
- perubahan HTML belum tentu perubahan aturan;
- satu halaman dapat memuat bagian dengan freshness berbeda;
- `verified_at` dan `reviewed_at` baru diperbarui setelah evidence-nya dibaca kembali.

Hash HTML mentah tidak dipakai sebagai kebenaran semantik untuk halaman dinamis.

## Validasi pack dan eval

`python scripts/validate_repo.py` memeriksa manifest yang terdaftar di `packs/index.json`, metadata periode, source dependency, course file, total SKS, version marker, Project Instructions, dan ordered `eval_suites`.

Site validator juga memeriksa agar tooling tetap generic dan tidak kembali membangun periode dari asumsi field `semester`.

Eval disusun sebagai:

```text
core → institution → program → pack
```

Scope `institution` dan `program` opsional. Validator memastikan urutan tidak mundur, `scope_ref` cocok dengan manifest, ID case unik setelah digabung, dan setiap contract case memiliki behavior case yang sesuai.

Semester 3 menambahkan E17–E24 untuk failure mode yang benar-benar spesifik: tax-currentness, metadata lama vs current AKM II, continuity kasus PRATON, requirement/control SIA, relevant cost, business evidence, tutoring Bahasa Inggris, dan ketidakpastian isi kebijakan GenAI UT.

CI menjalankan dry-run eval per pack dari `packs/index.json`. Saat Semester 3 ditambahkan, matrix kedua muncul otomatis tanpa path khusus S3 di workflow.

## Dokumentasi produk ChatGPT/OpenAI

Fitur produk berubah lebih cepat daripada kurikulum akademik. Karena itu source produk disimpan di registry global dengan interval review yang lebih pendek.

Snapshot 3 September 2026 mencatat:

- dokumentasi Projects sebagai source utama untuk workspace, files/sources, Project Instructions, dan memory;
- release notes untuk kronologi perubahan produk;
- existing-Project memory sebagai claim `confirmed` pada eligible Project;
- Study Mode di Project conversations sebagai `confirmed` tidak tersedia;
- Data Controls FAQ sebagai source pengaturan penggunaan percakapan/data;
- label UI diperlakukan sebagai detail yang bisa berubah, sehingga panduan lebih mengutamakan fungsi daripada posisi tombol.

Registry produk: [`../sources/registry.json`](../sources/registry.json).

Semua tanggal review di repository adalah snapshot, bukan cap bahwa sebuah source akan tetap benar selamanya.
