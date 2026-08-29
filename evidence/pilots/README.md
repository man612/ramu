# Published Pilot Evidence

Folder ini hanya untuk **ringkasan agregat pilot yang sudah disanitasi** dan memang sengaja dipublish sebagai evidence repository.

Jangan commit:

- nama, email, username, nomor mahasiswa, atau identifier peserta lain;
- baris data per peserta;
- transcript/chat mentah;
- screenshot atau isi tugas/materi kuliah mentah;
- credential, token, API key, atau data akun;
- kutipan feedback yang dapat mengidentifikasi peserta.

Draft kerja sebaiknya dibuat di lokasi lokal yang di-ignore Git, misalnya:

```bash
python scripts/pilot_evidence.py prepare \
  --pack id.ut.accounting-s1.2026-2027.s2 \
  --minimum 5 \
  --maximum 10 \
  --output evals/manual/results/pilot-summary.json
```

Setelah agregat diisi, hitung ulang metrik/readiness dan validasi:

```bash
python scripts/pilot_evidence.py finalize evals/manual/results/pilot-summary.json
python scripts/pilot_evidence.py validate evals/manual/results/pilot-summary.json
```

Kalau pilot sudah selesai:

```bash
python scripts/pilot_evidence.py finalize \
  evals/manual/results/pilot-summary.json \
  --complete-now
```

Hanya setelah privacy check, angka, kategori failure, feedback theme, dan regression linkage direview manusia, salin summary yang memang ingin dipublish ke folder ini lewat PR.

CI akan menjalankan JSON Schema validation dan `python scripts/pilot_evidence.py validate-published` terhadap setiap `*.json` di folder ini.

## Arti readiness

- `INCOMPLETE` — pilot atau protocol metadata belum lengkap;
- `INSUFFICIENT_SAMPLE` — pilot selesai tetapi jumlah peserta yang mulai belum mencapai minimum yang dideklarasikan;
- `BLOCKED` — ada regression critical yang reproducible dan masih open;
- `REVIEW_READY` — evidence agregat cukup lengkap untuk review maintainer.

`REVIEW_READY` **bukan** sinonim `PASS`, `stable`, statistically representative, atau bukti bahwa Ramu meningkatkan hasil belajar. Keputusan status pack/release tetap membutuhkan review manusia dan harus dibaca bersama manual behavior evidence, source freshness, serta limitation yang tercatat.
