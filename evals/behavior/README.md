# Behavior Eval Ramu

Folder ini berisi skenario yang benar-benar dikirim ke model. Berbeda dari `evals/cases/semester-02.json`, yang berfungsi sebagai kontrak perilaku dan regression marker, behavior eval menguji respons aktual model.

## Cara kerja

Untuk setiap kasus:

1. runner memuat `PROJECT-INSTRUCTIONS.md`;
2. runner menambahkan protocol/course context yang ditentukan oleh kasus;
3. model kandidat menerima percakapan uji;
4. model judge menilai respons berdasarkan `expected_behaviors` dan `forbidden_behaviors` dari contract eval;
5. kasus dinyatakan lulus jika judge memberi `pass=true` dan skor memenuhi `min_score`;
6. seluruh run lulus jika pass rate memenuhi `--fail-under`.

Respons kandidat dan hasil judge disimpan sebagai artifact JSON agar regresi bisa diaudit. Artifact tidak dikomit ke repo.

## Menjalankan tanpa API

```bash
python scripts/run_behavior_evals.py --dry-run
```

Dry-run memeriksa bahwa semua behavior case memiliki skenario, context file tersedia, dan hubungan dengan contract eval valid. Dry-run tidak membuktikan kualitas respons model.

## Menjalankan dengan OpenAI API

Set environment variable `OPENAI_API_KEY`, lalu pilih model kandidat dan judge secara eksplisit:

```bash
python scripts/run_behavior_evals.py \
  --candidate-model <model-kandidat-yang-tersedia-saat-ini> \
  --grader-model <model-judge-yang-tersedia-saat-ini> \
  --fail-under 0.80
```

Contoh menjalankan beberapa kasus saja:

```bash
python scripts/run_behavior_evals.py \
  --candidate-model <candidate> \
  --grader-model <judge> \
  --only E01,E05,E08
```

Ramu sengaja tidak memiliki default nama model permanen. Katalog model API dan model yang tersedia pada paket ChatGPT dapat berubah tanpa mengubah kontrak belajar Ramu.

Runner memakai Responses API dengan `store=false`. Kasus yang membutuhkan pemeriksaan informasi terkini dapat mengaktifkan built-in `web_search` secara eksplisit pada dataset.

## GitHub Actions

Workflow **Behavior Evals** hanya berjalan manual agar API tidak terpakai setiap push. Tambahkan repository secret bernama `OPENAI_API_KEY`, buka **Actions → Behavior Evals → Run workflow**, lalu isi model kandidat, model judge, case, dan pass rate.

Jika candidate dan judge memakai model yang sama, workflow tetap dapat dijalankan tetapi menghasilkan warning. Untuk hasil yang akan dipakai sebagai bukti public validation, lebih baik gunakan judge berbeda dan review sebagian hasil secara manual.

Default pass rate adalah 80%. Nilai ini adalah gate awal, bukan klaim bahwa 80% otomatis cukup untuk status stabil atau tervalidasi penuh.

## Prinsip evaluasi

- judge menilai perilaku, bukan sekadar kemiripan kata;
- `forbidden_behaviors` yang material harus menurunkan nilai secara signifikan;
- kasus yang berubah karena informasi terkini harus menilai proses verifikasi, bukan mengunci jawaban faktual yang cepat kedaluwarsa;
- hasil satu run tidak dianggap bukti permanen karena output model bersifat probabilistik;
- untuk benchmark yang akan dipublikasikan, ulangi run beberapa kali dan review sampel secara manual;
- perubahan Project Instructions/protocol sebaiknya dibandingkan dengan baseline run sebelumnya;
- selalu catat model kandidat/judge yang benar-benar digunakan pada run tersebut.
