# UT S1 Akuntansi — Semester 3

Pack ini untuk **Semester 3 S1 Akuntansi Universitas Terbuka tahun akademik 2026/2027**.

**Status:** source-verified  
**Terakhir diperiksa:** 3 September 2026  
**Total:** 20 SKS

## Mulai pakai

Pilih mata kuliah yang sedang digunakan. Tidak perlu menyiapkan seluruh Semester 3 sekaligus.

Nama Project:

1. `Semester 3 • Lab Perpajakan`
2. `Semester 3 • Kewirausahaan Digital`
3. `Semester 3 • Akuntansi Manajemen`
4. `Semester 3 • SIA`
5. `Semester 3 • Bahasa Inggris`
6. `Semester 3 • AKM II`
7. `Semester 3 • Belajar di Era Digital`

Ikuti [panduan setup](../../../../../docs/PANDUAN-SETUP-CHATGPT.md): buat satu Project, pasang Project Instructions, lalu unggah course pack yang sesuai sebagai Project Source.

## File pack

Project Instructions:

[PROJECT-INSTRUCTIONS.md](PROJECT-INSTRUCTIONS.md)

Course pack:

| Mata kuliah | File |
|---|---|
| Laboratorium Perpajakan | [EACC4206-laboratorium-perpajakan.md](courses/EACC4206-laboratorium-perpajakan.md) |
| Kewirausahaan di Era Digital | [MKDI4203-kewirausahaan-era-digital.md](courses/MKDI4203-kewirausahaan-era-digital.md) |
| Akuntansi Manajemen | [EMBS4326-akuntansi-manajemen.md](courses/EMBS4326-akuntansi-manajemen.md) |
| Sistem Informasi Akuntansi | [EACC4207-sistem-informasi-akuntansi.md](courses/EACC4207-sistem-informasi-akuntansi.md) |
| Bahasa Inggris | [MKDI4201-bahasa-inggris.md](courses/MKDI4201-bahasa-inggris.md) |
| Akuntansi Keuangan Menengah II | [EACC4205-akm-2.md](courses/EACC4205-akm-2.md) |
| Belajar di Era Digital | [MKDI4202-belajar-era-digital.md](courses/MKDI4202-belajar-era-digital.md) |

## Mata kuliah 2026/2027

| Kode | Mata kuliah | SKS | Ujian | Praktik/layanan |
|---|---|---:|---|---|
| EACC4206 | Laboratorium Perpajakan | 2 | II.1 | BPr · BPro |
| MKDI4203 | Kewirausahaan di Era Digital | 3 | I.1 | — |
| EMBS4326 | Akuntansi Manajemen | 3 | I.2 | T |
| EACC4207 | Sistem Informasi Akuntansi | 3 | I.3 | T |
| MKDI4201 | Bahasa Inggris | 3 | II.2 | T |
| EACC4205 | Akuntansi Keuangan Menengah II | 3 | II.3 | BP · BPro |
| MKDI4202 | Belajar di Era Digital | 3 | II.5 | WT |

Data mengikuti **Katalog Kurikulum UT 2026/2027 edisi Juli 2026**. Metadata bahan ajar dibandingkan dengan halaman BMP aktif Perpustakaan UT, sedangkan aturan praktik mengacu pada **Pedoman Sistem Penyelenggaraan UT 2026/2027**.

## Perubahan dibanding data lama

Semester 3 direview ulang dari source current karena beberapa metadata sudah berubah dari tahun sebelumnya:

- **AKM II** sekarang memakai `EACC4205 Akuntansi Keuangan Menengah II`, BMP Edisi 1 tahun 2026, dan berstatus **BP/BPro**. `EKMA4313 Edisi 3` tetap berguna sebagai konteks historis, tetapi bukan current pack truth.
- **Laboratorium Perpajakan** memakai slot ujian `II.1`, BPr/BPro, dengan prasyarat EACC4104 Perpajakan.
- **Bahasa Inggris** mencantumkan layanan `T` pada row S1 Akuntansi current.
- **Belajar di Era Digital** mencantumkan `WT`.

Halaman regional atau arsip dapat tertinggal dari katalog pusat. Untuk struktur dan metadata kurikulum, source pusat current tetap menjadi rujukan utama.

## Mata kuliah praktik

### EACC4206 — Laboratorium Perpajakan

Fokusnya aplikasi perpajakan. Pada pola BPro, PRATON wajib; pedoman 2026/2027 mencatat minimal 5 dari 8 tugas, kontribusi PRATON 60%, dan UAS 40%.

Kasus dapat berkesinambungan. Bila tugas lanjutan membutuhkan state sebelumnya, course pack meminta data yang benar daripada mengisi opening state dengan asumsi.

Perpajakan juga sensitif terhadap waktu, jadi konteks **BMP/soal** dipisahkan dari **aturan pajak terkini** ketika keduanya berbeda.

### EACC4205 — AKM II

AKM II memakai BMP EACC4205 yang baru dan masuk workflow BP/BPro. Course pack memberi perhatian pada jurnal, pengukuran, penyajian/pengungkapan, perhitungan, PSAK, dan konsistensi state kasus PRATON.

AKM II juga termasuk mata kuliah prasyarat TAPS.

## Prasyarat TAPS dari Semester 3

Katalog UT 2026/2027 mencantumkan:

- EACC4205 Akuntansi Keuangan Menengah II;
- EMBS4326 Akuntansi Manajemen;
- EACC4207 Sistem Informasi Akuntansi.

Informasi ini memberi konteks pentingnya mata kuliah pada kurikulum current. Jika katalog berubah, source terbaru tetap menjadi acuan.

## Source registry dan eval

[source-registry.json](source-registry.json) menyimpan halaman BMP aktif dan claim yang spesifik pada Semester 3. Source tingkat institusi tetap berada di [`../../../source-registry.json`](../../../source-registry.json).

Regression E17–E24 mencakup antara lain:

- BMP/soal pajak vs aturan terkini;
- metadata lama vs current AKM II;
- state kasus PRATON lanjutan;
- requirement/control sebelum flowchart SIA;
- relevant cost pada Akuntansi Manajemen;
- hipotesis vs evidence pasar pada Kewirausahaan Digital;
- tutoring sebelum full rewrite pada Bahasa Inggris;
- ketidakpastian isi kebijakan GenAI UT pada Belajar di Era Digital.

## Kode layanan UT

- `T` — layanan TTM/Tuweb untuk SIPAS Semi;
- `WT` — wajib Tuton untuk SIPAS Penuh/Plus;
- `BP` — mata kuliah berpraktik;
- `BPr` — mata kuliah berpraktikum;
- `BPro` — mata kuliah berpraktik/berpraktikum dengan bimbingan online wajib.

Pack ini dipelihara sebagai bagian dari proyek independen dan bukan layanan resmi Universitas Terbuka. Materi kuliah berhak cipta tidak disalin ke repository.
