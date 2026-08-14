# Evals

Ramu memakai dua lapisan evaluasi:

1. **contract tests** — berjalan tanpa model/API. Tes ini memastikan guardrail penting tidak hilang dari Project Instructions, protokol, atau course pack ketika file diedit;
2. **behavior evals** — skenario konkret benar-benar dikirim ke model kandidat, lalu responsnya dinilai model judge terhadap expected dan forbidden behavior.

Contract cases ada di [`cases/semester-02.json`](cases/semester-02.json). Skenario executable ada di [`behavior/semester-02.json`](behavior/semester-02.json), dengan panduan lengkap di [`behavior/README.md`](behavior/README.md).

## Pemeriksaan tanpa API

```bash
python scripts/validate_repo.py
python scripts/run_behavior_evals.py --dry-run
```

Validator memeriksa manifest, total SKS, course file, source registry, ID eval, contract marker, template belajar, serta wiring seluruh behavior case E01–E12.

## Behavior eval nyata

```bash
export OPENAI_API_KEY="..."
python scripts/run_behavior_evals.py
```

Runner akan:

- memuat Project Instructions dan context yang relevan;
- menjalankan model kandidat melalui Responses API;
- mengaktifkan `web_search` hanya pada case yang memang membutuhkannya;
- meminta model judge mengeluarkan penilaian terstruktur;
- menghasilkan skor per case, pass rate, penggunaan token, respons kandidat, dan alasan judge;
- menyimpan laporan ke `evals/results/` untuk artifact/audit, bukan untuk dikomit.

Di GitHub, workflow **Behavior Evals** sengaja hanya manual agar API tidak terpakai setiap push. Run memerlukan repository secret `OPENAI_API_KEY`.

Contract tests tetap penting karena murah dan deterministik, sedangkan behavior eval menguji sesuatu yang contract test tidak bisa buktikan: **apakah model benar-benar mengikuti guardrail saat menghadapi percakapan nyata**. Karena output model probabilistik, satu run tidak dianggap bukti permanen; regression penting sebaiknya dibandingkan pada beberapa run atau model snapshot.
