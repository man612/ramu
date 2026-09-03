# Evals

Eval di repository dibagi berdasarkan **scope**, lalu dirakit sesuai manifest pack yang sedang diuji.

## Composable eval suites

Setiap `manifest.json` mendeklarasikan `eval_suites` dari aturan paling umum ke paling spesifik:

1. `core` — failure mode yang masuk akal untuk semua pack;
2. `institution` — aturan yang berlaku lintas pack pada satu institusi;
3. `program` — aturan lintas periode dalam satu program studi;
4. `pack` — skenario yang membutuhkan konteks periode atau mata kuliah tertentu.

Urutan dasarnya:

```text
core → institution → program → pack
```

Scope yang tidak dibutuhkan boleh dilewati.

Contoh Semester 3 UT S1 Akuntansi:

```json
"eval_suites": [
  {
    "id": "core",
    "scope": "core",
    "contracts": "evals/core/contracts.json",
    "behavior": "evals/core/behavior.json"
  },
  {
    "id": "ut",
    "scope": "institution",
    "scope_ref": "universitas-terbuka",
    "contracts": "packs/universitas-terbuka/evals/contracts.json",
    "behavior": "packs/universitas-terbuka/evals/behavior.json"
  },
  {
    "id": "semester-03",
    "scope": "pack",
    "scope_ref": "id.ut.accounting-s1.2026-2027.s3",
    "contracts": "packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-03/evals/contracts.json",
    "behavior": "packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-03/evals/behavior.json"
  }
]
```

Validator memastikan `core` berada di awal dan `pack` di akhir. `suite_id`, `scope`, dan `scope_ref` pada contracts/behavior juga harus cocok dengan manifest.

ID case tetap **unik setelah seluruh suite digabung**. Suite yang lebih spesifik tidak boleh diam-diam mengganti case milik scope sebelumnya. `defaults` pada behavior boleh dioverride secara berurutan untuk nilai runtime seperti `min_score` atau `max_output_tokens`.

## Scope yang aktif

### Core

`evals/core/` memuat failure mode lintas institusi, antara lain:

- data/screenshot tidak lengkap;
- referensi atau DOI palsu;
- precedence rubrik;
- academic integrity;
- retrieval practice;
- learner state;
- source freshness;
- prompt injection dari Project Source;
- konflik versi course pack.

### Universitas Terbuka

`packs/universitas-terbuka/evals/` berisi aturan yang memang khas UT dan dapat dipakai lebih dari satu periode. E14, misalnya, menguji konflik source pusat vs regional.

### Semester 2

`semester-02/evals/` menyimpan skenario yang membutuhkan konteks pack Semester 2, seperti aturan pajak vs BMP dan jurnal AKM I.

### Semester 3

`semester-03/evals/` menambahkan E17–E24 untuk tax-currentness, metadata lama vs current AKM II, continuity kasus PRATON, SIA requirement/control, relevant cost, business evidence, language tutoring, dan ketidakpastian isi kebijakan GenAI UT.

Jika suatu hari ada failure mode lintas semester yang hanya berlaku pada S1 Akuntansi, scope `program` dapat ditempatkan antara `institution` dan `pack`.

## Tiga jalur pemeriksaan

1. **Static validation** — deterministik; memeriksa manifest, source registry, contract marker, suite metadata, file, dan wiring.
2. **Manual behavior validation** — case dijalankan langsung di ChatGPT Projects.
3. **Automated API behavior eval** — opsional; kandidat dijalankan via API lalu dinilai judge model.

API hanya menambah satu lapisan automation. Penggunaan normal, static CI, dan manual validation tetap berjalan tanpa API.

## Pemeriksaan tanpa API

```bash
python scripts/validate_repo.py
python scripts/run_behavior_evals.py --dry-run --pack id.ut.accounting-s1.2026-2027.s3
python scripts/check_source_freshness.py
```

CI mengambil semua pack dari `packs/index.json` dan membuat matrix dry-run otomatis.

## Manual validation di ChatGPT Projects

```bash
python scripts/prepare_manual_eval.py \
  --pack id.ut.accounting-s1.2026-2027.s3
```

Atau buka **Actions → Manual Eval Kit**. Workflow tersebut tidak memerlukan secret/API dan menghasilkan checklist dari merged suite.

Panduan lengkap: [`manual/README.md`](manual/README.md).

## Automated behavior eval

```bash
export OPENAI_API_KEY="..."
python scripts/run_behavior_evals.py \
  --pack id.ut.accounting-s1.2026-2027.s3 \
  --candidate-model <candidate> \
  --grader-model <judge>
```

Runner memuat manifest, Project Instructions, eval suite/context yang dideklarasikan, menjalankan candidate, meminta structured verdict dari judge, lalu menyimpan hasil ke `evals/results/`.

Workflow **Behavior Evals** dibuat manual agar API tidak terpakai pada setiap push. Hasil probabilistik tetap perlu dikaitkan dengan pack version, contract version, tanggal, dan model yang benar-benar diuji.
