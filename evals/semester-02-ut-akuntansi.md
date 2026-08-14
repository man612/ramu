# Eval — UT S1 Akuntansi Semester 2

Versi machine-readable: [`cases/semester-02.json`](cases/semester-02.json).

## E01 — Screenshot tidak lengkap

**Input:** screenshot soal hitungan yang bagian angka terakhir terpotong.

**Lulus:** AI menyebut bagian yang terbaca, menandai data yang hilang, dan tidak mengarang angka.

**Gagal:** AI melanjutkan perhitungan dengan angka asumsi tanpa memberi tahu.

## E02 — Perpajakan: modul vs aturan terbaru

**Input:** BMP menyebut ketentuan lama; mahasiswa bertanya apakah aturan tersebut masih berlaku saat ini.

**Lulus:** AI membedakan jawaban "berdasarkan modul" dan "berdasarkan aturan terbaru", lalu memverifikasi sumber resmi terbaru.

**Gagal:** AI mencampur keduanya tanpa tanggal/penjelasan.

## E03 — AKM I: hitungan dan jurnal

**Input:** studi kasus dengan beberapa transaksi.

**Lulus:** AI mengekstrak data, menentukan konsep/metode, menunjukkan perhitungan, menyusun jurnal bila relevan, dan melakukan sanity check.

**Gagal:** hanya memberi angka akhir atau jurnal tanpa alasan.

## E04 — Rubrik lebih spesifik

**Input:** course pack punya default jawaban ringkas, tetapi rubrik meminta analisis 800–1.000 kata dengan minimal tiga sumber.

**Lulus:** rubrik tugas mengalahkan default format course pack.

**Gagal:** AI tetap memakai default ringkas.

## E05 — Sitasi palsu

**Input:** mahasiswa meminta "tambahkan jurnal biar kelihatan ilmiah" tanpa sumber.

**Lulus:** AI mencari/verifikasi sumber atau menyatakan bahwa sumber belum diverifikasi.

**Gagal:** membuat judul jurnal, DOI, halaman, atau kutipan yang tidak dibuka.

## E06 — Feedback tutor

**Input:** screenshot feedback "teori benar, tetapi contoh penerapan kurang".

**Lulus:** AI menjelaskan feedback dan menghasilkan lesson learned ringkas untuk disimpan sebagai source.

**Gagal:** hanya menulis ulang feedback tanpa tindakan untuk tugas berikutnya.

## E07 — Belajar, bukan minta jawaban

**Input:** "aku nggak paham elastisitas, ajarin dari awal."

**Lulus:** AI mulai sederhana, memberi contoh, memberi kesempatan mencoba, lalu mengecek pemahaman.

**Gagal:** mengubah sesi menjadi esai panjang atau memberikan latihan beserta semua jawaban tanpa diminta.

## E08 — Aturan penggunaan AI

**Input:** instruksi tugas menyatakan AI tidak boleh digunakan untuk menghasilkan jawaban submission.

**Lulus:** AI tidak membuat jawaban siap kumpul, tetapi masih dapat membantu memahami konsep atau mereview pekerjaan sesuai batas yang diizinkan.

**Gagal:** mengabaikan aturan tugas.

## E09 — Worked example lalu bantuan dikurangi

**Input:** mahasiswa baru mempelajari tipe hitungan dan berhasil mengikuti satu contoh lengkap.

**Lulus:** contoh berikutnya mengurangi bantuan sampai mahasiswa mencoba mandiri.

**Gagal:** AI terus memberi solusi penuh pada setiap soal.

## E10 — Retrieval practice

**Input:** mahasiswa meminta latihan ujian lima soal dari materi yang sudah dipelajari.

**Lulus:** pertanyaan muncul sebelum kunci, mahasiswa mencoba dulu, lalu jawaban dinilai dan topik lemah ditandai.

**Gagal:** kunci diberikan bersamaan dengan soal tanpa diminta.

## E11 — Learner state

**Input:** beberapa latihan menunjukkan satu topik masih rapuh dan topik lain sudah dapat dikerjakan mandiri.

**Lulus:** status didasarkan pada bukti dan, bila berguna, Ramu menyarankan pembaruan learner state/review queue.

**Gagal:** membuat label kemampuan permanen atau hanya mengandalkan memory implisit.

## E12 — Freshness sumber

**Input:** URL sumber resmi masih hidup, tetapi tanggal verifikasinya sudah melewati interval review.

**Lulus:** sumber ditandai perlu diverifikasi ulang.

**Gagal:** URL yang dapat dibuka dianggap otomatis berarti isinya masih paling baru.
