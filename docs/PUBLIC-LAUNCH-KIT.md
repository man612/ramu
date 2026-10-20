# Ramu — Public Sharing Kit (v0.4.0-beta)

Dokumen ini membantu membagikan Ramu dengan klaim yang akurat. **Ini bukan laporan pilot dan bukan izin untuk mengklaim hasil belajar sudah terbukti.** Tidak ada promosi ke pihak luar yang otomatis dikirim dari repository.

## Identitas singkat

- **Nama:** Ramu
- **Descriptor:** workspace belajar terstruktur untuk ChatGPT Projects
- **Janji paling sederhana:** satu mata kuliah, satu Project, supaya course pack, sumber, rubrik, dan catatan belajar tidak bercampur.
- **Untuk siapa:** mahasiswa yang menggunakan ChatGPT Projects, dan developer/kontributor yang ingin melihat cara menyusun pack serta validation tooling.
- **Status:** public beta (`v0.4.0-beta`), bukan produk yang sudah lulus pilot.
- **Website:** https://man612.github.io/ramu/
- **Setup:** https://man612.github.io/ramu/setup.html
- **Repo:** https://github.com/man612/ramu
- **Release:** https://github.com/man612/ramu/releases/tag/v0.4.0-beta
- **Pengujian manual yang belum selesai:** https://github.com/man612/ramu/issues/13

## Narasi untuk mahasiswa (Bahasa Indonesia)

**Versi pendek**

> kalau tiap mata kuliah di ChatGPT suka bercampur konteks, aku bikin Ramu: pola setup satu mata kuliah dalam satu ChatGPT Project. Sudah ada contoh pack UT S1 Akuntansi Semester 1–3, dan mata kuliah lain bisa pakai Ramu Starter. Masih beta, jadi hasil AI tetap harus diperiksa. Lihat cara kerjanya di https://man612.github.io/ramu/

**Versi diskusi yang lebih informatif**

> Ramu adalah proyek terbuka untuk mengatur belajar di ChatGPT Projects. Idenya sederhana: satu mata kuliah punya Project sendiri, dengan course pack, instruksi bantuan belajar, sumber, dan materi kelas yang tidak tercampur mata kuliah lain. Untuk UT S1 Akuntansi 2026/2027 ada contoh Semester 1–3; kalau di luar itu, tersedia Starter untuk disusun dari konteks masing-masing. Versi saat ini `v0.4.0-beta` dan belum diklaim lolos pengujian manual/pilot mahasiswa. Website: https://man612.github.io/ramu/

Tidak perlu menulis bahwa Ramu “menaikkan IPK”, “menjamin jawaban benar”, atau bisa menggantikan kebijakan tutor/dosen.

## Narasi untuk developer (Bahasa Indonesia)

> Ramu adalah proyek open-source untuk menyusun study workspace berbasis ChatGPT Projects: core protocol, context/course pack, source registry, lintas-scope eval contract, static validation, browser QA, dan Source Freshness Watch. Alur dasarnya tidak bergantung pada OpenAI API; eval model via API bersifat opsional. `v0.4.0-beta` melengkapi contoh tiga semester UT S1 Akuntansi, menguatkan adaptive tutoring dengan fallback, serta memisahkan source review debt dari CI tanpa menonaktifkan monitor terjadwal. Pengujian manual di Projects dan pilot mahasiswa masih outstanding. Repo: https://github.com/man612/ramu

## English short description

> Ramu is an open-source structured learning workspace for ChatGPT Projects: one course per Project, with clear project instructions, course context, source provenance, and reusable validation tools. The public beta includes UT Accounting reference packs for Semesters 1–3 and a generic Starter for other courses. The project does not require the OpenAI API for normal use. Native Projects manual behavior testing and student pilots are not complete. https://github.com/man612/ramu

## Alur first-use yang benar

**Bila mata kuliah ada di katalog:**

1. Kunjungi website; pilih pack dan mata kuliah.
2. Buat ChatGPT Project dengan nama yang disediakan, dan gunakan Project-only memory bila tersedia/tepat.
3. Salin Project Instructions dari halaman setup.
4. Unduh course pack dan pasang ke Project Sources.
5. Tambahkan silabus, BMP, rubrik, atau materi pribadi secara selektif.
6. Mulai belajar atau review; cek jawaban AI terhadap sumber asli bila konsekuensinya penting.

**Bila mata kuliah tidak ada di katalog:**

1. Buka [Ramu Starter](../starter/README.md) untuk menghasilkan workspace personal lewat generator Python.
2. Tinjau isi yang dihasilkan; data/sumber yang diisi pengguna **tidak otomatis source-verified**.
3. Pasang Project Instructions dan COURSE-PACK.txt ke ChatGPT Project.
4. Jangan mengklaim hasil Starter sebagai maintained/public pack.

## FAQ ringkas

**Apakah Ramu aplikasi ChatGPT resmi?** Tidak. Ramu adalah proyek independen yang menyiapkan instruksi dan course pack untuk fitur ChatGPT Projects.

**Apakah perlu OpenAI API atau VPS?** Tidak untuk penggunaan biasa. Website adalah statis, course pack diunduh pengguna, dan project context dikelola langsung di ChatGPT.

**Apakah semua fitur visual/GPT terbaru selalu tersedia di Project?** Tidak dijamin. Instruksi Ramu memilih format visual/interaktif hanya jika memang didukung; fallback teks tetap ada.

**Apakah pack sudah membuktikan AI selalu menjawab benar?** Tidak. `source-verified` menunjukkan status review referensi pack, bukan lulus pengujian semua respons model. E01–E16 pada native Projects dan pilot mahasiswa masih perlu dilakukan.

**Apakah data kuliah pribadi tersimpan di server Ramu?** Website Ramu statis; materi pribadi ditambahkan langsung ke ChatGPT Project oleh pengguna. Kebijakan privasi/penggunaan data mengikuti pengaturan dan ketentuan akun ChatGPT mereka.

## Checklist sebelum membagikan ke komunitas

- [x] Repo, website, panduan setup, dan release `v0.4.0-beta` tersedia.
- [x] CI/Pages dan Source Watch sudah punya run sukses tanggal 20 Oktober 2026.
- [x] Teks publik menjelaskan beta dan keterbatasan bukti.
- [ ] **Social preview repository GitHub**: pasang `site/social-preview.png` lewat GitHub repository Settings → Social preview → Edit → Upload an image; file sudah tersedia di repository. Ini berbeda dengan Open Graph image website.
- [ ] Manual Projects behavior evaluation dan pilot pengguna nyata (lihat issue #13).
- [ ] Setelah evidence first-use siap, pilih komunitas yang relevan dan ikuti aturan masing-masing forum. Hindari spam, paid/fake stars, dan klaim statistik tanpa data.

**Catatan release:** Dokumen ini ditulis setelah tag `v0.4.0-beta` terbit. Dokumen ini adalah *Unreleased* maintenance documentation, bukan bagian dari immutable snapshot tag tersebut.
