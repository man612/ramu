# Berkontribusi ke Ramu

Kontribusi yang paling berguna biasanya jatuh ke salah satu dari empat hal: memperbaiki perilaku belajar, memperjelas setup, menjaga source tetap benar, atau membuat pack/tooling lebih mudah dipelihara.

## Sebelum mulai

Beberapa aturan dasar:

1. jangan commit BMP, modul berbayar, kunci jawaban, atau materi lain yang tidak boleh didistribusikan ulang;
2. fakta akademik perlu ditopang source resmi yang sesuai;
3. bedakan fakta terverifikasi, asumsi, pengalaman komunitas, dan keputusan desain;
4. jangan mengunci runtime ke satu nama model AI;
5. pack yang dipelihara di repository utama tetap proyek independen, bukan pack resmi universitas;
6. gunakan label periode yang jelas pada UI, misalnya `Semester 3`, bukan `S3`;
7. jaga `institution_id`, `program_id`, dan pack `id` tetap stabil setelah dipakai.

## Jenis kontribusi

Yang cocok dibawa lewat issue atau PR antara lain:

- dokumentasi dan onboarding;
- protocol, Project Instructions, atau course pack;
- source resmi yang berubah atau tidak sinkron;
- behavior eval untuk failure mode yang bisa direproduksi;
- validator, source watcher, site, atau tooling eval;
- pack periode/program/institusi baru.

## Menambah pack baru

Tooling menemukan pack dari [`packs/index.json`](packs/index.json). Hindari menambahkan daftar path baru secara manual ke JavaScript atau Python.

Urutan kerja yang disarankan:

1. buat `packs/<institusi>/<program>/<tahun>/<periode>/`;
2. tentukan `institution_id` yang stabil dan machine-safe;
3. tentukan `program_id` yang stabil dan unik secara global;
4. buat `manifest.json` mengikuti `schemas/pack-manifest.schema.json`;
5. isi `period_id`, misalnya `semester-03`, `trimester-01`, atau `term-fall`;
6. isi `period_label` sesuai istilah manusiawi yang dipakai institusi;
7. tambahkan Project Instructions dan course pack;
8. pakai registry yang sudah ada atau buat scoped `source-registry.json` jika diperlukan;
9. pilih eval suite pada scope yang tepat;
10. buat eval khusus pack bila memang ada failure mode pack-specific;
11. susun `eval_suites` dari umum ke spesifik;
12. daftarkan pack di `packs/index.json`;
13. jalankan seluruh validasi sebelum membuka PR.

Field yang paling sering disentuh:

- `institution_id` — identity mesin institusi;
- `institution` — label institusi untuk manusia;
- `program_id` — identity mesin program;
- `program` — label program;
- `status` — `source-verified`, `verified`, `community`, `experimental`, atau `deprecated`;
- `maintainer` — `ramu` atau `community`;
- `period_id` — ID periode machine-safe;
- `period_label` — label periode untuk UI;
- `project_name` — diawali `<period_label> • `;
- `source_registries` — registry yang menjadi dependency pack;
- `eval_suites` — urutan suite yang berlaku;
- `focus` — deskripsi pendek mata kuliah untuk site.

Periode tidak disimpan dalam field universal `semester`. Pack yang memang memakai semester cukup memakai `period_id`/`period_label`, sementara institusi lain dapat menggunakan istilah kalender mereka sendiri.

## Memilih scope eval

Letakkan regression case pada scope paling sempit yang masih reusable:

- `core` — berlaku untuk semua pack, misalnya sitasi palsu atau prompt injection;
- `institution` — berlaku lintas pack dalam satu institusi;
- `program` — berlaku lintas periode pada satu program;
- `pack` — membutuhkan konteks periode atau mata kuliah tertentu.

Jangan copy case yang sama ke banyak pack hanya karena semuanya membutuhkan perilaku tersebut.

Setiap suite memiliki `suite_id`, `scope`, dan—selain core—`scope_ref`.

`scope_ref` harus cocok dengan identity manifest:

- `institution` → `institution_id`;
- `program` → `program_id`;
- `pack` → pack `id`;
- `core` → tanpa `scope_ref`.

Contract dan behavior file harus mendeklarasikan metadata yang sama. ID case tetap unik setelah seluruh suite digabung.

Contoh urutan:

```text
core → institution:universitas-terbuka → pack:id.ut.accounting-s1.2026-2027.s2
```

Jika suatu hari ada aturan khusus S1 Akuntansi lintas periode:

```text
core → institution:universitas-terbuka → program:universitas-terbuka.s1-akuntansi → pack:<pack-id>
```

Behavior `defaults` diproses berurutan, jadi suite yang lebih spesifik boleh mengubah default runtime. Perubahan tersebut harus jelas di PR.

## Memilih scope source

- `sources/registry.json` → global/runtime;
- `packs/<institusi>/source-registry.json` → institusi;
- registry program → membawa identity institusi + program;
- registry pack → membawa identity institusi + program + `pack_id`.

Source ID harus unik lintas registry. Halaman sekunder atau community signal juga tidak otomatis menjadi kanonik hanya karena domainnya resmi.

## Validasi lokal

Gunakan Python 3.12 atau versi kompatibel.

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

`validate_schemas.py` memeriksa schema dan instance JSON. `validate_repo.py` serta `validate_scope_identities.py` menangani invariant lintas-file yang lebih tepat diperiksa secara semantik.

Daftar pack:

```bash
python scripts/list_pack_ids.py
```

Checklist manual tanpa API:

```bash
python scripts/prepare_manual_eval.py --pack <pack-id>
```

Workflow **Manual Eval Kit** menyediakan jalur yang sama lewat GitHub Actions.

## Behavior eval dengan API

Automated behavior eval adalah QA tambahan. Bila digunakan, `OPENAI_API_KEY`, candidate model, grader model, dan pack dipilih saat workflow dijalankan.

Jangan memasukkan API key ke commit, issue, artifact, screenshot, atau log publik.

## Pull request

PR yang baik menjelaskan:

- masalah yang diperbaiki;
- scope yang berubah;
- source yang dipakai bila ada perubahan fakta akademik;
- cara memverifikasi hasil;
- hal yang belum diuji atau risiko yang masih tersisa.

Jika perubahan menyentuh guardrail, source routing, learner state, atau perilaku tutor, tambahkan/perbarui eval pada scope yang sesuai.

## Prinsip review

Yang dicari bukan dokumentasi paling panjang, tetapi perubahan yang bisa dipahami dan diuji ulang: source jelas, identity stabil, metadata periode konsisten, setup tetap sederhana, dan failure mode penting punya tempat untuk direproduksi.
