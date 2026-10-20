# Kajian perubahan regulasi pajak — Oktober 2026

**Ditinjau:** 20 Oktober 2026  
**Relevansi:** UT S1 Akuntansi `EACC4104 Perpajakan` (Semester 2) dan `EACC4206 Laboratorium Perpajakan` (Semester 3).  
**Status:** dua perubahan aturan resmi **ditemukan dan diberi bukti di source registry**. Tidak ditemukan klaim tarif tetap yang jelas salah dalam kedua course pack; tidak ada alasan untuk menerbitkan ulang semua Project atau mengubah metadata kurikulum UT.

Ini adalah **catatan perubahan hukum saat tanggal review**, bukan nasihat pajak individual, tabel tarif permanen, atau pengganti BMP dan soal tutor.

## 1. PER-12/PJ/2026 — berlaku 1 Oktober 2026

**Sumber primer:** [DJP — PER-12/PJ/2026 (perubahan atas PER-11/PJ/2025)](https://www.pajak.go.id/index.php/id/peraturan/perubahan-atas-peraturan-direktur-jenderal-pajak-nomor-11pj2025-tentang-ketentuan). Peraturan ditetapkan **28 September 2026**, berlaku **1 Oktober 2026**, dan tercatat aktif pada halaman DJP.

- **Pasal 129A ayat (1):** hak dan kewajiban terkait pembetulan SPT didasarkan pada SPT pembetulan terakhir yang disampaikan.
- **Pasal II angka 1:** ada **ketentuan peralihan**. Pelaporan/pembetulan yang disampaikan sebelum berlaku dan belum selesai tindak lanjutnya mengikuti ketentuan PER-11/PJ/2025. Pembetulan yang disampaikan **setelah** PER-12 berlaku untuk masa/tahun pajak sejak 2025, sebagaimana dirinci pasal, ditindaklanjuti menurut PER-12/PJ/2026.
- Peraturan juga mencakup sejumlah detail pelaporan PPh dan PPN serta perlakuan kompensasi yang **tidak boleh dipadatkan menjadi satu rumus universal**.
- [Penjelasan DJP (30 September 2026)](https://pajak.go.id/index.php/id/artikel/goodbye-skema-delta-coretax-kini-terapkan-skema-replace-mulai-1-oktober-2026-12pj2026) menyebut transisi dari pendekatan *delta* ke *replace*, tetapi untuk skenario tertentu **teks peraturan dan transisi yang berlaku tetap harus diperiksa**.

**Dampak ke pertanyaan belajar:** kasus pembetulan SPT dengan periode, tanggal penyampaian, status tindak lanjut, atau kelebihan bayar berbeda dapat menghasilkan analisis berbeda. Sebelum menghitung, identifikasi minimal **jenis SPT, masa/tahun pajak, kapan SPT normal dan pembetulan disampaikan, serta status pemrosesan**. Jangan memakai contoh BMP lama seolah aturan administratifnya pasti sama pada 2026.

## 2. PMK 71/2026 — berlaku 2 Oktober 2026

**Sumber primer:** [JDIH Kemenkeu — PMK Nomor 71 Tahun 2026](https://www.jdih.kemenkeu.go.id/dok/pmk-71-tahun-2026). Ditetapkan 29 September 2026, diundangkan dan **berlaku 2 Oktober 2026**. Mengubah PMK 118/2024 tentang tata cara pembetulan, keberatan, pengurangan, penghapusan, dan pembatalan di bidang perpajakan.

- Dalam lingkup **Pasal 23 ayat (6)–(7)** hasil perubahan, pembayaran pada dokumen ketetapan/tagihan yang menjadi dasar permohonan pengurangan/penghapusan sanksi dihitung untuk **pokok pajak lebih dahulu**, lalu ke sanksi administratif/denda apabila ada sisa.
- Perubahan itu **bukan pernyataan bahwa semua kewajiban pajak, jenis pembayaran, atau sengketa** selalu mengikuti rumus yang sama tanpa membaca syarat pasal.
- [Siaran pers DJP, 12 Oktober 2026](https://www.pajak.go.id/id/siaran-pers/pemerintah-permudah-penyelesaian-kewajiban-perpajakan) mengonfirmasi perubahan mekanisme penyelesaian utang yang dimaksud.

**Dampak ke pertanyaan belajar:** analisis kasus penagihan, sanksi, dan permohonan pengurangan harus memisahkan **pokok pajak, sanksi/denda, jenis SKP/STP, jumlah pembayaran, dan dasar permohonan**. Jangan mencampurnya dengan perhitungan besaran PPh/PPN pada transaksi lain.

## 3. Apa yang sebenarnya berubah pada Ramu?

| Objek | Temuan | Keputusan |
|---|---|---|
| `EACC4104` Perpajakan (Semester 2) | Sudah mewajibkan verifikasi aturan DJP/Kemenkeu terkini dan membedakan BMP dari hukum saat ini. Tidak ada angka tarif tetap yang bertentangan dengan dua peraturan ini. | **Course pack tetap**. Tambahkan dua sumber primer dan klaim berbatas ruang lingkup pada registry institusi. |
| `EACC4206` Laboratorium Perpajakan (Semester 3) | Sudah meminta cek masa/tahun pajak, sumber resmi, kasus dan state sebelumnya; tidak membekukan Coretax atau ketentuan alokasi pembayaran sebagai hukum permanen. | **Course pack tetap**. Bukti hukum terbaru tersedia melalui registry/tautan catatan ini. |
| Katalog UT, slot ujian, SKS, struktur Semester 1–3 | Perubahan DJP/Kemenkeu tidak otomatis mengubah kurikulum UT. | Tidak mengubah manifest, `pack_version`, atau tanggal verifikasi akademik. |
| Source Watch | Pemeriksaan mingguan Ramu menemukan source registry dan item `watch: true`; tidak memvalidasi isi hukum hanya karena URL hidup. | Tambah dua URL primer dengan jendela review 30 hari dan dua klaim yang harus dibaca ulang sesuai intervalnya. |

## 4. Prosedur cek untuk revisi selanjutnya

1. Cari **sumber primer** pada [daftar peraturan DJP](https://www.pajak.go.id/id/peraturan) atau [JDIH Kemenkeu](https://www.jdih.kemenkeu.go.id/), lalu bedakan tanggal penetapan, pengundangan, mulai berlaku, serta ketentuan peralihan.
2. Cek apakah pasal yang berubah **benar-benar berlaku untuk kasus mata kuliah** yang sedang dibahas. Jangan menyimpulkan perubahan kurikulum dari perubahan regulasi pajak.
3. Jika content course pack perlu diperbarui, barulah naikkan `pack_version` terkait dan tulis alasan/dampak pengguna pada `PACK-CHANGES.md`; jangan memaksa upload ulang semua semester hanya karena ada berita pajak.
4. Jika URL gagal di CI, bedakan kegagalan jaringan dari perubahan hukum. Source Watch merupakan **sinyal review**, bukan pembaca semantik peraturan.
5. Peraturan lain—termasuk PPN, tarif, nilai kurs, atau kebijakan temporer—harus diverifikasi **untuk tanggal/periode kasusnya sendiri**. Dua regulasi di atas tidak cukup untuk menyimpulkan semua ketentuan pajak terbaru.

**Batas audit:** hanya dua regulasi spesifik yang ditelusuri pada 20 Oktober 2026. Kajian ini tidak membuktikan bahwa tidak ada peraturan pajak lain yang berubah, atau bahwa prosedur aplikasi Coretax selalu sama dengan teks peraturan pada setiap akun.
