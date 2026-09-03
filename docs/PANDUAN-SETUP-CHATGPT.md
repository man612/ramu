# Panduan Setup Ramu di ChatGPT

Panduan ini untuk pengguna yang ingin langsung memakai Ramu tanpa perlu memahami schema, eval, atau struktur repository.

Satu **pack** mewakili konteks akademik tertentu: institusi, program studi, tahun akademik, dan periode. Tidak perlu memasang seluruh pack sekaligus. Mulai dari satu mata kuliah yang benar-benar sedang dipakai.

## Pilih pack

Buka [site Ramu](https://man612.github.io/ramu/) lalu pilih pack yang sesuai.

Pack yang tersedia untuk UT S1 Akuntansi 2026/2027:

- **Semester 2** — 5 mata kuliah, 16 SKS;
- **Semester 3** — 7 mata kuliah, 20 SKS.

Nama Project memakai label periode secara penuh, misalnya:

- `Semester 2 • Perpajakan`
- `Semester 3 • AKM II`
- `Semester 3 • Bahasa Inggris`

Bentuk `S2`/`S3` dihindari pada nama yang dilihat pengguna karena mudah terbaca sebagai jenjang pendidikan. ID internal tetap boleh ringkas, misalnya `.s3` atau `semester-03/`.

## 1. Pilih satu mata kuliah

Pilih mata kuliah yang memang sedang digunakan. Tidak perlu menyiapkan seluruh semester hanya untuk mencoba workflow-nya.

## 2. Buat ChatGPT Project

1. Buka ChatGPT.
2. Pilih **New Project**.
3. Gunakan nama Project yang ditampilkan Ramu, misalnya `Semester 3 • AKM II`.
4. Pilih **Project-only memory** agar konteks Project tetap terpisah dari percakapan di luar Project.

Pada eligible Project yang sudah ada, pengaturan memory dapat diubah melalui **Project settings → Memory**. Shared Project tetap memakai Project-only memory. Nama atau posisi menu dapat berubah mengikuti versi aplikasi; yang dicari adalah fungsi yang setara.

## 3. Pasang Project Instructions

Di halaman setup pack, tekan **Salin instruksi**.

Kemudian buka:

`Project → ⋯ → Project settings → Project Instructions`

Tempel instruksi tersebut di sana.

Project Instructions adalah aturan runtime untuk cara AI menangani konteks, sumber, tugas, dan pola bantuan. Ia berbeda dari Project Source.

## 4. Tambahkan course pack

Di halaman setup:

1. pilih mata kuliah;
2. tekan **Unduh paket (.txt)**;
3. kembali ke ChatGPT Project;
4. buka **Sources** atau **Project Sources**;
5. unggah course pack yang baru diunduh.

Course pack menjadi konteks tetap untuk mata kuliah tersebut. BMP, materi kelas, screenshot soal, rubrik, atau file pribadi ditambahkan sendiri ketika memang dibutuhkan.

## 5. Mulai gunakan

Begitu satu Project siap, langsung pakai seperti chat biasa.

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

Kalau Project pertama terasa berguna, baru ulangi langkah yang sama untuk mata kuliah lain.

## Course pack Semester 2

| Nama Project | Mata kuliah | Course pack |
|---|---|---|
| `Semester 2 • Perpajakan` | EACC4104 Perpajakan | `EACC4104-perpajakan.md` |
| `Semester 2 • AKM I` | EACC4103 Akuntansi Keuangan Menengah I | `EACC4103-akm-1.md` |
| `Semester 2 • Manajemen Keuangan` | EMBS4210 Manajemen Keuangan | `EMBS4210-manajemen-keuangan.md` |
| `Semester 2 • Ekonomi Mikro` | ECON4102 Pengantar Ekonomi Mikro | `ECON4102-ekonomi-mikro.md` |
| `Semester 2 • Manajemen` | EMBS4101 Manajemen | `EMBS4101-manajemen.md` |

## Course pack Semester 3

| Nama Project | Mata kuliah | Course pack |
|---|---|---|
| `Semester 3 • Lab Perpajakan` | EACC4206 Laboratorium Perpajakan | `EACC4206-laboratorium-perpajakan.md` |
| `Semester 3 • Kewirausahaan Digital` | MKDI4203 Kewirausahaan di Era Digital | `MKDI4203-kewirausahaan-era-digital.md` |
| `Semester 3 • Akuntansi Manajemen` | EMBS4326 Akuntansi Manajemen | `EMBS4326-akuntansi-manajemen.md` |
| `Semester 3 • SIA` | EACC4207 Sistem Informasi Akuntansi | `EACC4207-sistem-informasi-akuntansi.md` |
| `Semester 3 • Bahasa Inggris` | MKDI4201 Bahasa Inggris | `MKDI4201-bahasa-inggris.md` |
| `Semester 3 • AKM II` | EACC4205 Akuntansi Keuangan Menengah II | `EACC4205-akm-2.md` |
| `Semester 3 • Belajar di Era Digital` | MKDI4202 Belajar di Era Digital | `MKDI4202-belajar-era-digital.md` |

Nama Project berasal dari `project_name` pada manifest pack, jadi formatnya tidak perlu dibuat sendiri.

### Catatan Semester 3 2026/2027

Semester 3 direview dari source 2026/2027, bukan disalin dari metadata tahun sebelumnya. Perubahan paling besar ada pada **AKM II**: bahan ajar current memakai `EACC4205`, dan mata kuliahnya sekarang berstatus BP/BPro. Laboratorium Perpajakan juga memakai metadata current 2026/2027 serta memiliki prasyarat EACC4104.

Gunakan pack yang sesuai tahun akademik aktif walaupun nama mata kuliahnya terlihat sama dengan tahun sebelumnya.

## Memory dan pemisahan konteks

Satu mata kuliah ditempatkan di satu Project supaya source, file, riwayat tugas, dan progres belajarnya tidak bercampur dengan mata kuliah lain.

Jika sesi menghasilkan konteks yang perlu dibawa ke chat berikutnya, minta **Catatan Belajar Terbaru**. Bila ChatGPT menyediakan opsi untuk menyimpannya ke Project atau Project Sources, catatan tersebut bisa dipakai sebagai state eksplisit. Hapus versi lama setelah digantikan supaya dua state yang bertentangan tidak aktif bersamaan.

## Menjaga Project tetap rapi

- course pack dapat menjadi source tetap;
- BMP dan materi kelas ditambahkan bila relevan;
- screenshot soal biasanya cukup dikirim di chat yang sedang dikerjakan;
- rubrik sebaiknya ikut dikirim jika tugas memilikinya;
- file yang sudah tidak dipakai dapat dihapus;
- hindari memasang dua versi course pack untuk mata kuliah yang sama sekaligus.

Batas file dan detail UI ChatGPT dapat berubah. Dokumentasi produk yang dicatat di source registry dipakai untuk memantau perubahan tersebut, bukan angka atau posisi tombol yang di-hardcode ke course pack.

## Privasi

Website Ramu bersifat statis. File kuliah pribadi masuk langsung ke ChatGPT Project, bukan ke server Ramu.

Pengaturan penggunaan percakapan untuk peningkatan model berada di **Data Controls** akun ChatGPT dan terpisah dari setup Ramu.

## Study Mode

Dokumentasi OpenAI yang direview saat ini menyatakan **Study Mode tidak berlaku pada Project conversations**. Workflow belajar di Ramu berasal dari Project Instructions, protocols, dan course pack, jadi Project tetap dapat memakai scaffolding dan retrieval practice tanpa Study Mode.

## Jika UI ChatGPT berubah

Fokus pada fungsinya:

- **Project Instructions** → aturan runtime;
- **Sources / Project Sources** → course pack dan materi yang perlu menjadi konteks;
- **Project-only memory** → pemisahan konteks Project.

Jika label atau posisi menu berubah, gunakan fungsi yang setara dan cek dokumentasi produk terbaru.
