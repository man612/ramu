# Manual Behavior Validation

Jalur ini dipakai ketika maintainer/tester ingin menguji Ramu langsung di **ChatGPT Projects** tanpa OpenAI API.

Manual validation bukan pengganti static CI. Keduanya menguji hal berbeda:

- `scripts/validate_repo.py` — struktur, manifest, source registry, contract marker, dan wiring eval;
- `scripts/run_behavior_evals.py --dry-run` — memastikan core + pack behavior suite dapat dirakit;
- **manual validation** — memeriksa perilaku ChatGPT Projects asli;
- automated API behavior eval — lapisan tambahan opsional bila API tersedia.

## Membuat checklist

```bash
python scripts/prepare_manual_eval.py --pack id.ut.accounting-s1.2026-2027.s2
```

Atau case tertentu:

```bash
python scripts/prepare_manual_eval.py \
  --pack id.ut.accounting-s1.2026-2027.s2 \
  --only E01,E05,E08,E13,E14,E15,E16
```

File checklist hasil generate diabaikan Git agar hasil percakapan/test pribadi tidak tidak sengaja masuk commit.

## GitHub Actions tanpa API

Workflow **Manual Eval Kit** hanya membuat checklist sebagai artifact. Ia tidak memanggil model, tidak membutuhkan secret, dan tidak menimbulkan biaya API. Download checklist, jalankan case satu per satu di ChatGPT Project yang benar, lalu tandai PASS/PARTIAL/FAIL secara lokal.

## Cara membaca hasil

Satu PASS hanya berarti perilaku pada kombinasi **tanggal + ChatGPT product state + plan/model yang terlihat + pack version** tersebut memenuhi contract. Jangan mengubah status pack menjadi `verified` hanya dari satu run manual singkat; review failure material dan ulangi case penting setelah perubahan guardrail/course pack.
