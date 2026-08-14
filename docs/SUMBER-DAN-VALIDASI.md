# Sumber dan Validasi

Ramu membedakan **sumber resmi**, **literatur akademik**, dan **sinyal komunitas**. Ketiganya berguna, tetapi fungsinya tidak sama.

Daftar sumber machine-readable ada di [`../sources/registry.json`](../sources/registry.json). Dokumen ini menjelaskan cara mengambil keputusan dari registry tersebut.

## Aturan sumber

Untuk data kurikulum dan aturan UT, prioritasnya:

1. katalog/pedoman pusat Universitas Terbuka untuk tahun akademik yang sesuai;
2. laman fakultas/program studi pusat;
3. laman UT Daerah;
4. forum/komunitas hanya sebagai sinyal masalah UX, bukan sumber aturan akademik.

Untuk fitur ChatGPT, dokumentasi resmi OpenAI menjadi sumber utama. Forum OpenAI dipakai untuk menemukan pola keluhan dan failure mode yang perlu diantisipasi, bukan sebagai spesifikasi produk.

## Validasi UT 2026/2027

Sumber utama paket Semester 2:

- **Katalog Kurikulum Program Studi FEB, FHISIP, FKIP, FST UT 2026/2027**, cetakan Juli 2026.
- **Pedoman Sistem Penyelenggaraan Universitas Terbuka 2026/2027**, Juni 2026.
- laman resmi Program Studi S1 Akuntansi FEB UT.

Katalog pusat terbaru mencatat Semester 2 S1 Akuntansi sebanyak **16 SKS**:

- EACC4104 Perpajakan — 3 SKS;
- EACC4103 Akuntansi Keuangan Menengah I — 3 SKS;
- EMBS4210 Manajemen Keuangan — 3 SKS;
- ECON4102 Pengantar Ekonomi Mikro — 3 SKS;
- EMBS4101 Manajemen — 4 SKS.

Katalog juga menandai **EACC4103 AKM I sebagai BP/BPro**, dan pedoman penyelenggaraan memasukkannya sebagai mata kuliah berpraktik Semester 2. PRATON untuk kelompok mata kuliah tersebut menggunakan studi kasus/problem solving berkesinambungan; mahasiswa wajib mengikuti PRATON dan UAS, mengerjakan minimal 5 dari 8 tugas, dengan kontribusi PRATON 60% dan UAS 40%.

## Contoh ketidaksinkronan sumber resmi

Saat validasi 14 Agustus 2026 ditemukan bahwa halaman **UT Banjarmasin – Program Studi Akuntansi (S1)** masih berbeda dengan katalog pusat Juli 2026 pada beberapa data Semester 2. Contohnya:

- AKM I masih memakai bahan ajar `EKMA4210 Akuntansi Keuangan Menengah I (Edisi 3)` dan layanan `T`, sedangkan katalog pusat menampilkan bahan ajar `EACC4103 Akuntansi Keuangan Menengah I` dengan `BP/BPro`;
- Manajemen Keuangan ditandai `WT` pada halaman regional, sedangkan katalog pusat menandainya `T`;
- Manajemen tidak menampilkan penanda layanan pada halaman regional, sedangkan katalog pusat menandainya `WT`.

Ramu memakai **katalog pusat terbaru untuk tahun akademik terkait** sebagai sumber kanonik untuk struktur kurikulum dan mencatat ketidaksinkronan seperti ini agar course pack tidak mengikuti halaman regional yang belum diperbarui. Jika dokumen pusat yang lebih baru menggantikan katalog tersebut, pack harus diperiksa ulang.

## Source registry

Setiap entri di registry memiliki:

- `authority` — siapa penerbit/otoritasnya;
- `canonical_for` — jenis klaim apa yang boleh menjadikannya sumber utama;
- `verified_at` — kapan terakhir diperiksa manusia;
- `review_interval_days` — berapa lama sebelum perlu review ulang;
- `watch` — apakah source watch perlu mencoba URL tersebut;
- `status` — `active`, `secondary`, atau `signal-only`.

Dengan cara ini, “sumber resmi” tidak otomatis berarti “sumber paling tepat untuk semua hal”.

## Freshness dan source watch

`python scripts/check_source_freshness.py` memeriksa umur verifikasi. Workflow `.github/workflows/source-watch.yml` menjalankannya setiap minggu dan mencoba mengakses URL yang ditandai `watch: true`.

Kegagalan akses sesaat hanya menjadi warning. Sebaliknya, sumber aktif yang melewati interval review membuat workflow gagal agar maintainer tahu bahwa verifikasi manual sudah jatuh tempo.

Ramu **tidak** menganggap URL yang masih hidup sebagai bukti bahwa isinya masih paling baru. Perubahan fakta tetap harus diverifikasi dari dokumen/otoritas yang tepat.

## Sinyal masalah mahasiswa UT

Forum komunitas PojokUT dan kanal komunitas mahasiswa memperlihatkan pertanyaan berulang tentang:

- langkah setelah mendapat NIM;
- mata kuliah yang belum muncul;
- tracking bahan ajar;
- akses/login;
- interpretasi nilai Tuton dan ujian;
- registrasi ulang mata kuliah.

Ramu tidak menganggap keluhan komunitas sebagai statistik resmi. Temuan tersebut hanya dipakai untuk menentukan fitur yang masuk akal.

Tanggal verifikasi sumber utama: **14 Agustus 2026**.
