# Ramu Starter

Ramu Starter adalah jalur paling ringan untuk memakai pola Ramu pada **mata kuliah apa pun** tanpa membuat public pack, mempelajari schema repository, atau memakai OpenAI API.

Starter sengaja dipisahkan dari `packs/`:

- **Starter** adalah workspace personal berdasarkan konteks yang diberikan pengguna;
- **public/community pack** adalah artefak repository yang punya identity stabil, source registry, manifest, dan validation contract sendiri.

Pemisahan ini penting supaya onboarding yang mudah tidak mengubah source yang belum diverifikasi menjadi seolah-olah maintained pack.

## Membuat Starter

Contoh non-interaktif:

```bash
python scripts/create_starter.py \
  --course "Statistika Bisnis" \
  --institution "Kampus Contoh" \
  --period "Semester 2" \
  --goal "Memahami probabilitas dan distribusi" \
  --source "Syllabus dosen" \
  --source "Buku utama kelas" \
  --rule "Tugas akhir tidak boleh dibuat penuh oleh AI"
```

Bila `--course` tidak diberikan dan command dijalankan dari terminal interaktif, generator akan menanyakannya. Opsi lain boleh kosong dan ditambahkan nanti.

Secara default output dibuat di `./ramu-starter-<nama-mata-kuliah>/`. Gunakan `--output <folder>` untuk menentukan lokasi lain.

## Artefak yang dihasilkan

- `PROJECT-INSTRUCTIONS.md` — behavior contract generik Ramu untuk satu mata kuliah;
- `COURSE-PACK.txt` — konteks personal yang bisa langsung diunggah ke Project Sources;
- `START-HERE.md` — langkah setup singkat;
- `starter.json` — metadata lokal agar isi Starter dapat dibaca tooling lain tanpa menebak isi teks.

Generator tidak mengunggah file, memanggil model AI, membuat ChatGPT Project secara otomatis, atau mendaftarkan hasil ke katalog publik.

## Batas kepercayaan

`starter.json` selalu ditulis dengan `public_pack: false` dan `source_verified: false`. Source/file yang disebut pengguna adalah **input pengguna**, bukan source yang sudah diperiksa maintainer Ramu.

Jika suatu Starter ternyata berguna lintas pengguna dan ingin dijadikan community pack, gunakan jalur [`Create a Pack`](../docs/CREATE-A-PACK.md). Jangan memindahkan file Starter langsung ke `packs/` lalu menaikkan statusnya tanpa source review dan validation yang sesuai.

## Privasi

Starter boleh tetap lokal. Jangan commit credential, data pribadi yang tidak perlu, transcript privat, rubrik/tugas yang tidak boleh dipublikasikan, atau materi kuliah berhak cipta ke repository publik.
