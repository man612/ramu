# Security Policy

Ramu tidak menjalankan server atau menyimpan akun mahasiswa sendiri, tetapi tetap memiliki risiko keamanan pada prompt, sumber, file yang diunggah, dan tooling evaluasi.

## Versi yang didukung

Security fix diprioritaskan untuk **current `main`** dan **public-beta release terbaru**. Tag beta lama tetap dipertahankan sebagai snapshot yang dapat ditelusuri, tetapi tidak dijanjikan menerima backport untuk setiap perbaikan.

Jika masalah hanya muncul pada release lama, periksa dulu apakah masalah tersebut masih ada pada release terbaru sebelum membuat laporan publik.

## Yang termasuk isu keamanan

Contohnya:

- prompt injection dari source/course material yang dapat mengubah guardrail Ramu;
- source poisoning atau source routing yang membuat informasi tidak tepercaya diperlakukan sebagai sumber resmi;
- secret/API key yang dapat bocor melalui workflow, artifact, log, atau contoh konfigurasi;
- file atau instruksi yang menyebabkan data pribadi/sensitif tersalin ke output publik;
- perubahan tooling yang membuat hasil eval terlihat lulus padahal gate tidak benar-benar dijalankan.

## Pelaporan

Untuk masalah yang tidak mengandung detail sensitif, buka GitHub Issue dengan reproduksi minimal dan dampaknya.

Untuk kerentanan yang memerlukan detail sensitif, gunakan GitHub private vulnerability reporting / Security Advisory repository bila fitur tersebut tersedia. Jangan menempelkan API key, token, data pribadi, materi kuliah privat, atau exploit yang belum diperbaiki ke issue publik.

## Batas keamanan

Ramu adalah lapisan konfigurasi dan evaluasi di atas layanan AI yang digunakan pengguna. Ramu tidak dapat menjamin perilaku model pihak ketiga, uptime layanan, kebijakan privasi platform, atau bahwa setiap jawaban AI selalu benar. Guardrail dan eval di repo digunakan untuk mengurangi failure mode yang diketahui, bukan sebagai jaminan keamanan absolut.
