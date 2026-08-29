# Ramu v0.2.2-beta — Public Readiness & Security

`v0.2.2-beta` adalah patch release setelah `v0.2.1-beta` yang menutup fase public-readiness Ramu. Fokus release ini adalah repository hygiene, jalur bantuan publik, contributor safety, dokumentasi yang tahan perubahan UI, dan hardening konfigurasi GitHub sebelum Ramu dibuka lebih luas sebagai Public Beta.

Release ini tidak mengubah data akademik, course pack, behavior contract, critical eval, atau arsitektur multi-pack.

## Yang berubah

### Public support dan contribution flow

- Tambah `SUPPORT.md` sebagai jalur bantuan publik.
- Tambah issue form **Minta pack baru** untuk usulan periode, program, atau institusi baru.
- Issue chooser diarahkan ke setup guide, support, dan security policy yang sesuai.
- Pull request template disinkronkan dengan validation stack dan dry-run pack yang terdampak.

### Repository hygiene

- `.gitignore` diperluas untuk local `.env`, virtual environment, Python cache, metadata editor/OS, dan log.
- Dokumentasi setup tidak lagi bergantung pada label UI ChatGPT tertentu seperti `Add from library`.
- Wording pack README dibuat device-neutral.
- Aset setup lama yang tidak lagi dipakai dihapus.
- Histori release, changelog, release process, dan snapshot release notes disinkronkan.

### Public site metadata

- Homepage dan setup page mendapat canonical URL serta Open Graph metadata dasar.
- Jalur dukungan publik ditampilkan dari site.
- Site validator menjaga metadata dan support surface agar tidak hilang diam-diam pada refactor berikutnya.

### Security posture repository

Pada saat release ini disiapkan, repository juga menggunakan hardening GitHub berikut:

- `main` dilindungi ruleset aktif;
- perubahan ke `main` wajib lewat pull request;
- required check `validate` wajib hijau dan branch wajib up-to-date;
- force push dan branch deletion diblok;
- review conversation wajib resolved sebelum merge;
- CodeQL default setup aktif untuk GitHub Actions, JavaScript/TypeScript, dan Python;
- ruleset mewajibkan hasil CodeQL dengan threshold security `High or higher` dan standard alert `Errors`;
- Dependency Graph dan Dependabot aktif;
- secret protection dan push protection aktif;
- private vulnerability reporting diaktifkan;
- merged head branches otomatis dihapus;
- Wiki dan GitHub Projects yang tidak digunakan dimatikan.

Konfigurasi GitHub adalah state repository saat publikasi dan bukan bagian dari source tree yang ditag.

## Validation

Sebelum tag dibuat, release candidate harus memenuhi:

- `Validate Ramu` sukses pada commit target;
- downstream `Deploy Pages` sukses pada SHA yang sama;
- CodeQL analysis sukses pada bahasa yang terdeteksi;
- tidak ada perubahan data akademik atau behavior contract yang tidak tercatat.

## Status

Ramu tetap **Public Beta**.

Release ini tidak mengklaim bahwa:

- full manual E01–E16 di ChatGPT Projects sudah selesai;
- pilot nyata 5–10 mahasiswa sudah selesai;
- automated OpenAI API benchmark sudah dijalankan;
- semua output AI selalu benar;
- Ramu sudah berstatus stable atau fully validated.

Manual validation, pilot evidence, dan optional API benchmark tetap dilacak terpisah pada backlog evidence publik.

OpenAI API tetap tidak diperlukan untuk memakai Ramu.
