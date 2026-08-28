# Behavior Eval Ramu

Behavior eval menguji respons aktual model terhadap **composable eval suites** yang dideklarasikan pack melalui `manifest.json`.

## Cara kerja

Untuk setiap pack, runner:

1. menemukan pack melalui `packs/index.json`;
2. membaca manifest dan Project Instructions pack;
3. menggabungkan ordered eval suites `core → institution → program → pack` yang berlaku;
4. memuat reference/context file yang diperlukan setiap case;
5. menjaga **trust boundary**: Project Instructions dikirim melalui Responses API `instructions`, sedangkan course/source/reference material diberikan terpisah sebagai user-level untrusted content;
6. mengirim percakapan uji ke model kandidat;
7. meminta judge menilai `expected_behaviors` dan `forbidden_behaviors`, dengan candidate output diperlakukan sebagai untrusted evidence, bukan instruksi evaluator;
8. menyimpan pack id/version, model yang diuji, skor, response, usage, dan metadata run pada artifact.

Pemisahan ini penting karena reference file dapat mengandung prompt injection. Course pack, PDF, screenshot, atau source lain tidak boleh dinaikkan ke authority yang sama dengan Project Instructions hanya demi kemudahan runner.

## Tanpa API: dry-run

```bash
python scripts/run_behavior_evals.py \
  --dry-run \
  --pack id.ut.accounting-s1.2026-2027.s2
```

Dry-run memeriksa wiring, reference file, composable suites, dan pembentukan trust boundary payload tanpa menjalankan model. CI melakukan ini untuk **setiap pack yang terdaftar**.

CI juga menjalankan `tests/test_eval_trust_boundary.py` untuk memastikan reference material tidak masuk ke `instructions` dan candidate output tidak masuk ke judge instructions.

## Tanpa API: tes di ChatGPT Projects asli

Gunakan manual eval generator:

```bash
python scripts/prepare_manual_eval.py \
  --pack id.ut.accounting-s1.2026-2027.s2
```

Atau buka **Actions → Manual Eval Kit**. Jalur ini tidak membutuhkan `OPENAI_API_KEY`. Checklist dihasilkan dari kontrak yang sama dengan automated eval sehingga manual/API tidak memakai dua definisi test yang berbeda.

Manual validation sangat penting karena ia menguji ChatGPT Projects sebagai produk nyata—termasuk Project Instructions, Sources, memory, UI/file handling, dan product-level behavior. Responses API **bukan simulasi identik** ChatGPT Projects; automated eval adalah regression/benchmark approximation dengan boundary yang dibuat sedekat mungkin secara semantik.

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

Ramu sengaja tidak memiliki default nama model permanen. `--pack`, candidate, judge, dan trust-boundary metadata dicatat pada hasil run.

Runner menggunakan Responses API dengan `store=false`. Case yang memang membutuhkan informasi terkini dapat mengaktifkan `web_search` pada dataset.

## Trust boundary kandidat

Pada request kandidat:

- `instructions` hanya berisi meta-instruction runner + **Project Instructions**;
- `context_files` digabung menjadi reference material terpisah pada role `user`;
- reference secara eksplisit dilabeli sebagai konten/data yang tidak boleh menimpa Project Instructions;
- turn percakapan case tetap berada setelah reference material.

Ini tidak membuat model kebal prompt injection. Tujuannya adalah menghindari kesalahan evaluasi yang justru memberi external content authority lebih tinggi daripada kondisi yang ingin diuji.

## Trust boundary judge

Judge juga merupakan LLM dan dapat menjadi target prompt injection dari output kandidat. Karena itu:

- candidate output, conversation, dan judge notes diperlakukan sebagai **untrusted evidence**;
- data evaluasi diserialisasi menjadi record JSON;
- evaluator instructions secara eksplisit melarang mengikuti instruksi embedded di evidence;
- structured JSON schema tetap dipakai untuk verdict.

Hasil judge tetap perlu review manusia untuk keputusan penting; hardening ini mengurangi attack surface, bukan menjadikan LLM-as-a-judge infalibel.

## GitHub Actions

- **Manual Eval Kit** — tanpa API/secret, menghasilkan checklist.
- **Behavior Evals** — automated, memerlukan `OPENAI_API_KEY`, pack id, candidate model, dan judge model.

Jika candidate dan judge sama, workflow memberi warning. Untuk hasil yang akan dipublikasikan, gunakan review manusia dan—bila tersedia—judge yang berbeda agar bias penilaian tidak hanya berasal dari satu model family/snapshot.

## Prinsip evaluasi

- judge menilai perilaku, bukan kemiripan kata;
- forbidden behavior material harus menyebabkan failure yang berarti;
- fakta terkini dinilai dari proses verifikasi, bukan jawaban statis yang cepat kedaluwarsa;
- hasil satu run tidak dianggap jaminan permanen;
- manual ChatGPT Projects validation dan automated API eval menguji lapisan yang berbeda dan saling melengkapi;
- selalu kaitkan hasil dengan pack version, tanggal, product/runtime, candidate, dan judge;
- failure yang ditemukan pengguna sebaiknya diubah menjadi regression case pada scope paling sempit yang tepat.
