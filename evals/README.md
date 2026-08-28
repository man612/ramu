# Evals

Ramu memisahkan **scope evaluasi**, **urutan komposisi**, dan **cara menjalankannya**.

## Composable eval suites

Setiap pack mendeklarasikan `eval_suites` berurutan di `manifest.json`. Scope yang didukung:

1. `core` — failure mode universal Ramu;
2. `institution` — aturan/failure mode yang berlaku lintas pack pada satu institusi;
3. `program` — aturan/failure mode yang berlaku lintas periode pada satu program studi;
4. `pack` — skenario yang benar-benar spesifik pada pack/periode/mata kuliah tersebut.

Urutannya selalu dari umum ke spesifik: `core → institution → program → pack`. Scope yang tidak dibutuhkan boleh dilewati, misalnya `core → pack`.

Contoh pack UT S1 Akuntansi Semester 2 sekarang:

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
    "id": "semester-02",
    "scope": "pack",
    "scope_ref": "id.ut.accounting-s1.2026-2027.s2",
    "contracts": "packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/evals/contracts.json",
    "behavior": "packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/evals/behavior.json"
  }
]
```

Validator mewajibkan `core` berada di awal dan `pack` di akhir. Scope tidak boleh mundur ke level yang lebih umum. `suite_id`, `scope`, dan `scope_ref` pada file contracts/behavior harus cocok dengan deklarasi manifest.

ID case harus **unik setelah seluruh suite digabung**. Jadi suite yang lebih spesifik tidak boleh diam-diam mengganti E01/E14 milik suite sebelumnya. Bila behavior suite yang lebih spesifik mendefinisikan `defaults`, nilai default runtime seperti `min_score` atau `max_output_tokens` boleh mengoverride nilai dari suite sebelumnya secara berurutan.

## Scope yang tersedia sekarang

### Core

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

### Universitas Terbuka

`packs/universitas-terbuka/evals/` berisi failure mode yang memang terkait source governance UT dan dapat dipakai ulang oleh pack UT lain. E14, misalnya, menguji konflik source pusat vs regional berdasarkan registry UT.

### Pack Semester 2

`packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02/evals/` hanya menyimpan skenario yang membutuhkan konteks pack tersebut, misalnya aturan pajak vs BMP, jurnal AKM I, contoh pedagogis pada mata kuliah S2, dan context isolation antarmata kuliah.

Dengan struktur ini, Semester 3 UT nanti dapat menyertakan suite `core + ut + <suite pack Semester 3>` tanpa menyalin E14. Jika suatu hari S1 Akuntansi mempunyai failure mode lintas semester yang tidak berlaku untuk program lain, suite `program` dapat ditambahkan di antara `ut` dan suite pack.

## Tiga jalur pemeriksaan

1. **Static validation** — gratis/deterministik; memeriksa manifest, source registry, contract marker, suite metadata, file, dan wiring.
2. **Manual behavior validation** — gratis; case dijalankan manusia langsung di ChatGPT Projects.
3. **Automated API behavior eval** — opsional; model kandidat dijalankan via API dan respons dinilai judge model.

Tidak memiliki API tidak membuat Ramu gagal atau tidak dapat dipakai. API hanya menambah automation/reproducibility pada satu lapisan QA.

## Pemeriksaan tanpa API

```bash
python scripts/validate_repo.py
python scripts/run_behavior_evals.py --dry-run --pack id.ut.accounting-s1.2026-2027.s2
python scripts/check_source_freshness.py
```

CI mengambil seluruh pack dari `packs/index.json` dan menjalankan dry-run per pack melalui matrix. Dry-run selalu memakai suite yang dideklarasikan manifest pack tersebut.

## Manual validation di ChatGPT Projects

```bash
python scripts/prepare_manual_eval.py \
  --pack id.ut.accounting-s1.2026-2027.s2
```

Atau buka **Actions → Manual Eval Kit**. Workflow itu tidak membutuhkan secret/API dan menghasilkan checklist dari merged suite sebagai artifact.

Panduan: [`manual/README.md`](manual/README.md).

## Automated behavior eval — opsional

```bash
export OPENAI_API_KEY="..."
python scripts/run_behavior_evals.py \
  --pack id.ut.accounting-s1.2026-2027.s2 \
  --candidate-model <candidate> \
  --grader-model <judge>
```

Runner memuat manifest pack, Project Instructions, seluruh eval suite/context yang dideklarasikan, menjalankan kandidat, meminta judge structured verdict, lalu menyimpan summary/artifact ke `evals/results/`.

Workflow **Behavior Evals** sengaja manual agar API tidak terpakai pada setiap push. Satu run probabilistik bukan bukti permanen; hasil penting perlu direview manusia dan dikaitkan dengan pack version + contract version + tanggal + model yang benar-benar diuji.
