# Memperbarui Ramu di ChatGPT Project yang sudah dipakai

Panduan ini untuk pengguna yang **sudah memiliki** ChatGPT Project satu mata kuliah. **Jangan membuat Project baru hanya karena Ramu atau website mendapat rilis baru.** Chat, file pribadi, dan catatan belajarmu tetap penting.

## Bedakan tiga jenis pembaruan

| Yang berubah | Apa yang perlu dilakukan |
|---|---|
| Website, workflow CI, metadata registry internal, atau rilis repository | Biasanya **tidak perlu** mengubah Project maupun mengunggah ulang course pack. |
| **Project Instructions** untuk pack yang sedang dipakai | Buka Project yang ada → `⋯ → Project settings → Project Instructions`; periksa/perbarui teks instruksi. Perubahan ini tidak otomatis mengubah isi file course pack. |
| **Course pack** untuk mata kuliah yang sama (isi/kode/versi akademik berubah) | Bandingkan dulu dengan versi yang terpasang, kemudian **ganti source course pack lama** dengan file baru sesuai langkah aman di bawah. |

`v0.4.0-beta` adalah **versi repository Ramu**, bukan penanda bahwa seluruh course pack wajib diunggah ulang. Pada tiap pack ada `pack_version` sendiri di manifest/katalog. Kode mata kuliah, tahun akademik, dan sumber yang relevan lebih penting daripada hanya membandingkan tanggal unduh.

## Langkah aman untuk Project yang sudah ada

1. Buka **Project mata kuliah yang sudah ada**, bukan membuat `New Project` lagi. Pastikan nama dan mata kuliahnya cocok dengan pack baru.
2. Cek identitas dan periode akademik sebelum mengganti apa pun. Untuk perubahan tahun kurikulum, kode course, atau mata kuliah, **jangan otomatis menimpa** Project lama: konteksnya mungkin berbeda dan perlu Project terpisah.
3. Buka [setup Ramu](https://man612.github.io/ramu/setup.html), pilih pack/semester yang sesuai. Salin Project Instructions lalu perbarui pada **Project settings**, jika memang versi instruksinya berbeda. Jangan menempel instruksi itu sebagai chat atau file source pengganti.
4. Kalau **isi course pack** memang lebih baru, unduh file .txt dari mata kuliah yang tepat. Sebelum menghapus apa pun, catat versi/identitas course pack lama dan simpan salinan file pribadi yang diperlukan.
5. Di area **Sources** pada ChatGPT Project, identifikasi file course pack lama berdasarkan **nama dan isi/versinya**, bukan dengan menghapus seluruh Sources. Simpan file pribadi, BMP, rubrik, dan materi dosen yang masih relevan.
6. Unggah file course pack baru. **Jika nama file sama**, pilihan `Upload anyway` dapat menambahkan file baru di samping file lama; `Skip` justru dapat melewatkan versi baru. Periksa daftar Sources setelah upload dan **hapus hanya course pack lama yang benar-benar tergantikan**. Jangan biarkan dua pack yang bertentangan sama-sama aktif.
7. Kalau ada `Catatan Belajar Terbaru`, pertahankan yang terbaru agar progres belajar tidak hilang. Jika catatan lama dan baru bertentangan, tinjau sebelum menghapus versi usang. Pembaruan course pack **bukan alasan** menghapus seluruh riwayat chat.
8. Jika Project dibagikan, koordinasikan perubahan dengan anggota lain: menghapus source dari Shared Project memengaruhi semua anggota. Pengaturan memory Shared Project juga berbeda dari Project pribadi.

## Memastikan hasil pembaruan

- Project masih untuk **mata kuliah yang sama**, dan tahun/periode akademik relevan.
- Instruksi Project sesuai alur Ramu yang ingin dipakai.
- Hanya **satu versi course pack aktif** untuk mata kuliah itu; BMP dan materi penting lain tetap utuh.
- Tidak ada anggapan bahwa konten baru secara otomatis memperbarui jawaban atau learner state yang sebelumnya keliru. Periksa ulang konsep/aturan yang berubah.
- Status `source-verified` bukan bukti bahwa setiap respons model telah lulus pengujian manual.

## Memory, file, dan keterbatasan produk

ChatGPT Projects dapat memakai **Project-only memory** untuk membatasi rujukan lintas Project. Pengaturan ini dipilih saat membuat Project dan dapat diubah melalui **Project settings → Memory** bila tersedia; perubahan mungkin perlu beberapa jam. Persyaratan Memory pribadi/workspace dapat berbeda. Pada akun yang hanya menampilkan **Enable memory**, aktifkan pengaturan itu jika ingin memakai memory; pada pengalaman lama yang masih memiliki dua toggle terpisah, ikuti persyaratan sesuai plan.

File dan respons yang disimpan di Sources adalah **sumber**, bukan instruksi berotoritas untuk menimpa Project Instructions. Link Google Drive yang ditambahkan lewat aplikasi tidak otomatis tersinkron menjadi indeks lokal Project.

Rujukan resmi OpenAI:
- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)
- [Memory in ChatGPT](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

**Privasi:** Ramu adalah website statis; tidak dapat melihat atau mengubah Project milik pengguna secara otomatis. Pembaruan Project hanya dilakukan pengguna melalui ChatGPT. Jangan menaruh materi privat di issue publik Ramu.
