# Create a Pack

Jalur ini untuk mengubah kebutuhan yang sudah cukup jelas menjadi **draft community pack** tanpa harus menulis manifest, registry, eval wiring, dan struktur folder dari nol.

Ini berbeda dari [Ramu Starter](../starter/README.md):

- **Starter** untuk pemakaian personal satu mata kuliah dan tidak masuk katalog;
- **Create a Pack** untuk scaffold yang memang diarahkan menjadi kontribusi reusable ke repository.

Generator tetap konservatif. Ia tidak mencari source sendiri, tidak menganggap input contributor otomatis benar, tidak menulis klaim `verified`, dan tidak mengarang regression case.

## Input minimum

Sebelum membuat draft, siapkan:

- label + ID institusi yang stabil;
- label + ID program yang stabil;
- tahun akademik;
- `period_id` dan `period_label`;
- pack ID yang unik;
- daftar course: kode, nama, short name, SKS, dan fokus;
- minimal satu source HTTPS yang benar-benar sudah dibaca contributor;
- nama dan authority source tersebut.

Contoh:

```bash
python scripts/create_pack.py \
  --institution "Kampus Contoh" \
  --institution-id kampus-contoh \
  --program "S1 Manajemen" \
  --program-id kampus-contoh.s1-manajemen \
  --academic-year "2026/2027" \
  --period-id semester-01 \
  --period-label "Semester 1" \
  --pack-id id.community.kampus-contoh.management-s1.2026-2027.s1 \
  --course "MAN101|Pengantar Manajemen|Pengantar Manajemen|3|konsep dasar manajemen dan organisasi" \
  --course "ECO101|Pengantar Ekonomi|Pengantar Ekonomi|3|mikro dan makro dasar untuk keputusan bisnis" \
  --source-url "https://example.edu/catalog" \
  --source-name "Katalog Akademik 2026/2027" \
  --source-authority "Kampus Contoh"
```

## Output

Generator membuat scaffold dengan:

- `manifest.json` schema v4;
- `PROJECT-INSTRUCTIONS.md` generik untuk draft community pack;
- satu file course per input;
- pack-scoped `source-registry.json`;
- `evals/contracts.json` dan `evals/behavior.json` dengan `cases: []`;
- `catalog-entry.example.json` untuk membantu penambahan ke `packs/index.json`;
- README lokal berisi checklist review.

Status awal selalu:

```text
status: experimental
maintainer: community
```

`source_verified_at` pada draft adalah tanggal contributor menyatakan source input terakhir dibaca. Itu bukan endorsement maintainer Ramu dan bukan alasan untuk menaikkan status menjadi `source-verified` atau `verified`.

## Kenapa eval dimulai kosong?

Karena regression case harus mewakili failure mode nyata yang bisa dijelaskan dan diuji ulang. Generator yang otomatis membuat `E01`, `E02`, dan seterusnya tanpa masalah nyata justru merusak evidence model Ramu.

Core eval tetap diwarisi melalui:

```text
core → pack draft
```

Tambahkan suite institusi/program hanya bila memang ada aturan reusable pada scope tersebut.

## Sebelum masuk katalog

Jangan langsung copy `catalog-entry.example.json` lalu merge. Review dulu:

1. identity dan path tidak akan mudah berubah setelah dipublish;
2. setiap metadata course sesuai source current;
3. source registry memakai authority dan `canonical_for` yang tepat;
4. source sekunder/community signal tidak naik kelas menjadi canonical tanpa dasar;
5. course pack tidak menyalin materi berhak cipta;
6. Project Instructions tidak mengarang kebijakan institusi/tutor;
7. failure mode penting punya eval pada scope yang tepat;
8. total SKS, file path, source dependency, dan eval wiring konsisten.

Setelah draft dipindahkan ke path final `packs/...`, tambahkan entry ke `packs/index.json`, lalu jalankan:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_schemas.py
python scripts/validate_repo.py
python scripts/validate_scope_identities.py
python scripts/validate_display_names.py
python scripts/validate_site.py
python scripts/check_source_freshness.py
python scripts/run_behavior_evals.py --dry-run --pack <pack-id>
```

Jalankan browser regression bila environment sudah mempunyai Chromium Playwright:

```bash
python -m playwright install chromium
python tests/test_site_browser.py
```

## Kapan memakai Starter saja?

Tetap gunakan Starter bila konteksnya personal, source belum cukup kuat, struktur course masih berubah, atau artefaknya tidak punya alasan untuk dipakai orang lain. Tidak semua workspace perlu menjadi public pack.
