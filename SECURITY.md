# Security Policy

Ramu berjalan sebagai konfigurasi dan tooling di atas layanan AI pihak ketiga. Tidak ada server aplikasi atau akun mahasiswa yang dikelola repository ini, tetapi risiko tetap ada pada prompt, source, file, workflow, dan tooling evaluasi.

## Versi yang didukung

Perbaikan keamanan diprioritaskan untuk **current `main`** dan **public-beta release terbaru**. Tag beta lama dipertahankan sebagai snapshot dan tidak selalu menerima backport.

Jika masalah hanya muncul pada release lama, cek dulu apakah masih dapat direproduksi pada versi terbaru.

## Yang termasuk isu keamanan

Contohnya:

- prompt injection dari source/course material yang dapat mengubah guardrail;
- source poisoning atau routing yang membuat sumber tidak tepercaya dianggap resmi;
- API key/secret bocor lewat workflow, artifact, log, atau contoh konfigurasi;
- file atau instruksi yang menyebabkan data pribadi/sensitif tersalin ke output publik;
- tooling yang membuat eval terlihat lulus padahal gate sebenarnya tidak dijalankan.

## Pelaporan

Masalah tanpa detail sensitif dapat dilaporkan lewat GitHub Issue dengan reproduksi minimal dan dampaknya.

Untuk kerentanan yang memerlukan detail sensitif, gunakan GitHub private vulnerability reporting / Security Advisory bila tersedia. Jangan menaruh API key, token, data pribadi, materi kuliah privat, atau exploit yang belum diperbaiki di issue publik.

## Batas keamanan

Guardrail dan eval membantu mengurangi failure mode yang sudah diketahui, tetapi tidak bisa menjamin perilaku model pihak ketiga, uptime layanan, kebijakan privasi platform, atau akurasi setiap jawaban AI. Klaim keamanan sebaiknya selalu dibaca dalam batas tersebut.
