# Pilot Public Beta Ramu

Dokumen ini dipakai untuk menguji apakah Ramu benar-benar dapat dipasang dan digunakan mahasiswa dalam kondisi nyata, bukan hanya terlihat rapi di repository.

Pilot adalah **field evidence kecil untuk menemukan friction dan failure mode**. Pilot 5–10 orang bukan eksperimen terkontrol dan tidak boleh dipakai sendirian untuk mengklaim Ramu meningkatkan nilai, hasil belajar, atau mewakili seluruh populasi mahasiswa.

## Target awal

Mulai dari **5–10 mahasiswa yang benar-benar cocok dengan pack yang diuji**. Untuk pack awal berarti mahasiswa yang relevan dengan Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027.

Tujuannya bukan mengejar star GitHub, melainkan mengetahui:

- apakah pengguna dapat mengaktifkan satu Project;
- seberapa cepat mereka mencapai manfaat pertama;
- langkah setup mana yang gagal atau membingungkan;
- failure mode tutor yang muncul di penggunaan nyata;
- apakah mereka kembali dalam 7 hari;
- apakah setelah satu mata kuliah mereka memilih memasang mata kuliah lain.

## Skenario minimum

Setiap peserta diminta:

1. memasang **satu mata kuliah terlebih dahulu**, bukan seluruh pack;
2. menjalankan satu sesi memahami konsep yang belum dikuasai;
3. meminta Ramu mengecek jawaban buatan sendiri;
4. memakai satu materi/screenshot/PDF yang memang mereka punya;
5. kembali memakai Project yang sama pada hari berbeda bila masih relevan.

Setelah satu Project berhasil dan manfaatnya terasa, baru tawarkan setup mata kuliah lain.

## Jangan simpan dataset peserta di repository

Individual chat dan data peserta bukan artifact publik Ramu. Jangan commit:

- nama, email, nomor mahasiswa, username, atau direct identifier lain;
- row per peserta;
- transcript/chat mentah;
- screenshot atau isi tugas/materi mentah;
- credential/token;
- kutipan feedback yang mudah mengidentifikasi seseorang.

Yang boleh menjadi evidence repository hanyalah **angka agregat, kategori failure, tema feedback yang sudah disanitasi, dan regression linkage**.

## Membuat summary lokal

Gunakan tooling pilot tanpa API:

```bash
python scripts/pilot_evidence.py prepare \
  --pack id.ut.accounting-s1.2026-2027.s2 \
  --minimum 5 \
  --maximum 10 \
  --output evals/manual/results/pilot-summary.json
```

`evals/manual/results/` di-ignore Git sehingga draft tidak sengaja terpublish.

Saat pilot dimulai:

```bash
python scripts/pilot_evidence.py finalize \
  evals/manual/results/pilot-summary.json \
  --start-now
```

Setelah angka agregat diubah, jalankan lagi:

```bash
python scripts/pilot_evidence.py finalize evals/manual/results/pilot-summary.json
python scripts/pilot_evidence.py validate evals/manual/results/pilot-summary.json
```

Saat periode pilot benar-benar selesai:

```bash
python scripts/pilot_evidence.py finalize \
  evals/manual/results/pilot-summary.json \
  --complete-now
```

Tooling menghitung metrik dan readiness dari count yang dicatat; jangan mengedit nilai `metrics` atau `readiness` secara manual.

## Data agregat yang dicatat

Summary menyimpan funnel dan metrik proses berikut:

- `started` — peserta yang benar-benar mulai mencoba;
- `setup_completed` — berhasil setup satu Project;
- `first_value_reached` — berhasil mencapai sesi yang dianggap memberi manfaat pertama;
- `return_7d_eligible` dan `returned_within_7d` — denominator/numerator return use;
- `multi_course_adopted` — memilih memasang mata kuliah tambahan;
- `setup_completed_without_live_help` — setup selesai tanpa maintainer mengambil alih proses;
- bucket **time-to-first-value**: `<5m`, `5–15m`, `15–30m`, `>30m`, atau unknown;
- aggregate setup/behavior failure category;
- sanitized feedback theme;
- regression `P001`, `P002`, ... untuk failure yang perlu ditindaklanjuti.

Rate dihitung tooling dari count tersebut. CI juga menolak funnel mustahil seperti `first_value_reached > setup_completed` atau jumlah bucket waktu yang tidak sama dengan jumlah first-value.

## Regression dari pilot

Failure yang material ditulis sebagai regression agregat, bukan transcript. Contoh kategori:

- fabrication;
- source-selection;
- academic-integrity;
- prompt-injection;
- context-leak;
- over-answering;
- learner-state;
- setup.

Jika dapat direproduksi, hubungkan ke behavior case `E..` yang sudah ada atau buat eval regression baru pada scope paling tepat.

Regression yang `critical: true`, `reproducible: true`, dan masih `open` membuat readiness pilot menjadi **BLOCKED**.

## Arti readiness

Tooling hanya memiliki empat status:

- `INCOMPLETE` — pilot/protocol belum selesai;
- `INSUFFICIENT_SAMPLE` — pilot selesai tetapi peserta yang mulai belum mencapai minimum yang dideklarasikan;
- `BLOCKED` — ada reproducible critical regression yang masih terbuka;
- `REVIEW_READY` — summary cukup lengkap untuk review manusia.

Tidak ada status `PASS`, `STABLE`, atau `VALIDATED` otomatis dari pilot.

`REVIEW_READY` berarti evidence cukup untuk dibaca bersama evidence lain. Ia **bukan** bukti statistik, bukan causal claim, dan bukan keputusan release otomatis.

## Publish summary bila memang perlu

Setelah privacy review dan review angka dilakukan manusia, sanitized summary yang ingin menjadi evidence publik dapat disalin ke:

```text
evidence/pilots/*.json
```

CI akan memvalidasi schema serta invariant agregat setiap summary yang dipublish. Lihat [`../evidence/pilots/README.md`](../evidence/pilots/README.md).

## Kriteria sebelum mempertimbangkan status lebih tinggi

Public beta tidak sama dengan tervalidasi penuh. Sebelum status pack/release yang lebih tinggi dipertimbangkan, minimal:

- static/schema/identity/site CI hijau;
- full manual E01–E16 di ChatGPT Projects sudah dijalankan dan direview;
- critical manual behavior case tidak FAIL;
- pilot mencapai minimum yang dideklarasikan atau kekurangannya dijelaskan eksplisit;
- critical failure dari pilot sudah diperbaiki/didokumentasikan dan, bila reproducible, masuk regression eval;
- setup satu mata kuliah dapat diselesaikan pengguna baru tanpa bantuan maintainer terus-menerus;
- source resmi aktif dan claim produk masih dalam interval review;
- tidak ada blocker lisensi, secret, atau materi berhak cipta di repo.

Automated API benchmark tetap QA tambahan opsional dan bukan pengganti manual Projects + field evidence.
