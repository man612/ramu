# Ramu v0.4.0-beta — Semester 1, Adaptive Learning & Source Integrity

**Tanggal kandidat release:** 20 Oktober 2026  
**Jenis release:** public beta / pre-release  
**Versi sebelumnya:** `v0.3.0-beta`  
**Status evidence:** automated repository checks and browser-level site regression pass; native ChatGPT Projects manual evaluation and student pilot are **not complete**.

## Ringkasan

Ramu membantu menyusun **satu mata kuliah dalam satu ChatGPT Project**: course pack memberi konteks akademik; Project Instructions mengarahkan bantuan belajar, tugas, dan review; source registry menandai status referensi.

`v0.4.0-beta` melengkapi reference implementation UT S1 Akuntansi 2026/2027 menjadi **Semester 1–3**, menyelesaikan putaran perombakan pengalaman website/onboarding, serta memperjelas perilaku tutor adaptif dan mekanisme pengawasan integritas sumber. Ramu Starter tetap tersedia untuk mata kuliah di luar katalog UT dan tidak membutuhkan OpenAI API.

## Perubahan utama

### 1. Semester 1 dan onboarding

- UT S1 Akuntansi 2026/2027 kini mempunyai tiga maintained pack: Semester 1 **18 SKS / tujuh slot mata kuliah**, Semester 2 **16 SKS / lima mata kuliah**, dan Semester 3 **20 SKS / tujuh mata kuliah**.
- Slot Pendidikan Agama Semester 1 adalah pilihan **satu** mata kuliah sesuai registrasi mahasiswa, bukan enam kelas wajib terpisah.
- Alur website/setup memakai katalog dan manifest sebagai sumber metadata; Semester 2 tetap default entry historis, dengan daftar Semester 1–3 dalam urutan akademik.
- Pengalaman homepage dan setup dibuat lebih jelas dan responsif; regression Playwright mencakup ukuran mobile, keyboard, keterbacaan, dan area interaksi.

### 2. Tutor adaptif dengan fallback

- Project Instructions untuk Starter dan tiga pack memakai penjelasan teks, tabel/diagram, contoh langkah, atau format interaktif **jika tersedia dan membantu**; format interaktif bukan persyaratan runtime.
- Learner state dan mastery map membedakan jawaban mandiri vs setelah petunjuk. Menyelesaikan flashcard/visual bukan otomatis bukti penguasaan.
- Ramu **tidak** menganggap Study Mode tersedia di Project conversations, dan tidak mengandalkan kemampuan eksklusif satu model/plan.

### 3. Source Watch dan sumber tepercaya

- GitHub Actions memisahkan review debt dari gate kode: source/claim yang terlambat tetap dilaporkan, tetapi perubahan kode tak terkait tidak otomatis gagal. Scheduled Source Watch tetap strict.
- Probing URL kini membedakan kegagalan DNS/TLS/timeout dan mencoba GET jika HEAD gagal; pemeriksaan dibatasi tiga worker paralel.
- Halaman OpenAI Help Center yang menolak bot dengan HTTP 403 dicatat **advisory / inconclusive**, bukan otomatis bukti hilangnya sumber.
- URL regional UT Banjarmasin yang teramati menampilkan konten tak relevan/error dikarantina menjadi **signal-only**. Rujukan akademik tetap mengikuti katalog pusat dan sumber resmi yang sesuai.

### 4. Dependensi dan kebersihan release

- Playwright `1.63.0` dan pinned `actions/upload-artifact` v7.0.2 melalui Dependabot serta review CI.
- Bahasa Indonesia tetap dokumentasi kanonik; jalur pengenalan berbahasa Inggris tersedia melalui README/CONTRIBUTING English.
- Tampilan social-preview untuk tautan website sudah memakai Open Graph/Twitter image. **Pengaturan Social preview di halaman GitHub repository berbeda dan perlu diverifikasi/diunggah terpisah.**

## Verifikasi yang telah dikerjakan

- CI `Validate Ramu`: JSON schema, catalog/manifest/registry, identity, evaluasi konfigurasi tiga pack, test generator, dan browser regression. Lulus pada `main` sebelum proses release.
- GitHub Pages hanya dideploy setelah gate `validate` pada push ke `main` berhasil.
- Source Watch manual [20 Oktober 2026](https://github.com/man612/ramu/actions/runs/39384171914) **SUCCESS**: 28 source + 8 claim masih dalam interval review; dari 26 URL dipantau, 22 URL UT menghasilkan HTTP 200 dan empat OpenAI Help Center menghasilkan HTTP 403 berpolicy advisory. Keberhasilan URL **bukan verifikasi isi dokumen terbaru**.
- Kegagalan jaringan UT yang terjadi 19 Oktober tidak terulang dalam run tersebut; penyebab pastinya tidak diketahui karena log lama tidak cukup rinci.

## Status batas validasi — penting

**Tidak diklaim sudah selesai:**
- Pengujian manual E01–E16 pada native ChatGPT Projects, termasuk perbedaan retrieval, memory, dan perilaku tiap model.
- Pilot 5–10 mahasiswa, pengukuran friction setup, atau bukti peningkatan hasil belajar.
- Bukti bahwa seluruh jawaban atau sumber masa depan akan selalu benar.
- Launch besar ke komunitas dan penyetelan gambar Social preview **repository GitHub**.

Lihat [#13](https://github.com/man612/ramu/issues/13) untuk manual validation/pilot dan [#52](https://github.com/man612/ramu/issues/52) untuk adopsi publik. Status akademik `source-verified` adalah review referensi, bukan jaminan lulus uji perilaku model. Release tetap pre-release dan **bukan versi stabil 1.0**.

## Mulai menggunakan Ramu

1. Buka [website Ramu](https://man612.github.io/ramu/) dan pilih pack, atau gunakan [Ramu Starter](https://github.com/man612/ramu/tree/main/starter) untuk mata kuliah lain.
2. Pilih satu mata kuliah dan buat satu ChatGPT Project dengan nama yang ditampilkan.
3. Tempel Project Instructions dari setup dan unggah course pack ke Project Sources.
4. Tambahkan buku, rubrik, dan materi pribadi hanya jika relevan; gunakan source yang paling mutakhir untuk informasi yang dapat berubah.
5. Coba mode belajar/review/latihan sesuai kebutuhan. Tinjau hasil model secara kritis, terutama untuk tugas dinilai.

Panduan lengkap: [Setup ChatGPT](https://github.com/man612/ramu/blob/main/docs/PANDUAN-SETUP-CHATGPT.md).

## Rujukan release

- [Changelog v0.4.0-beta](../CHANGELOG.md)
- [Perbandingan dari v0.3.0-beta](https://github.com/man612/ramu/compare/v0.3.0-beta...v0.4.0-beta)
- [Proses release](RELEASE-PROCESS.md)

Release ini adalah snapshot repository pada SHA tag `v0.4.0-beta`; saat proses publikasi, tag tidak dipindahkan setelah dibuat.
