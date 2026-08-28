# Pilot Public Beta Ramu

Dokumen ini dipakai untuk menguji apakah Ramu benar-benar membantu mahasiswa, bukan hanya terlihat rapi di repository.

## Target awal

Mulai dari 5–10 mahasiswa yang sesuai dengan course pack yang sedang tersedia. Tujuannya bukan mengejar star GitHub, tetapi menemukan friction setup, failure mode tutor, dan apakah pengguna kembali memakai Ramu setelah percobaan pertama.

## Skenario minimum

Setiap peserta diminta:

1. memasang satu mata kuliah terlebih dahulu, bukan seluruh semester;
2. menjalankan satu sesi memahami konsep yang belum dikuasai;
3. meminta Ramu mengecek jawaban buatan sendiri;
4. memakai satu materi/screenshot/PDF yang memang mereka punya;
5. kembali memakai Project yang sama pada hari berbeda.

Setelah satu Project berhasil dan manfaatnya terasa, baru tawarkan setup mata kuliah lain.

## Data yang dicatat

Jangan menyimpan isi tugas atau data pribadi tanpa izin. Yang dibutuhkan cukup metrik proses:

- **activation** — berhasil setup satu Project dan mengirim sesi pertama;
- **time-to-first-value** — seberapa jauh proses setup terasa sebelum manfaat pertama didapat;
- **setup failure** — langkah mana yang membingungkan atau gagal;
- **behavior failure** — contoh ketika tutor terlalu cepat memberi jawaban, salah memilih source, menebak informasi, atau kehilangan konteks;
- **return use** — apakah pengguna kembali memakai Ramu dalam 7 hari;
- **multi-course adoption** — apakah setelah mencoba satu mata kuliah pengguna memilih memasang mata kuliah lain;
- **qualitative feedback** — hal yang lebih enak/lebih buruk dibanding memakai ChatGPT biasa.

## Kriteria sebelum menyebut paket stabil

Public beta tidak sama dengan tervalidasi penuh. Sebelum label stabil dipertimbangkan, minimal:

- static validator dan dry-run eval selalu hijau;
- behavior eval nyata sudah dijalankan dan hasilnya direview;
- critical failure yang ditemukan pilot sudah masuk eval regression bila bisa direproduksi;
- setup satu mata kuliah dapat diselesaikan pengguna baru tanpa bantuan maintainer secara terus-menerus;
- source resmi aktif masih berada dalam interval review;
- tidak ada blocker lisensi, secret, atau materi berhak cipta di repo.

## Cara memakai feedback

Feedback seperti “jawabannya kurang enak” belum cukup menjadi perubahan prompt. Cari failure yang dapat dijelaskan dan diuji, misalnya:

- AI langsung memberi jawaban lengkap sebelum mahasiswa mencoba;
- source regional mengalahkan katalog pusat;
- screenshot yang tidak terbaca malah ditebak;
- feedback tutor dari sesi sebelumnya tidak dipakai;
- Project satu mata kuliah mulai mencampurkan konteks mata kuliah lain.

Jika failure dapat direproduksi, perbaiki behavior lalu tambahkan eval agar regresi yang sama tidak kembali diam-diam.
