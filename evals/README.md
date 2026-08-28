# Evals

Ramu memisahkan **scope evaluasi** dan **cara menjalankannya**.

## Scope eval

### Core eval

`evals/core/` berisi failure mode yang harus masuk akal lintas institusi/program, misalnya:

- data/screenshot tidak lengkap;
- referensi/DOI palsu;
- precedence rubrik;
- integritas tugas;
- retrieval practice;
- learner state;
- source freshness;
- prompt injection dari Project Source;
- konflik versi course pack.

### Pack eval

Setiap pack dapat memiliki `<pack>/evals/` untuk skenario yang bergantung pada institusi, program, semester, atau mata kuliah tertentu. Contoh UT S1 Akuntansi Semester 2: aturan pajak yang berubah, jurnal AKM I, konflik source pusat/regional, dan context isolation antarmata kuliah.

`manifest.json` menunjuk lokasi core + pack contract/behavior. `scripts/run_behavior_evals.py` menggabungkannya saat runtime. ID case harus unik setelah kedua scope digabung.

## Tiga jalur pemeriksaan

1. **Static validation** — gratis/deterministik; memeriksa manifest, source registry, contract marker, file, dan wiring.
2. **Manual behavior validation** — gratis; case dijalankan manusia langsung di ChatGPT Projects.
3. **Automated API behavior eval** — opsional; model kandidat dijalankan via API dan respons dinilai judge model.

Tidak memiliki API tidak membuat Ramu gagal atau tidak dapat dipakai. API hanya menambah automation/reproducibility pada satu lapisan QA.

## Pemeriksaan tanpa API

```bash
python scripts/validate_repo.py
python scripts/run_behavior_evals.py --dry-run --pack id.ut.accounting-s1.2026-2027.s2
python scripts/check_source_freshness.py
```

CI mengambil seluruh pack dari `packs/index.json` dan menjalankan dry-run per pack melalui matrix.

## Manual validation di ChatGPT Projects

```bash
python scripts/prepare_manual_eval.py \
  --pack id.ut.accounting-s1.2026-2027.s2
```

Atau buka **Actions → Manual Eval Kit**. Workflow itu tidak membutuhkan secret/API dan menghasilkan checklist sebagai artifact.

Panduan: [`manual/README.md`](manual/README.md).

## Automated behavior eval — opsional

```bash
export OPENAI_API_KEY="..."
python scripts/run_behavior_evals.py \
  --pack id.ut.accounting-s1.2026-2027.s2 \
  --candidate-model <candidate> \
  --grader-model <judge>
```

Runner akan memuat manifest pack, Project Instructions, core + pack eval/context, menjalankan kandidat, meminta judge structured verdict, lalu menyimpan summary/artifact ke `evals/results/`.

Workflow **Behavior Evals** sengaja manual agar API tidak terpakai pada setiap push. Satu run probabilistik bukan bukti permanen; hasil penting perlu direview manusia dan dikaitkan dengan pack version + tanggal + model yang benar-benar diuji.
