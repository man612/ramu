# Evals

Ramu memakai dua lapisan evaluasi:

1. **contract tests** — dapat dijalankan otomatis tanpa model/API. Tes ini memastikan guardrail penting tidak hilang dari Project Instructions, protokol, atau course pack ketika file diedit;
2. **behavior evals** — skenario yang harus dijalankan terhadap model untuk menilai perilaku nyata. Bagian ini tetap membutuhkan review manusia atau grader yang sesuai.

Sumber kasus terstruktur ada di [`cases/semester-02.json`](cases/semester-02.json). Versi Markdown lama tetap dipertahankan sebagai ringkasan yang mudah dibaca.

Jalankan pemeriksaan lokal:

```bash
python scripts/validate_repo.py
```

Validator akan memeriksa:

- manifest dan total SKS;
- semua course file yang direferensikan;
- struktur source registry;
- ID eval yang unik;
- setiap contract marker benar-benar ada pada file yang dituju;
- template learner state tersedia.

Contract test **tidak membuktikan model pasti berperilaku benar**. Ia mencegah regression yang lebih sederhana: misalnya guardrail sitasi palsu, screenshot terpotong, atau source conflict terhapus tanpa sengaja dari prompt/course pack.
