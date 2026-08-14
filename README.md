# Ramu

**Ramu membantu menyiapkan ChatGPT Projects untuk kuliah supaya tiap mata kuliah punya konteks, sumber, dan cara kerja yang lebih rapi.**

Implementasi pertama dibuat untuk **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**.

> Awamnya: di awal semester kamu menyiapkan satu Project ChatGPT untuk tiap mata kuliah. Setelah itu, setiap ada soal, materi, jawaban, atau feedback tutor, tinggal buka Project yang sesuai lalu kirim seperti biasa.

[Mulai dari Semester 2](packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/README.md) · [Panduan setup dari HP](docs/PANDUAN-SETUP-CHATGPT.md) · [Dasar riset](docs/RISET-DAN-DASAR-DESAIN.md)

## Kalau kamu cuma mau pakai

Tidak perlu ngerti struktur repo ini.

Untuk UT S1 Akuntansi Semester 2, alurnya:

1. siapkan **5 Project** di ChatGPT;
2. tempel **Project Instructions** yang sama ke masing-masing Project;
3. masukkan **1 course pack** sesuai mata kuliahnya;
4. selesai.

Setelah itu penggunaan sehari-hari cukup seperti ini:

```text
Buka ChatGPT
→ pilih Project mata kuliah
→ buat chat baru
→ kirim soal / materi / jawaban
→ bilang kebutuhanmu dengan bahasa biasa
```

Contoh:

- `aku ga paham bagian ini`
- `bantu tugas ini`
- `cek jawabanku`
- `ini feedback tutor kemarin`

## Project yang dibuat untuk Semester 2

| Project | Mata kuliah | SKS |
|---|---|---:|
| `S2 • Perpajakan` | Perpajakan | 3 |
| `S2 • AKM I` | Akuntansi Keuangan Menengah I | 3 |
| `S2 • Manajemen Keuangan` | Manajemen Keuangan | 3 |
| `S2 • Ekonomi Mikro` | Pengantar Ekonomi Mikro | 3 |
| `S2 • Manajemen` | Manajemen | 4 |

Kenapa dipisah? Supaya file, riwayat tugas, aturan sumber, dan konteks AKM tidak bercampur dengan Perpajakan atau mata kuliah lain.

## Lima fondasi Ramu

Ramu memakai lima hal yang selalu dijaga terpisah:

### R — Referensi
Menentukan sumber mana yang tepat untuk pertanyaan tertentu. Soal dan rubrik menentukan apa yang harus dikerjakan; modul/BMP membantu memahami materi; aturan kampus dicek dari sumber kampus; informasi yang berubah seperti pajak harus dicek ke sumber resmi terbaru.

### I — Instruksi
AI tidak langsung menjawab dari judul soal. Arahan tutor, rubrik, batas kata, format, dan ketentuan tugas dibaca lebih dulu.

### Z — Zona Konteks
Satu mata kuliah dibuat sebagai satu Project supaya percakapan dan file tidak bercampur dengan mata kuliah lain.

### M — Materi
Course pack tidak menggantikan BMP atau materi kelas. Mahasiswa tetap memasukkan modul, screenshot, PDF, soal, atau materi tutor yang memang sedang dipakai.

### A — Asesmen
Sebelum dianggap selesai, hasil dicek lagi: semua pertanyaan terjawab, hitungan masuk akal, sumber benar, dan format sesuai instruksi.

## Ramu bukan apa

- bukan aplikasi kuliah baru;
- bukan LMS pengganti UT;
- bukan kumpulan jawaban tugas;
- bukan tempat menyimpan salinan BMP berhak cipta;
- bukan jaminan bahwa AI selalu benar;
- bukan layanan resmi Universitas Terbuka atau OpenAI.

## Paket pertama

Paket **UT S1 Akuntansi Semester 2 2026/2027** saat ini berstatus **Sumber terverifikasi**. Artinya data utama sudah diperiksa terhadap sumber resmi yang relevan, tetapi paket belum diberi status “Terverifikasi” penuh sampai eval perilakunya selesai dijalankan.

Acuan utama saat ini:

- Katalog Kurikulum UT 2026/2027 edisi Juli 2026;
- Pedoman Sistem Penyelenggaraan UT 2026/2027.

Lihat [Sumber dan Validasi](docs/SUMBER-DAN-VALIDASI.md) untuk detail sumber dan cara Ramu menangani perbedaan informasi antarhalaman resmi.

## Struktur repo

Bagian ini untuk yang ingin melihat cara Ramu disusun.

```text
ramu/
├── core/           # Referensi, Instruksi, Zona Konteks, Materi, Asesmen
├── docs/           # panduan, riset, dan validasi sumber
├── evals/          # skenario uji perilaku pack
├── packs/          # paket siap pakai per institusi/program/semester
├── site/           # halaman GitHub Pages
└── .github/        # workflow deployment
```

Implementasi awal sengaja fokus dulu ke UT S1 Akuntansi Semester 2. Fondasinya dibuat cukup umum supaya kelak dapat diperluas tanpa mencampur aturan dari kampus atau mata kuliah yang berbeda.
