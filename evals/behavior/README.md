# Behavior Eval Ramu

Folder ini berisi skenario yang benar-benar dikirim ke model. Berbeda dari `evals/cases/semester-02.json`, yang berfungsi sebagai kontrak perilaku dan regression marker, behavior eval menguji respons aktual model.

## Cara kerja

Untuk setiap kasus:

1. runner memuat `PROJECT-INSTRUCTIONS.md`;
2. runner menambahkan protocol/course context yang ditentukan oleh kasus;
3. model kandidat menerima percakapan uji;
4. model judge terpisah menilai respons berdasarkan `expected_behaviors` dan `forbidden_behaviors` dari contract eval;
5. kasus dinyatakan lulus jika judge memberi `pass=true` dan skor memenuhi `min_score`;
6. seluruh run lulus jika pass rate memenuhi `--fail-under`.

Respons kandidat dan hasil judge disimpan sebagai artifact JSON agar regresi bisa diaudit. Artifact tidak dikomit ke repo.

## Menjalankan tanpa API

```bash
python scripts/run_behavior_evals.py --dry-run
```

Dry-run memeriksa bahwa semua E01–E12 memiliki skenario behavior, context file tersedia, dan hubungan dengan contract eval valid.

## Menjalankan dengan OpenAI API

Set environment variable `OPENAI_API_KEY`, lalu:

```bash
python scripts/run_behavior_evals.py
```

Contoh menjalankan beberapa kasus saja:

```bash
python scripts/run_behavior_evals.py --only E01,E05,E08
```

Model dapat diganti tanpa mengubah dataset:

```bash
python scripts/run_behavior_evals.py \
  --candidate-model gpt-5-mini \
  --grader-model gpt-5-mini \
  --fail-under 0.80
```

Runner memakai Responses API dengan `store=false`. Kasus yang memang membutuhkan pemeriksaan informasi terkini dapat mengaktifkan built-in `web_search` secara eksplisit pada dataset.

## GitHub Actions

Workflow **Behavior Evals** hanya berjalan manual agar API tidak terpakai setiap push. Tambahkan repository secret bernama `OPENAI_API_KEY`, buka tab **Actions → Behavior Evals → Run workflow**, lalu pilih model/case yang ingin diuji.

Default pass rate adalah 80%. Nilai ini sengaja menjadi gate awal, bukan klaim bahwa 80% sudah cukup untuk status `Terverifikasi penuh`. Status tersebut tetap memerlukan review kualitas hasil dan kestabilan lintas beberapa run/model snapshot.

## Prinsip evaluasi

- judge menilai perilaku, bukan sekadar kemiripan kata;
- `forbidden_behaviors` yang material harus menurunkan nilai secara signifikan;
- kasus yang berubah karena informasi terkini harus tetap menilai proses verifikasi, bukan mengunci jawaban faktual yang cepat kedaluwarsa;
- hasil satu run tidak dianggap bukti permanen karena output model bersifat probabilistik;
- perubahan Project Instructions/protocol sebaiknya dibandingkan dengan baseline run sebelumnya.
