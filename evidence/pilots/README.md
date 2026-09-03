# Published Pilot Evidence

Folder ini untuk **ringkasan agregat pilot yang sudah disanitasi** dan memang perlu disimpan sebagai evidence publik.

Jangan commit:

- nama, email, username, nomor mahasiswa, atau identifier peserta lain;
- data per peserta;
- transcript/chat mentah;
- screenshot atau isi tugas/materi kuliah mentah;
- credential, token, API key, atau data akun;
- kutipan feedback yang masih dapat mengidentifikasi seseorang.

Draft kerja sebaiknya tetap lokal di path yang di-ignore Git, misalnya:

```bash
python scripts/pilot_evidence.py prepare \
  --pack id.ut.accounting-s1.2026-2027.s3 \
  --minimum 5 \
  --maximum 10 \
  --output evals/manual/results/pilot-summary.json
```

Setelah data agregat diisi:

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

Summary baru dipindahkan ke folder ini setelah privacy check, angka, kategori failure, tema feedback, dan regression linkage sudah direview.

CI menjalankan JSON Schema validation dan `python scripts/pilot_evidence.py validate-published` untuk setiap `*.json` yang dipublish di sini.

## Readiness

- `INCOMPLETE` — pilot atau metadata protocol belum lengkap;
- `INSUFFICIENT_SAMPLE` — pilot selesai tetapi jumlah peserta belum mencapai minimum;
- `BLOCKED` — ada critical regression yang reproducible dan masih terbuka;
- `REVIEW_READY` — evidence agregat cukup lengkap untuk dibaca dan dinilai.

`REVIEW_READY` bukan sinonim PASS, stabil, representatif secara statistik, atau bukti peningkatan hasil belajar. Status pack/release tetap perlu dibaca bersama manual behavior evidence, source freshness, dan limitation yang tercatat.
