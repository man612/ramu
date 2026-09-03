# Pilot Public Beta

Pilot dipakai untuk melihat apakah setup dan penggunaan Ramu benar-benar masuk akal di kondisi nyata. Fokusnya mencari friction dan failure mode, bukan membuktikan klaim besar tentang peningkatan nilai atau hasil belajar.

Pilot kecil 5–10 orang tetap berguna untuk menemukan masalah, tetapi bukan eksperimen terkontrol dan tidak mewakili seluruh populasi mahasiswa.

## Target awal

Mulai dari **5–10 mahasiswa yang cocok dengan pack yang sedang diuji**. Untuk baseline awal, targetnya adalah pengguna yang relevan dengan UT S1 Akuntansi 2026/2027.

Hal yang ingin diketahui:

- apakah satu Project bisa disiapkan tanpa kebingungan besar;
- seberapa cepat pengguna sampai pada manfaat pertama;
- langkah setup mana yang paling sering gagal;
- behavior tutor apa yang bermasalah di penggunaan nyata;
- apakah Project dipakai lagi dalam 7 hari;
- apakah setelah satu mata kuliah pengguna memilih menambah mata kuliah lain.

## Skenario minimum

Setiap peserta mencoba:

1. memasang **satu mata kuliah terlebih dahulu**;
2. menjalankan satu sesi memahami konsep yang belum dikuasai;
3. meminta pengecekan terhadap jawaban buatan sendiri;
4. memakai satu materi/screenshot/PDF yang memang mereka punya;
5. kembali ke Project yang sama pada hari berbeda bila masih relevan.

Mata kuliah lain baru ditambahkan setelah Project pertama benar-benar bisa dipakai.

## Data peserta tidak masuk repository

Jangan commit data individual seperti:

- nama, email, nomor mahasiswa, username, atau direct identifier lain;
- row per peserta;
- transcript/chat mentah;
- screenshot atau isi tugas/materi mentah;
- credential/token;
- feedback yang mudah mengidentifikasi seseorang.

Evidence publik cukup berupa **angka agregat, kategori failure, tema feedback yang sudah disanitasi, dan regression linkage**.

## Menyiapkan summary lokal

Gunakan tooling pilot tanpa API:

```bash
python scripts/pilot_evidence.py prepare \
  --pack id.ut.accounting-s1.2026-2027.s2 \
  --minimum 5 \
  --maximum 10 \
  --output evals/manual/results/pilot-summary.json
```

`evals/manual/results/` di-ignore Git agar draft tidak ikut terpublish.

Saat pilot dimulai:

```bash
python scripts/pilot_evidence.py finalize \
  evals/manual/results/pilot-summary.json \
  --start-now
```

Setelah count diperbarui:

```bash
python scripts/pilot_evidence.py finalize evals/manual/results/pilot-summary.json
python scripts/pilot_evidence.py validate evals/manual/results/pilot-summary.json
```

Saat pilot selesai:

```bash
python scripts/pilot_evidence.py finalize \
  evals/manual/results/pilot-summary.json \
  --complete-now
```

Tooling menghitung `metrics` dan `readiness` dari count. Field hasil perhitungan tersebut tidak perlu diedit manual.

## Data agregat yang dicatat

Summary menyimpan:

- `started` — peserta yang benar-benar mulai;
- `setup_completed` — berhasil menyiapkan satu Project;
- `first_value_reached` — sampai pada sesi yang dianggap memberi manfaat pertama;
- `return_7d_eligible` dan `returned_within_7d` — denominator/numerator penggunaan ulang;
- `multi_course_adopted` — memilih menambah mata kuliah;
- `setup_completed_without_live_help` — setup selesai tanpa maintainer mengambil alih;
- bucket **time-to-first-value**: `<5m`, `5–15m`, `15–30m`, `>30m`, atau unknown;
- kategori setup/behavior failure;
- tema feedback yang sudah disanitasi;
- regression `P001`, `P002`, dan seterusnya untuk masalah yang perlu ditindaklanjuti.

CI menolak data agregat yang secara logika tidak mungkin, misalnya `first_value_reached > setup_completed` atau jumlah bucket waktu yang tidak cocok dengan count first-value.

## Regression dari pilot

Masalah material dicatat sebagai regression agregat, bukan transcript.

Kategori yang tersedia antara lain:

- fabrication;
- source-selection;
- academic-integrity;
- prompt-injection;
- context-leak;
- over-answering;
- learner-state;
- setup.

Jika masalah bisa direproduksi, hubungkan ke behavior case `E..` yang sudah ada atau tambahkan case baru pada scope yang tepat.

Regression dengan `critical: true`, `reproducible: true`, dan status `open` membuat readiness menjadi **BLOCKED**.

## Arti readiness

Tooling memakai empat status:

- `INCOMPLETE` — pilot/protocol belum selesai;
- `INSUFFICIENT_SAMPLE` — pilot selesai tetapi jumlah peserta belum mencapai minimum;
- `BLOCKED` — ada critical regression yang reproducible dan masih terbuka;
- `REVIEW_READY` — summary cukup lengkap untuk direview manusia.

`REVIEW_READY` berarti evidence sudah cukup rapi untuk dibaca bersama evidence lain. Ia bukan bukti statistik atau keputusan release otomatis.

## Mempublikasikan summary

Setelah privacy review dan pengecekan angka, sanitized summary yang memang perlu menjadi evidence publik dapat disalin ke:

```text
evidence/pilots/*.json
```

CI akan memvalidasi schema dan invariant agregat. Lihat [`../evidence/pilots/README.md`](../evidence/pilots/README.md).

## Sebelum menaikkan status

Public beta belum berarti behavior sudah tervalidasi penuh. Sebelum mempertimbangkan status yang lebih tinggi, periksa minimal:

- static/schema/identity/site CI hijau;
- manual behavior case yang relevan sudah dijalankan dan direview;
- critical case tidak FAIL;
- pilot mencapai minimum yang dideklarasikan atau kekurangannya dijelaskan;
- critical failure pilot sudah diperbaiki/didokumentasikan dan masuk regression bila reproducible;
- pengguna baru dapat menyiapkan satu mata kuliah tanpa bantuan terus-menerus;
- source resmi masih aktif dan berada dalam interval review;
- tidak ada blocker lisensi, secret, atau materi berhak cipta di repository.

Automated API benchmark tetap menjadi QA tambahan, bukan pengganti manual Projects atau evidence penggunaan nyata.
