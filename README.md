# Ramu

**Ramu** adalah kerangka konfigurasi workspace AI untuk membantu proses kuliah tetap rapi, kontekstual, dan bisa dipakai berulang sepanjang semester.

Ramu tidak membuat AI baru dan tidak menggantikan LMS kampus. Ramu menyiapkan **Project Instructions**, **course pack**, aturan sumber, alur belajar, dan pemeriksaan hasil supaya ChatGPT Projects tidak selalu mulai dari nol setiap kali mahasiswa membuka tugas baru.

> Dukungan pertama: **Universitas Terbuka · S1 Akuntansi · 2026/2027 · Semester 2**

[Mulai dari paket Semester 2](packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/README.md) · [Panduan setup ChatGPT](docs/PANDUAN-SETUP-CHATGPT.md) · [Dasar riset & keputusan desain](docs/RISET-DAN-DASAR-DESAIN.md)

## Cara kerjanya

Satu semester dipilih sekali dari Ramu, lalu setiap mata kuliah dibuat sebagai **Project terpisah di ChatGPT**. Pemisahan ini menjaga konteks tetap fokus dan memberi ruang file sendiri untuk tiap mata kuliah.

```text
Ramu
└── Universitas Terbuka
    └── S1 Akuntansi
        └── Semester 2
            ├── S2 • Perpajakan
            ├── S2 • AKM I
            ├── S2 • Manajemen Keuangan
            ├── S2 • Ekonomi Mikro
            └── S2 • Manajemen
```

Di awal semester, mahasiswa cukup menyalin satu Project Instructions yang sama dan memasukkan satu course pack untuk masing-masing Project. Setelah itu penggunaan harian kembali sederhana: buka Project mata kuliah, kirim soal atau materi, lalu bicara seperti biasa.

## Lima prinsip dasar

Ramu dirancang dengan lima hal yang selalu dipisahkan agar konteks tidak berantakan:

1. **Referensi** — menentukan sumber mana yang berwenang untuk pertanyaan tertentu dan kapan informasi terbaru perlu diverifikasi.
2. **Instruksi** — membedakan aturan umum, aturan kampus, aturan mata kuliah, rubrik, dan instruksi tugas yang lebih spesifik.
3. **Zona Konteks** — menjaga satu mata kuliah berada di ruangnya sendiri dan mencegah konteks semester berubah menjadi satu tumpukan besar.
4. **Materi** — mengutamakan bahan kuliah yang memang sedang dipakai, tanpa menyalin bahan berhak cipta ke repo publik.
5. **Asesmen** — memeriksa hasil terhadap soal, rubrik, hitungan, sumber, dan feedback sebelumnya sebelum dianggap selesai.

## Kenapa memakai ChatGPT Projects?

Projects menyatukan chat, file, dan Project Instructions dalam satu ruang. Ramu merekomendasikan **project-only memory** supaya konteks satu mata kuliah tidak mengambil chat dari luar Project. Detail pengaturan dan batasannya dijelaskan di [panduan setup](docs/PANDUAN-SETUP-CHATGPT.md).

Ramu tidak mengandalkan memory sebagai satu-satunya tempat menyimpan hal penting. Feedback tutor, aturan yang berubah, dan ringkasan keputusan penting sebaiknya tetap disimpan sebagai sumber eksplisit karena Project memory tidak menyediakan daftar memory yang dapat diperiksa satu per satu.

## Status paket pertama

| Mata kuliah | Kode | SKS | Status |
|---|---|---:|---|
| Perpajakan | EACC4104 | 3 | Sumber terverifikasi |
| Akuntansi Keuangan Menengah I | EACC4103 | 3 | Sumber terverifikasi |
| Manajemen Keuangan | EMBS4210 | 3 | Sumber terverifikasi |
| Pengantar Ekonomi Mikro | ECON4102 | 3 | Sumber terverifikasi |
| Manajemen | EMBS4101 | 4 | Sumber terverifikasi |

Data paket mengacu pada **Katalog Kurikulum UT 2026/2027 edisi Juli 2026** dan **Pedoman Sistem Penyelenggaraan UT 2026/2027**. Detail sumber dan cara menangani perbedaan antarhalaman UT ada di [Sumber & Validasi](docs/SUMBER-DAN-VALIDASI.md).

## Batasan

- Ramu bukan layanan resmi Universitas Terbuka maupun OpenAI.
- Course pack tidak menggantikan BMP, Tuton, PRATON, RPS/silabus, rubrik, atau arahan tutor.
- Aturan tugas dan kebijakan penggunaan AI dari kampus/tutor selalu harus diperhatikan.
- Informasi yang dapat berubah, terutama regulasi dan perpajakan, harus diverifikasi terhadap sumber resmi terbaru.
- Materi kuliah berhak cipta tidak disertakan ke repo publik.

## Struktur repo

```text
ramu/
├── core/           # prinsip dasar lintas kampus/mata kuliah
├── docs/           # panduan, riset, validasi, dan keputusan desain
├── evals/          # skenario uji perilaku pack
├── packs/          # konfigurasi siap pakai per institusi/program/semester
├── site/           # GitHub Pages, mobile-first
└── .github/        # workflow deployment
```

Implementasi awal memang difokuskan pada UT S1 Akuntansi Semester 2. Struktur `core` dan format pack dibuat supaya kelak dapat diperluas tanpa mencampur aturan tiap institusi.
