# Arah Proyek

## Tujuan

Ramu menyediakan konfigurasi workspace akademik yang bisa dipasang ke platform AI tanpa memaksa mahasiswa belajar prompt engineering.

Implementasi pertama memakai **ChatGPT Projects**, tetapi format core dan pack tidak dibuat sebagai dokumentasi produk OpenAI semata. Jika platform utama berubah, course context dan aturan sumber tetap dapat digunakan kembali melalui adapter/panduan baru.

## Unit utama

- **Core** — prinsip umum yang jarang berubah.
- **Pack institusi/program/semester** — data resmi dan aturan kontekstual.
- **Course pack** — konfigurasi siap upload untuk satu mata kuliah.
- **Project Instructions** — perilaku umum yang ditempel ke Project.
- **Eval** — skenario untuk menguji apakah konfigurasi bertingkah sesuai harapan.
- **Site** — antarmuka publik yang memudahkan pengguna menemukan pack tanpa harus memahami struktur repo.

## Prinsip versioning

Data akademik selalu ditulis bersama tahun akademik dan tanggal verifikasi. Jika kampus mengubah kurikulum, pack baru dibuat pada jalur versi/tahun baru; pack lama tidak diam-diam ditimpa seolah masih berlaku.

## Status pack

- **Sumber terverifikasi** — data dan aturan utama sudah diperiksa terhadap sumber resmi primer yang masih berlaku, tetapi pack belum dinyatakan lolos eval perilaku secara penuh.
- **Terverifikasi** — sumber sudah terverifikasi dan pack telah melewati eval inti yang relevan.
- **Komunitas** — kontribusi pihak lain yang belum selesai diverifikasi penuh.
- **Eksperimental** — format atau workflow masih diuji.
- **Kedaluwarsa** — sumber sudah digantikan versi lebih baru.

## Bukan target Ramu

- menyimpan jawaban tugas massal;
- menyalin BMP berhak cipta;
- menjadi LMS pengganti kampus;
- menebak nilai akhir mahasiswa;
- menjanjikan keluaran AI selalu benar;
- mengunci pengguna ke satu model atau satu vendor untuk selamanya.
