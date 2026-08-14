# Panduan Setup Ramu di ChatGPT Android

Panduan ini dibuat untuk pengguna yang ingin langsung memakai Ramu tanpa perlu memahami GitHub, prompt engineering, atau cara kerja teknis di belakangnya.

Tujuannya sederhana: setelah setup selesai, kamu memiliki lima Project ChatGPT untuk Semester 2 dan dapat menggunakannya untuk belajar, mengerjakan tugas, memeriksa jawaban, atau membahas feedback tutor.

## Yang akan dibuat

- `S2 • Perpajakan`
- `S2 • AKM I`
- `S2 • Manajemen Keuangan`
- `S2 • Ekonomi Mikro`
- `S2 • Manajemen`

Satu mata kuliah dibuat sebagai satu Project agar file, percakapan, dan konteksnya tidak bercampur dengan mata kuliah lain.

## Langkah 1 — periksa Memory ChatGPT

Di aplikasi ChatGPT, buka:

`Settings → Personalization → Memory`

Pastikan pengaturan Memory yang dibutuhkan Projects aktif. Untuk akun personal, dokumentasi OpenAI saat ini menjelaskan bahwa **Reference saved memories** dan **Reference chat history** perlu aktif agar Project memory dapat digunakan.

Saat membuat Project nanti, pilih **Project-only memory**. Artinya, konteks Project tersebut dijaga tetap berada di dalam ruang mata kuliah itu dan tidak mengambil percakapan dari luar Project.

### Pilihan privasi

Kalau ingin mengatur apakah percakapan boleh digunakan untuk membantu peningkatan model, buka:

`Settings → Data Controls → Improve the model for everyone`

Pengaturan ini merupakan pilihan akunmu dan bukan syarat untuk menggunakan Ramu.

## Langkah 2 — salin Project Instructions

Buka:

[`PROJECT-INSTRUCTIONS.md`](../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/PROJECT-INSTRUCTIONS.md)

Salin seluruh isinya.

Project Instructions **bukan Project Source**. Setelah Project dibuat, buka:

`⋯ → Project settings → Project Instructions`

lalu tempel teks Ramu di sana. Instruksi yang sama digunakan untuk kelima mata kuliah.

## Langkah 3 — buat Project pertama

Mulai dari Perpajakan.

1. Buka ChatGPT.
2. Pilih **New Project**.
3. Beri nama `S2 • Perpajakan`.
4. Pilih **Project-only memory**.
5. Buka `⋯ → Project settings → Project Instructions`.
6. Tempel Project Instructions dari langkah 2.
7. Dari panduan setup interaktif Ramu, tekan **Unduh paket (.txt)** untuk Perpajakan.
8. Kembali ke Project dan buka **Sources → Add source → Upload files**.
9. Pilih file course pack yang baru diunduh.

Jika file tersebut sudah tersimpan di Library ChatGPT, **Add from library** juga dapat digunakan.

Course pack sumber di repo tetap dapat dilihat di:

[`EACC4104-perpajakan.md`](../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/courses/EACC4104-perpajakan.md)

Setelah itu, Project Perpajakan selesai disiapkan.

## Langkah 4 — ulangi untuk empat mata kuliah lain

Caranya sama. Yang berubah hanya nama Project dan course pack-nya.

| Nama Project | Course pack |
|---|---|
| `S2 • AKM I` | [`EACC4103-akm-1.md`](../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/courses/EACC4103-akm-1.md) |
| `S2 • Manajemen Keuangan` | [`EMBS4210-manajemen-keuangan.md`](../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/courses/EMBS4210-manajemen-keuangan.md) |
| `S2 • Ekonomi Mikro` | [`ECON4102-ekonomi-mikro.md`](../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/courses/ECON4102-ekonomi-mikro.md) |
| `S2 • Manajemen` | [`EMBS4101-manajemen.md`](../packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/courses/EMBS4101-manajemen.md) |

Panduan interaktif menghasilkan file `.txt` dari course pack yang sama supaya lebih aman dipilih melalui menu **Upload files**. Ramu tidak bergantung pada opsi paste-text di Sources, karena pada sebagian UI Project opsi yang terlihat hanya upload file dan Add from library.

Setelah kelima Project selesai dibuat, setup semester selesai.

## Setelah setup, bagaimana cara menggunakannya?

GitHub tidak perlu dibuka setiap kali ada tugas.

### Kalau ada tugas AKM I

1. Buka ChatGPT.
2. Masuk ke `S2 • AKM I`.
3. Buat chat baru.
4. Kirim screenshot, PDF, atau teks soal.
5. Tulis, misalnya: `bantu aku kerjakan tugas ini`.

### Kalau belum memahami materi

Kirim bagian materi yang dimaksud, lalu tulis:

`aku belum paham bagian ini`

### Kalau sudah memiliki jawaban

Kirim jawabanmu, lalu tulis:

`cek jawabanku`

### Kalau tutor memberikan feedback

Kirim feedback tersebut, lalu tulis:

`ini feedback tutor kemarin`

Jika dari sesi belajar/review muncul pola yang berguna untuk dibawa ke chat berikutnya, Ramu dapat membuat **Catatan Belajar Terbaru**. Jika menu respons menyediakan **Save to project / Add to project sources**, simpan respons itu di sana. Jika kemudian dibuat versi yang lebih baru, hapus source lama agar dua catatan yang bertentangan tidak dipakai bersamaan.

## Mengatur file supaya Project tidak cepat penuh

Course pack sebaiknya menjadi source tetap. Untuk pekerjaan harian:

- screenshot soal dapat dikirim langsung di chat;
- rubrik/materi ditambahkan hanya saat relevan;
- file lama yang sudah tidak diperlukan dapat dihapus;
- potongan materi pendek dapat dikirim di chat bila tidak perlu menjadi source permanen.

Batas file per Project bergantung pada paket ChatGPT dan dapat berubah. Dokumentasi resmi OpenAI menjadi acuan terbaru untuk batas tersebut.

## Kebiasaan yang disarankan

- Gunakan satu chat untuk satu tugas atau satu topik besar.
- Kalau screenshot soal terpotong, kirim bagian yang kurang. Jangan membiarkan AI menebak isi yang tidak terlihat.
- Kalau tugas memiliki rubrik, kirim rubriknya juga.
- Kalau tugas harus dijawab berdasarkan modul, tambahkan bagian modul yang relevan.
- Untuk informasi yang dapat berubah, seperti aturan pajak, minta pemeriksaan terhadap sumber resmi terbaru.
- Kalau jawaban berisi hitungan, tetap periksa hasil akhirnya sebelum dikumpulkan.

## Tentang Study Mode

Ramu tidak bergantung pada Study Mode bawaan ChatGPT. Alur belajar Ramu tetap ditangani oleh Project Instructions. Jika Study Mode tersedia dan nyaman dipakai di Project akunmu, anggap sebagai alat tambahan, bukan syarat Ramu.

## Kalau nama menu ChatGPT berbeda

Tampilan dan nama menu ChatGPT dapat berubah seiring pembaruan aplikasi. Kalau nama menu sedikit berbeda, cari fungsi yang setara pada pengaturan Project, Sources, atau Memory. Untuk setup Ramu, patokan praktisnya tetap: **Project Instructions masuk ke Project settings; course pack masuk ke Sources sebagai file**.
