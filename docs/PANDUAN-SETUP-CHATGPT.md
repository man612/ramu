# Panduan Setup Ramu di ChatGPT

Panduan ini untuk pengguna yang ingin langsung memakai Ramu tanpa perlu memahami GitHub, prompt engineering, schema, atau tooling di belakangnya.

Ramu memakai **pack**. Satu pack mewakili konteks akademik tertentu—misalnya institusi, program studi, tahun akademik, dan periode belajar. Kamu tidak perlu memasang seluruh pack sekaligus; untuk mencoba Ramu, cukup siapkan **satu mata kuliah dulu**.

## Pilih pack yang sesuai

Buka [site Ramu](https://man612.github.io/ramu/) lalu pilih pack yang sesuai.

Pack Ramu Maintained yang tersedia untuk UT S1 Akuntansi 2026/2027 saat ini:

- **Semester 2** — 5 mata kuliah, 16 SKS;
- **Semester 3** — 7 mata kuliah, 20 SKS.

Nama Project selalu memakai label periode secara penuh. Contoh Semester 3:

- `Semester 3 • Lab Perpajakan`
- `Semester 3 • Kewirausahaan Digital`
- `Semester 3 • Akuntansi Manajemen`
- `Semester 3 • SIA`
- `Semester 3 • Bahasa Inggris`
- `Semester 3 • AKM II`
- `Semester 3 • Belajar di Era Digital`

Ramu sengaja menulis **Semester 2/3** secara penuh pada nama yang dilihat pengguna. Singkatan `S2` atau `S3` tidak dipakai sebagai label Project karena di Indonesia mudah dibaca sebagai jenjang pendidikan. ID internal seperti `.s2`, `.s3`, `semester-02/`, atau `semester-03/` tetap boleh dipakai oleh tooling.

Untuk pack lain, gunakan nama Project yang ditampilkan oleh halaman setup pack tersebut. Manifest pack memiliki `period_label` agar periode dapat ditulis jelas, termasuk bila suatu institusi memakai istilah lain seperti trimester atau term.

## Langkah 1 — pilih satu mata kuliah

Jangan setup seluruh periode hanya untuk mengetes Ramu.

Pilih satu mata kuliah yang memang sedang dipakai. Misalnya **Perpajakan** pada Semester 2 atau **AKM II** pada Semester 3.

## Langkah 2 — buat ChatGPT Project

1. Buka ChatGPT.
2. Pilih **New Project**.
3. Gunakan nama Project yang diberikan Ramu, misalnya `Semester 3 • AKM II`.
4. Gunakan **Project-only memory** agar konteks Project tidak bercampur dengan percakapan di luar Project.

Nama menu ChatGPT dapat berubah seiring pembaruan produk. Jika letaknya berbeda, cari pengaturan yang setara di Project settings.

## Langkah 3 — pasang Project Instructions

Pada halaman setup Ramu untuk pack aktif, tekan **Salin instruksi**.

Di ChatGPT buka:

`Project → ⋯ → Project settings → Project Instructions`

lalu tempel Project Instructions tersebut.

Project Instructions **bukan Project Source**. Ia adalah aturan runtime untuk cara Ramu menangani konteks, sumber, tugas, pembelajaran, dan guardrail.

## Langkah 4 — tambahkan course pack

Pada halaman setup Ramu:

1. pilih mata kuliah yang sedang disiapkan;
2. tekan **Unduh paket (.txt)**;
3. kembali ke Project ChatGPT;
4. buka area **Sources** atau **Project Sources**;
5. gunakan kontrol untuk menambahkan atau mengunggah file, lalu pilih course pack yang baru diunduh.

Nama tombol dan opsi untuk menambahkan source dapat berbeda antar akun, plan, atau versi aplikasi. Jika ChatGPT menyediakan cara untuk memakai ulang file yang sudah tersimpan di Library atau source lain, opsi yang setara tersebut juga dapat digunakan.

Course pack menjadi source tetap untuk Project tersebut. BMP, materi kelas, screenshot soal, rubrik, atau file pribadi tetap ditambahkan sendiri oleh pengguna ketika diperlukan; materi berhak cipta tidak disimpan di repo Ramu.

## Langkah 5 — langsung gunakan

Begitu satu Project selesai, langsung pakai. Tidak perlu menunggu semua mata kuliah selesai disiapkan.

Contoh:

```text
aku belum paham bagian ini
```

```text
bantu aku latihan tanpa langsung kasih kunci
```

```text
cek jawabanku
```

```text
ini feedback tutor kemarin
```

Kalau Project pertama terasa berguna, baru ulangi pola yang sama untuk mata kuliah lain.

## Course pack UT S1 Akuntansi Semester 2

| Nama Project | Mata kuliah | Course pack |
|---|---|---|
| `Semester 2 • Perpajakan` | EACC4104 Perpajakan | `EACC4104-perpajakan.md` |
| `Semester 2 • AKM I` | EACC4103 Akuntansi Keuangan Menengah I | `EACC4103-akm-1.md` |
| `Semester 2 • Manajemen Keuangan` | EMBS4210 Manajemen Keuangan | `EMBS4210-manajemen-keuangan.md` |
| `Semester 2 • Ekonomi Mikro` | ECON4102 Pengantar Ekonomi Mikro | `ECON4102-ekonomi-mikro.md` |
| `Semester 2 • Manajemen` | EMBS4101 Manajemen | `EMBS4101-manajemen.md` |

## Course pack UT S1 Akuntansi Semester 3

| Nama Project | Mata kuliah | Course pack |
|---|---|---|
| `Semester 3 • Lab Perpajakan` | EACC4206 Laboratorium Perpajakan | `EACC4206-laboratorium-perpajakan.md` |
| `Semester 3 • Kewirausahaan Digital` | MKDI4203 Kewirausahaan di Era Digital | `MKDI4203-kewirausahaan-era-digital.md` |
| `Semester 3 • Akuntansi Manajemen` | EMBS4326 Akuntansi Manajemen | `EMBS4326-akuntansi-manajemen.md` |
| `Semester 3 • SIA` | EACC4207 Sistem Informasi Akuntansi | `EACC4207-sistem-informasi-akuntansi.md` |
| `Semester 3 • Bahasa Inggris` | MKDI4201 Bahasa Inggris | `MKDI4201-bahasa-inggris.md` |
| `Semester 3 • AKM II` | EACC4205 Akuntansi Keuangan Menengah II | `EACC4205-akm-2.md` |
| `Semester 3 • Belajar di Era Digital` | MKDI4202 Belajar di Era Digital | `MKDI4202-belajar-era-digital.md` |

Nama Project berasal dari `project_name` pada manifest pack. Contributor tidak perlu membuat format nama sendiri.

### Catatan Semester 3 2026/2027

Semester 3 tidak dibuat dengan menyalin metadata tahun sebelumnya. Katalog pusat UT 2026/2027 dan halaman BMP aktif menunjukkan beberapa perubahan, terutama **AKM II** yang sekarang memakai bahan ajar `EACC4205` baru dan berstatus BP/BPro. Laboratorium Perpajakan juga memakai metadata current 2026/2027 dan mempunyai prasyarat EACC4104.

Karena itu, jangan memakai course pack atau metadata Semester 3 lama untuk Project 2026/2027 hanya karena nama mata kuliahnya sama.

## Memory dan pemisahan konteks

Ramu memakai satu Project per mata kuliah supaya file, riwayat, source, dan learner state tidak bercampur.

Gunakan **Project-only memory**. Pada eligible Project yang sudah ada, pengaturan memory dapat diubah melalui **Project settings → Memory**; perubahan dapat membutuhkan beberapa jam untuk berlaku. Shared Project tetap memakai Project-only memory. Jika kamu sedang berada di Project AKM II tetapi ingin membahas Lab Perpajakan, lebih baik pindah Project daripada menyimpan progres pajak ke learner state AKM II.

Jika dari suatu sesi muncul konteks belajar yang perlu dibawa ke chat berikutnya, minta Ramu membuat **Catatan Belajar Terbaru**. Bila ChatGPT menyediakan opsi untuk menyimpan hasil ke Project atau menjadikannya Project Source, catatan itu dapat disimpan ke Project. Ketika catatan baru menggantikan versi lama, hapus versi lama supaya dua state yang bertentangan tidak dipakai bersamaan.

## Mengatur file agar Project tetap bersih

- course pack Ramu dapat menjadi source tetap;
- BMP/materi kelas ditambahkan bila memang relevan;
- screenshot soal biasanya cukup dikirim pada chat yang sedang dikerjakan;
- rubrik sebaiknya ikut dikirim jika tugas memilikinya;
- file lama yang sudah tidak diperlukan dapat dihapus;
- jangan memasang dua versi course pack untuk mata kuliah yang sama sekaligus.

Batas file per Project bergantung pada produk/paket ChatGPT dan dapat berubah. Dokumentasi OpenAI yang tercatat di source registry Ramu menjadi acuan untuk perubahan produk, bukan angka yang di-hardcode permanen di course pack.

## Privasi

Ramu adalah site statis dan tidak memiliki backend untuk menerima file kuliah pribadi. File pribadi ditambahkan langsung oleh pengguna ke ChatGPT.

Pengaturan apakah percakapan boleh digunakan untuk peningkatan model berada di **Data Controls** akun ChatGPT dan bukan syarat penggunaan Ramu.

## Tentang Study Mode

Dokumentasi OpenAI saat ini menyatakan **Study Mode tidak berlaku pada Project conversations**. Ramu tidak bergantung pada Study Mode: pola bantuan belajar berasal dari Project Instructions, protocols, dan course pack, sehingga scaffolding, retrieval practice, dan tutoring behavior tetap tersedia di dalam Project tanpa Study Mode.

## Kalau UI ChatGPT berubah

ChatGPT Projects adalah produk yang dapat berubah. Karena itu panduan Ramu berpegang pada fungsi, bukan hanya posisi tombol:

- **Project Instructions** → aturan runtime Ramu;
- **Sources** → course pack dan materi yang memang perlu menjadi konteks Project;
- **Project-only memory** → pemisahan konteks antarmata kuliah.

Jika nama atau lokasi menu berubah, gunakan fungsi yang setara dan cek dokumentasi produk terbaru.
