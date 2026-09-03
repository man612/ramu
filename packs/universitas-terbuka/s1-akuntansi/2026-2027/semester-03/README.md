# UT S1 Akuntansi — Semester 3

Paket ini disiapkan untuk **Semester 3 S1 Akuntansi Universitas Terbuka tahun akademik 2026/2027**.

**Status:** Sumber terverifikasi  
**Terakhir diperiksa:** 3 September 2026  
**Total:** 20 SKS

## Kalau ingin langsung menggunakan Ramu

Di ChatGPT, buat Project sesuai mata kuliah yang sedang dipakai. Tidak perlu menyiapkan semuanya sekaligus.

Nama Project Semester 3:

1. `Semester 3 • Lab Perpajakan`
2. `Semester 3 • Kewirausahaan Digital`
3. `Semester 3 • Akuntansi Manajemen`
4. `Semester 3 • SIA`
5. `Semester 3 • Bahasa Inggris`
6. `Semester 3 • AKM II`
7. `Semester 3 • Belajar di Era Digital`

Ikuti [panduan setup Ramu](../../../../../docs/PANDUAN-SETUP-CHATGPT.md): buat Project, pasang Project Instructions, lalu unggah **satu** course pack yang sesuai sebagai Project Source.

## File yang digunakan

**Project Instructions — digunakan pada semua Project Semester 3**  
[PROJECT-INSTRUCTIONS.md](PROJECT-INSTRUCTIONS.md)

| Mata kuliah | Course pack |
|---|---|
| Laboratorium Perpajakan | [EACC4206-laboratorium-perpajakan.md](courses/EACC4206-laboratorium-perpajakan.md) |
| Kewirausahaan di Era Digital | [MKDI4203-kewirausahaan-era-digital.md](courses/MKDI4203-kewirausahaan-era-digital.md) |
| Akuntansi Manajemen | [EMBS4326-akuntansi-manajemen.md](courses/EMBS4326-akuntansi-manajemen.md) |
| Sistem Informasi Akuntansi | [EACC4207-sistem-informasi-akuntansi.md](courses/EACC4207-sistem-informasi-akuntansi.md) |
| Bahasa Inggris | [MKDI4201-bahasa-inggris.md](courses/MKDI4201-bahasa-inggris.md) |
| Akuntansi Keuangan Menengah II | [EACC4205-akm-2.md](courses/EACC4205-akm-2.md) |
| Belajar di Era Digital | [MKDI4202-belajar-era-digital.md](courses/MKDI4202-belajar-era-digital.md) |

## Mata kuliah Semester 3 — current 2026/2027

| Kode | Mata kuliah | SKS | Ujian | Praktik/layanan |
|---|---|---:|---|---|
| EACC4206 | Laboratorium Perpajakan | 2 | II.1 | BPr · BPro |
| MKDI4203 | Kewirausahaan di Era Digital | 3 | I.1 | — |
| EMBS4326 | Akuntansi Manajemen | 3 | I.2 | T |
| EACC4207 | Sistem Informasi Akuntansi | 3 | I.3 | T |
| MKDI4201 | Bahasa Inggris | 3 | II.2 | T |
| EACC4205 | Akuntansi Keuangan Menengah II | 3 | II.3 | BP · BPro |
| MKDI4202 | Belajar di Era Digital | 3 | II.5 | WT |

Data mengikuti **Katalog Kurikulum UT 2026/2027 edisi Juli 2026**. Metadata course material juga dibandingkan dengan halaman BMP aktif Perpustakaan UT dan aturan praktik dibandingkan dengan **Pedoman Sistem Penyelenggaraan UT 2026/2027**.

## Yang berubah dibanding data Semester 3 sebelumnya

Jangan menyalin metadata Semester 3 tahun lalu ke pack ini. Review 3 September 2026 menemukan beberapa perubahan yang memengaruhi workflow Ramu:

- **AKM II berubah besar:** current 2026/2027 memakai bahan ajar `EACC4205 Akuntansi Keuangan Menengah II`, BMP Edisi 1 tahun 2026, dan sekarang ditandai **BP/BPro**. Metadata lama `EKMA4313 Edisi 3` adalah konteks historis, bukan current pack truth.
- **Laboratorium Perpajakan:** current slot ujian `II.1`, tetap BPr/BPro, dan mempunyai prasyarat EACC4104 Perpajakan.
- **Bahasa Inggris:** current row S1 Akuntansi mencantumkan layanan `T`.
- **Belajar di Era Digital:** current row mencantumkan `WT`.
- halaman regional/arsip dapat tertinggal dari katalog pusat; source registry Ramu karena itu tetap menjadikan katalog pusat sebagai kanonik untuk struktur dan metadata kurikulum.

## Dua mata kuliah praktik Semester 3

### EACC4206 — Laboratorium Perpajakan

Mata kuliah ini menekankan aplikasi perpajakan. Untuk BPro, PRATON wajib; katalog/pedoman 2026/2027 mencatat minimal 5 dari 8 tugas, kontribusi PRATON 60%, dan UAS 40%. Kasus dapat berkesinambungan, sehingga course pack tidak boleh mengarang state tugas sebelumnya.

Karena perpajakan sensitif waktu, Ramu juga memisahkan konteks **BMP/soal** dari **aturan pajak terkini**.

### EACC4205 — AKM II

AKM II sekarang menggunakan BMP EACC4205 yang baru dan masuk workflow BP/BPro. Course pack menekankan jurnal, pengukuran, penyajian/pengungkapan, perhitungan, PSAK, dan konsistensi kasus PRATON.

AKM II juga termasuk mata kuliah prasyarat TAPS.

## Mata kuliah Semester 3 yang menjadi prasyarat TAPS

Katalog UT 2026/2027 mencantumkan tiga mata kuliah Semester 3 dalam daftar prasyarat TAPS S1 Akuntansi:

- EACC4205 Akuntansi Keuangan Menengah II;
- EMBS4326 Akuntansi Manajemen;
- EACC4207 Sistem Informasi Akuntansi.

Metadata ini dipakai untuk memberi konteks pentingnya mata kuliah, bukan untuk mengubah syarat kelulusan secara otomatis jika katalog UT di masa depan berubah.

## Source registry dan eval

Semester 3 memiliki [source-registry.json](source-registry.json) sendiri untuk halaman BMP aktif dan claim yang memang spesifik pada pack ini. Source institusi tetap berada di [`../../../source-registry.json`](../../../source-registry.json).

Regression suite Semester 3 menambahkan E17–E24 untuk menguji antara lain:

- Lab Perpajakan: konteks soal/BMP vs aturan terkini;
- AKM II: metadata lama vs current 2026/2027;
- dependency state pada kasus PRATON lanjutan;
- SIA: requirement/control sebelum flowchart;
- Akuntansi Manajemen: relevant cost untuk keputusan;
- Kewirausahaan Digital: hipotesis vs evidence pasar;
- Bahasa Inggris: tutoring sebelum rewrite penuh;
- Belajar di Era Digital: tidak mengarang isi kebijakan GenAI UT.

## Keterangan teknis UT

- `T` — layanan TTM/Tuweb untuk SIPAS Semi;
- `WT` — wajib Tuton untuk SIPAS Penuh/Plus;
- `BP` — mata kuliah berpraktik;
- `BPr` — mata kuliah berpraktikum;
- `BPro` — mata kuliah berpraktik/berpraktikum dengan bimbingan online wajib.

Ramu adalah proyek independen dan bukan layanan resmi Universitas Terbuka. Materi kuliah berhak cipta tidak disalin ke repository.
