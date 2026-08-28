# Behavior Eval Ramu

Behavior eval menguji respons aktual model terhadap gabungan **core eval + pack eval** yang dideklarasikan di `manifest.json`.

## Cara kerja

Untuk setiap pack, runner:

1. menemukan pack melalui `packs/index.json`;
2. membaca manifest dan Project Instructions pack;
3. menggabungkan core contract/behavior dengan contract/behavior khusus pack;
4. memuat context yang diperlukan setiap case;
5. mengirim percakapan uji ke model kandidat;
6. meminta judge menilai `expected_behaviors` dan `forbidden_behaviors`;
7. menyimpan pack id/version, model yang diuji, skor, response, dan usage pada artifact.

## Tanpa API: dry-run

```bash
python scripts/run_behavior_evals.py \
  --dry-run \
  --pack id.ut.accounting-s1.2026-2027.s2
```

Dry-run memeriksa wiring dan context tanpa menjalankan model. CI melakukan ini untuk **setiap pack yang terdaftar**.

## Tanpa API: tes di ChatGPT Projects asli

Gunakan manual eval generator:

```bash
python scripts/prepare_manual_eval.py \
  --pack id.ut.accounting-s1.2026-2027.s2
```

Atau buka **Actions → Manual Eval Kit**. Jalur ini tidak membutuhkan `OPENAI_API_KEY`. Checklist dihasilkan dari kontrak yang sama dengan automated eval sehingga manual/API tidak memakai dua definisi test yang berbeda.

Manual validation sangat berguna karena ia menguji ChatGPT Projects sebagai produk nyata—termasuk Project Instructions, Sources, dan product behavior—yang tidak identik 100% dengan Responses API.

## Dengan OpenAI API — opsional

Jika API tersedia:

```bash
python scripts/run_behavior_evals.py \
  --pack id.ut.accounting-s1.2026-2027.s2 \
  --candidate-model <model-kandidat-yang-tersedia> \
  --grader-model <model-judge-yang-tersedia> \
  --fail-under 0.80
```

Subset case:

```bash
python scripts/run_behavior_evals.py \
  --pack id.ut.accounting-s1.2026-2027.s2 \
  --candidate-model <candidate> \
  --grader-model <judge> \
  --only E01,E05,E13
```

Ramu sengaja tidak memiliki default nama model permanen. `--pack`, candidate, dan judge dicatat pada hasil run.

Runner menggunakan Responses API dengan `store=false`. Case yang memang membutuhkan informasi terkini dapat mengaktifkan `web_search` pada dataset.

## GitHub Actions

- **Manual Eval Kit** — tanpa API/secret, menghasilkan checklist.
- **Behavior Evals** — automated, memerlukan `OPENAI_API_KEY`, pack id, candidate model, dan judge model.

Jika candidate dan judge sama, workflow memberi warning. Untuk hasil yang akan dipublikasikan, gunakan review manusia dan—bila tersedia—judge yang berbeda agar bias penilaian tidak hanya berasal dari satu model family/snapshot.

## Prinsip evaluasi

- judge menilai perilaku, bukan kemiripan kata;
- forbidden behavior material harus menyebabkan failure yang berarti;
- fakta terkini dinilai dari proses verifikasi, bukan jawaban statis yang cepat kedaluwarsa;
- hasil satu run tidak dianggap jaminan permanen;
- selalu kaitkan hasil dengan pack version, tanggal, product/runtime, candidate, dan judge;
- failure yang ditemukan pengguna sebaiknya diubah menjadi regression case pada scope paling sempit yang tepat: core jika universal, pack jika kontekstual.
