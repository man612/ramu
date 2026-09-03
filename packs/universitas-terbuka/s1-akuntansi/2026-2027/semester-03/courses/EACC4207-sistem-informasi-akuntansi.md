# EACC4207 — Sistem Informasi Akuntansi

**Semester:** 3  
**SKS:** 3  
**Versi paket:** 2026-2027.s3.1  
**Sumber paket diverifikasi:** 3 September 2026  
**Waktu ujian:** I.3  
**Bahan ajar katalog:** EKSI4312 Sistem Informasi Akuntansi (Edisi 4)  
**Layanan katalog:** T  
**Catatan:** termasuk mata kuliah prasyarat TAPS S1 Akuntansi.

## Fokus Project

BMP membahas konsep dan penerapan Sistem Informasi Akuntansi (SIA), metode/teknik pengembangan sistem, sistem berbasis komputer, DBMS, serta siklus pendapatan, pengeluaran, produksi, penggajian, dan pelaporan. Flowchart digunakan sebagai alat untuk memahami proses bisnis dan aliran informasi.

Untuk pertanyaan SIA, jangan langsung menggambar alur sebelum memahami **aktor, dokumen/data, event bisnis, titik keputusan, sistem yang digunakan, dan tujuan pengendalian**.

## Workflow analisis sistem

1. tentukan proses/siklus yang dianalisis;
2. identifikasi aktor internal/eksternal dan tanggung jawabnya;
3. identifikasi input, dokumen, data store/database, proses, dan output;
4. susun urutan event bisnis dari awal sampai selesai;
5. tandai authorization, custody, recording, reconciliation, atau control point yang relevan;
6. baru buat flowchart/DFD/deskripsi proses sesuai notasi yang diminta;
7. cek apakah aliran data dan dokumen dapat ditelusuri end-to-end;
8. jelaskan kelemahan kontrol dan usulan perbaikan bila diminta.

## Verifier khusus

- jangan mencampur aliran barang, kas, dokumen, dan data seolah sama;
- setiap simbol/step flowchart harus punya fungsi yang dapat dijelaskan;
- aktor yang mengotorisasi transaksi tidak otomatis boleh memegang aset atau mencatat transaksi;
- output sistem harus dapat ditelusuri ke input/proses yang menghasilkan;
- database/table tidak boleh dikarang jika kasus tidak memberi atau tidak memerlukan detail tersebut;
- kelemahan kontrol harus dihubungkan dengan risiko yang nyata, bukan daftar kontrol generik;
- solusi sistem harus menjawab masalah yang ditemukan, bukan sekadar menambah teknologi.

## Jika soal meminta desain

Jika requirement penting belum ada—misalnya siapa yang menyetujui transaksi, kapan pencatatan terjadi, atau sistem mana yang menjadi source of truth—nyatakan requirement yang masih kosong. Boleh membuat asumsi untuk latihan **hanya jika ditandai jelas sebagai asumsi**, bukan fakta kasus.

## Aturan umum

- Baca soal/rubrik lengkap sebelum membuat diagram.
- Prioritaskan BMP dan notasi yang digunakan tutor jika ada.
- Jangan membuat detail organisasi, software, database, atau kontrol yang tidak diberikan tanpa menandainya sebagai asumsi.
- Jika gambar/diagram input tidak terbaca, minta versi yang lebih jelas daripada menebak label.
- Akhiri dengan pemeriksaan aliran proses, data, aktor, control objective, dan konsistensi diagram dengan penjelasan.
