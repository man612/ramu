<p align="center">
  <img src=".github/assets/hero-light.svg#gh-light-mode-only" alt="Ramu — ChatGPT Projects yang disiapkan untuk kuliah" width="100%">
  <img src=".github/assets/hero-dark.svg#gh-dark-mode-only" alt="Ramu — ChatGPT Projects yang disiapkan untuk kuliah" width="100%">
</p>

<p align="center">
  <a href="https://man612.github.io/ramu/"><strong>Buka Ramu</strong></a>
  ·
  <a href="https://man612.github.io/ramu/setup.html">Panduan setup Semester 2</a>
  ·
  <a href="docs/RISET-DAN-DASAR-DESAIN.md">Dasar riset</a>
</p>

<p align="center">
  <img alt="GitHub Pages" src="https://img.shields.io/github/actions/workflow/status/man612/ramu/pages.yml?label=pages&style=flat-square">
  <img alt="Paket pertama" src="https://img.shields.io/badge/paket-UT%20S1%20Akuntansi-405A46?style=flat-square">
  <img alt="Semester" src="https://img.shields.io/badge/semester-2%20%C2%B7%202026%2F2027-BB8C51?style=flat-square">
  <img alt="Status" src="https://img.shields.io/badge/status-sumber%20terverifikasi-745B86?style=flat-square">
</p>

---

## Ramu itu apa?

Ramu adalah **paket konfigurasi untuk ChatGPT Projects** agar setiap mata kuliah memiliki ruang, konteks, sumber, dan cara pemeriksaan yang jelas.

Ramu bukan aplikasi pengganti ChatGPT dan bukan kumpulan jawaban tugas. Anggap saja Ramu sebagai **meja belajar yang sudah disiapkan**. Setelah setup selesai, kamu tinggal membuka Project mata kuliah yang sesuai, mengirim soal atau materi, lalu menjelaskan kebutuhanmu dengan bahasa biasa.

<table>
<tr>
<td width="50%" valign="top">
<h3>Tanpa Ramu</h3>
<p>Setiap membuka chat baru, kamu mungkin perlu menjelaskan ulang:</p>
<ul>
<li>mata kuliah yang sedang dibahas;</li>
<li>materi yang digunakan;</li>
<li>format dan aturan tugas;</li>
<li>sumber yang perlu diprioritaskan;</li>
<li>cara memeriksa hitungan atau jawaban.</li>
</ul>
</td>
<td width="50%" valign="top">
<h3>Dengan Ramu</h3>
<p>Buka Project mata kuliahnya, lalu kamu bisa langsung menulis:</p>
<p><code>aku belum paham bagian ini</code></p>
<p><code>cek jawabanku</code></p>
<p><code>bantu aku kerjakan soal ini pelan-pelan</code></p>
<p><code>ini feedback tutor kemarin</code></p>
</td>
</tr>
</table>

## Cara pakainya

<p align="center">
  <img src=".github/assets/setup-flow.svg" alt="Alur penggunaan Ramu dari setup sampai pemakaian sehari-hari" width="100%">
</p>

Paket pertama Ramu disiapkan untuk **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**. Di ChatGPT, kamu membuat lima Project terpisah:

| Project | Mata kuliah | SKS |
|---|---|---:|
| `S2 • Perpajakan` | EACC4104 Perpajakan | 3 |
| `S2 • AKM I` | EACC4103 Akuntansi Keuangan Menengah I | 3 |
| `S2 • Manajemen Keuangan` | EMBS4210 Manajemen Keuangan | 3 |
| `S2 • Ekonomi Mikro` | ECON4102 Pengantar Ekonomi Mikro | 3 |
| `S2 • Manajemen` | EMBS4101 Manajemen | 4 |

> **Kalau ingin langsung menggunakan Ramu:** buka [panduan setup interaktif](https://man612.github.io/ramu/setup.html). Kamu tidak perlu memahami struktur repo ini.

## Yang dijaga Ramu

Ramu menyiapkan beberapa aturan dasar di belakang layar agar penggunaan tiap Project tetap rapi. Pengguna tidak perlu mengatur bagian ini satu per satu.

- **Sumber yang sesuai** — sumber dipilih berdasarkan jenis pertanyaan dan masa berlakunya.
- **Aturan tugas** — rubrik, instruksi tutor, dan ketentuan kampus diprioritaskan.
- **Konteks per mata kuliah** — satu mata kuliah tetap berada di Project-nya sendiri.
- **Materi utama** — BMP, bahan tutor, soal, dan materi kelas tetap menjadi dasar belajar.
- **Pemeriksaan akhir** — isi, hitungan, sumber, dan format diperiksa sebelum jawaban dianggap selesai.

Aturan tersebut sudah diterjemahkan ke dalam **Project Instructions** dan **paket mata kuliah (course pack)**.

## Yang sudah disiapkan

- **Project Instructions** — aturan dasar yang digunakan di semua Project.
- **Paket mata kuliah** — konteks, sumber, alur kerja, dan pemeriksaan yang disesuaikan dengan mata kuliah.
- **Panduan Android** — langkah setup dari aplikasi ChatGPT.
- **Aturan sumber dan kebaruan informasi** — penting untuk informasi yang dapat berubah, seperti perpajakan.
- **Eval** — skenario pengujian untuk memeriksa perilaku paket, bukan sekadar membaca prompt.
- **GitHub Pages** — tampilan yang lebih mudah digunakan tanpa harus memahami GitHub.

## Kenapa satu mata kuliah dibuat sebagai satu Project?

Satu Project untuk seluruh semester memang terlihat lebih sederhana pada awalnya, tetapi lama-kelamaan file, percakapan, dan aturan lima mata kuliah akan bercampur. Ramu memisahkannya agar:

- file setiap mata kuliah tetap terpisah;
- riwayat percakapan lebih mudah dicari;
- instruksi satu mata kuliah tidak tercampur dengan mata kuliah lain;
- feedback tutor tersimpan di tempat yang tepat;
- penggunaan sehari-hari tetap sederhana.

Penjelasan lengkap tentang keputusan ini ada di [`docs/RISET-DAN-DASAR-DESAIN.md`](docs/RISET-DAN-DASAR-DESAIN.md).

## Struktur repo

```text
ramu/
├── core/       prinsip dasar Ramu
├── docs/       panduan, riset, dan validasi
├── evals/      skenario pengujian
├── packs/      paket kampus / program studi / semester
├── site/       GitHub Pages
└── .github/    workflow dan aset README
```

## Status paket UT Semester 2

**Sumber terverifikasi** berarti data utama paket sudah dicocokkan dengan sumber resmi yang berlaku. Status ini berbeda dari **Terverifikasi penuh**, yang baru diberikan setelah skenario eval perilaku paket selesai diuji.

Acuan utama saat ini:

- Katalog Kurikulum UT 2026/2027 edisi Juli 2026.
- Pedoman Sistem Penyelenggaraan UT 2026/2027.

Ramu tidak menyertakan salinan BMP atau materi kuliah berhak cipta. Materi yang memang dimiliki atau dapat diakses mahasiswa ditambahkan sendiri ke Project saat diperlukan.

---

<p align="center">
  <b>Mulai dari sini → <a href="https://man612.github.io/ramu/setup.html">Panduan setup UT S1 Akuntansi Semester 2</a></b>
</p>

<p align="center">
  <sub>Proyek independen. Bukan layanan resmi Universitas Terbuka maupun OpenAI.</sub>
</p>
