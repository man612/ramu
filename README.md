<p align="center">
  <img src=".github/assets/hero-light.svg#gh-light-mode-only" alt="Ramu — ChatGPT Projects yang disiapkan untuk kuliah" width="100%">
  <img src=".github/assets/hero-dark.svg#gh-dark-mode-only" alt="Ramu — ChatGPT Projects yang disiapkan untuk kuliah" width="100%">
</p>

<p align="center">
  <a href="https://man612.github.io/ramu/"><strong>Buka Ramu</strong></a>
  ·
  <a href="https://man612.github.io/ramu/setup.html">Panduan setup Semester 2</a>
  ·
  <a href="docs/LANDASAN-PEMBELAJARAN.md">Landasan pembelajaran</a>
</p>

<p align="center">
  <img alt="GitHub Pages" src="https://img.shields.io/github/actions/workflow/status/man612/ramu/pages.yml?label=pages&style=flat-square">
  <img alt="Validasi Ramu" src="https://img.shields.io/github/actions/workflow/status/man612/ramu/validate.yml?label=contracts&style=flat-square">
  <img alt="Paket pertama" src="https://img.shields.io/badge/paket-UT%20S1%20Akuntansi-405A46?style=flat-square">
  <img alt="Semester" src="https://img.shields.io/badge/semester-2%20%C2%B7%202026%2F2027-BB8C51?style=flat-square">
  <img alt="Status" src="https://img.shields.io/badge/status-sumber%20terverifikasi-745B86?style=flat-square">
</p>

---

## Ramu itu apa?

Ramu adalah **paket konfigurasi untuk ChatGPT Projects** agar setiap mata kuliah memiliki ruang, konteks, sumber, cara belajar, dan cara pemeriksaan yang jelas.

Ramu bukan aplikasi pengganti ChatGPT dan bukan kumpulan jawaban tugas. Anggap saja Ramu sebagai **meja belajar yang sudah disiapkan**. Setelah setup selesai, kamu tinggal membuka Project mata kuliah yang sesuai, mengirim soal atau materi, lalu menjelaskan kebutuhanmu dengan bahasa biasa.

<table>
<tr>
<td width="100%">
<p align="center"><strong>Fondasi Ramu</strong><br><sub>Lima hal yang selalu dijaga di setiap Project.</sub></p>
<hr>
<h3>Referensi</h3>
<p>Memilih sumber yang sesuai dengan pertanyaan dan memastikan informasi yang digunakan masih berlaku.</p>
<h3>Instruksi</h3>
<p>Mengikuti aturan tugas, rubrik, arahan tutor, dan ketentuan kampus sebelum menyusun jawaban.</p>
<h3>Zona Konteks</h3>
<p>Menjaga setiap mata kuliah tetap berada di Project-nya sendiri agar materi dan percakapan tidak bercampur.</p>
<h3>Materi</h3>
<p>Menggunakan BMP, bahan tutor, soal, dan materi kelas sebagai dasar belajar saat tersedia.</p>
<h3>Asesmen</h3>
<p>Memeriksa kembali isi, hitungan, sumber, dan format sebelum jawaban dianggap selesai.</p>
</td>
</tr>
</table>

Kelima bagian ini diterapkan di runtime melalui **Project Instructions** dan **course pack** mata kuliah. Folder protokol, state, source registry, dan eval di repo menjadi lapisan desain serta pemeriksaan di belakangnya; pengguna tidak perlu mengunggah semuanya ke ChatGPT.

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

Untuk setiap Project, yang dipasang hanya **Project Instructions yang sama + satu course pack mata kuliah**. Project Instructions ditempel lewat **Project settings**, sedangkan course pack ditambahkan lewat **Sources** sebagai file. Materi, rubrik, screenshot, atau PDF tugas ditambahkan saat memang diperlukan.

> **Kalau ingin langsung menggunakan Ramu:** buka [panduan setup interaktif](https://man612.github.io/ramu/setup.html). Kamu tidak perlu memahami struktur repo ini.

## Yang sudah disiapkan

- **Project Instructions** — aturan runtime yang digunakan di semua Project.
- **Course pack** — konteks, sumber, alur kerja, verifier, versi paket, dan tanggal verifikasi yang disesuaikan dengan mata kuliah.
- **Protokol belajar** — spesifikasi desain untuk belajar, tugas, review, dan latihan ujian; perilaku intinya sudah diringkas ke Project Instructions.
- **State belajar** — template desain untuk learner state, review queue, misconception log, dan mastery map. Di runtime, catatan penting dapat diringkas menjadi **Catatan Belajar Terbaru** lalu disimpan sebagai Project Source jika fitur tersebut tersedia.
- **Source registry** — sumber memiliki fungsi, otoritas, tanggal verifikasi, interval review, dan status.
- **Eval contracts** — guardrail penting diuji agar tidak hilang saat prompt/course pack diedit.
- **Behavior evals** — E01–E12 dapat dijalankan ke model dan dinilai oleh model judge sebagai pengujian opsional.
- **Source freshness watch** — GitHub Actions mengecek kapan sumber aktif perlu diverifikasi ulang.
- **Panduan Android** — setup dari HP dengan jalur utama unduh course pack `.txt` lalu unggah melalui `Sources → Add source → Upload files`; `Add from library` menjadi alternatif bila file sudah tersimpan.
- **GitHub Pages** — tampilan yang lebih mudah digunakan tanpa harus memahami GitHub.

## Belajarnya tidak cuma “tanya → dapat jawaban”

Untuk sesi belajar, Ramu memakai bantuan bertahap: mulai dari penjelasan/petunjuk yang cukup, memberi kesempatan mencoba, lalu mengurangi bantuan ketika mahasiswa mulai mampu. Untuk latihan ujian, pertanyaan diberikan sebelum kunci dan topik yang masih rapuh dapat masuk ke review queue.

Desain ini sengaja dibuat agar AI membantu proses belajar tanpa otomatis menjadi mesin jawaban. Dasar riset dan batas interpretasinya ada di [`docs/LANDASAN-PEMBELAJARAN.md`](docs/LANDASAN-PEMBELAJARAN.md).

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
├── core/        prinsip dasar Ramu
├── protocols/   spesifikasi perilaku belajar, tugas, review, dan latihan
├── learning/    template desain state belajar
├── packs/       paket kampus / program studi / semester
├── sources/     registry sumber dan kebijakan freshness
├── evals/       contract + behavior eval
├── schemas/     kontrak data terstruktur
├── scripts/     validator, freshness check, dan behavior runner
├── docs/        panduan, riset, dan validasi
├── site/        GitHub Pages
└── .github/     workflow validasi, behavior eval, source watch, Pages, dan aset
```

## Yang diuji otomatis

`python scripts/validate_repo.py` dan `python scripts/run_behavior_evals.py --dry-run` memeriksa antara lain:

- total SKS dan file mata kuliah pada manifest;
- `pack_version` serta metadata verifikasi pada setiap course pack;
- struktur source registry;
- ID eval yang unik;
- keberadaan learner-state templates;
- keberadaan format runtime **Catatan Belajar Terbaru**;
- contract marker pada Project Instructions/protokol/course pack;
- seluruh E01–E12 memiliki skenario behavior dan context file yang valid.

Contract test ini **bukan bukti bahwa model pasti selalu berperilaku benar**. Tujuannya mencegah regression sederhana, misalnya aturan “jangan mengarang DOI”, “jangan menebak screenshot”, atau “bedakan modul dengan aturan terbaru” terhapus tanpa sengaja.

## Behavior eval nyata

Workflow **Behavior Evals** bersifat opsional. Ia dapat dijalankan manual dari GitHub Actions jika repository secret `OPENAI_API_KEY` tersedia. Model kandidat dan model judge bisa dipilih secara terpisah, case dapat dibatasi misalnya `E01,E05,E08`, dan pass rate minimum dapat diubah tanpa mengubah dataset.

Setiap run menghasilkan ringkasan `PASS/FAIL`, skor per case, alasan judge, penggunaan token, serta artifact JSON yang menyimpan respons kandidat untuk audit. Workflow ini sengaja tidak berjalan pada setiap push agar penggunaan API tetap terkendali dan hasil probabilistik tidak membuat CI rutin menjadi noisy.

Panduan lengkap ada di [`evals/behavior/README.md`](evals/behavior/README.md).

## Status paket UT Semester 2

**Sumber terverifikasi** berarti data utama paket sudah dicocokkan dengan sumber resmi yang berlaku. Status ini berbeda dari **Terverifikasi penuh**, yang baru diberikan setelah skenario eval perilaku paket selesai diuji dan hasilnya direview.

Acuan utama saat ini:

- Katalog Kurikulum UT 2026/2027 edisi Juli 2026.
- Pedoman Sistem Penyelenggaraan UT 2026/2027.

Registry lengkap dan tanggal review ada di [`sources/registry.json`](sources/registry.json).

Ramu tidak menyertakan salinan BMP atau materi kuliah berhak cipta. Materi yang memang dimiliki atau dapat diakses mahasiswa ditambahkan sendiri ke Project saat diperlukan.

---

<p align="center">
  <b>Mulai dari sini → <a href="https://man612.github.io/ramu/setup.html">Panduan setup UT S1 Akuntansi Semester 2</a></b>
</p>

<p align="center">
  <sub>Proyek independen. Bukan layanan resmi Universitas Terbuka maupun OpenAI.</sub>
</p>
