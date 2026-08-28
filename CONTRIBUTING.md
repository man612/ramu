# Berkontribusi ke Ramu

Terima kasih sudah ingin membantu Ramu. Kontribusi paling berguna adalah perubahan yang membuat perilaku belajar lebih dapat diuji, sumber lebih dapat dipercaya, setup lebih mudah, atau pack lebih mudah dipelihara.

## Sebelum membuat perubahan

1. Jangan menambahkan BMP, modul, materi kuliah berbayar, kunci jawaban, atau dokumen lain yang tidak boleh didistribusikan ulang.
2. Untuk fakta akademik, prioritaskan sumber resmi dan masukkan source ke registry dengan scope yang tepat.
3. Pisahkan fakta terverifikasi dari asumsi, pengalaman komunitas, dan keputusan desain.
4. Jangan mengunci runtime ke satu nama model AI. Model/plan dapat berubah; kontrak Ramu harus tetap masuk akal ketika model berganti.
5. Jangan menyebut pack Ramu sebagai pack “resmi” dari universitas. Gunakan `maintainer: ramu` (Ramu Maintained) atau `maintainer: community`.
6. Gunakan label periode yang jelas untuk pengguna. Jangan memakai `S2`, `S3`, dan bentuk singkat serupa sebagai pengganti “Semester 2/3” pada nama Project karena dapat tertukar dengan jenjang pendidikan.

## Jalur kontribusi

- dokumentasi dan onboarding;
- protocol, Project Instructions, atau course pack;
- perubahan/kerusakan source resmi;
- behavior eval untuk failure mode realistis;
- validator, source watcher, site, atau tooling eval;
- pack periode/program/institusi baru.

## Menambah pack baru

Tooling Ramu menemukan pack melalui [`packs/index.json`](packs/index.json). Jangan menambahkan path baru ke JavaScript atau Python secara manual.

Untuk pack baru:

1. buat struktur `packs/<institusi>/<program>/<tahun>/<periode>/`;
2. tentukan stable `institution_id` dan `program_id` yang machine-safe; `program_id` harus berada di namespace institusi, misalnya `id.ut` → `id.ut.accounting-s1`;
3. buat `manifest.json` mengikuti `schemas/pack-manifest.schema.json`; pack `id` harus berada di namespace `program_id`;
4. tentukan `period_id` machine-safe, misalnya `semester-03`, `trimester-01`, `quarter-fall`, atau `term-02`;
5. tentukan `period_label` yang manusiawi sesuai istilah institusi, misalnya `Semester 3`, `Trimester 1`, `Fall Quarter`, atau `Term 2`;
6. taruh course pack di folder `courses/` dan Project Instructions di pack tersebut;
7. pakai registry yang sudah ada atau buat scoped `source-registry.json` jika source-nya belum punya tempat yang tepat;
8. tentukan eval suite yang benar-benar berlaku untuk pack tersebut;
9. buat eval khusus pack di `<pack>/evals/contracts.json` dan `<pack>/evals/behavior.json`;
10. daftarkan semua suite berurutan pada `eval_suites` di manifest dengan `scope_ref` memakai stable identity;
11. daftarkan pack di `packs/index.json` dengan identity dan period metadata yang sama;
12. jalankan seluruh validasi lokal.

Field penting:

- `institution_id`: ID stabil institusi untuk relasi mesin, misalnya `id.ut`; jangan memakai nama tampilan sebagai foreign key;
- `program_id`: ID stabil program di namespace institusi, misalnya `id.ut.accounting-s1`;
- `id`: ID pack di namespace program, misalnya `id.ut.accounting-s1.2026-2027.s2`;
- `status`: `source-verified`, `verified`, `community`, `experimental`, atau `deprecated`;
- `maintainer`: `ramu` atau `community`;
- `period_id`: ID periode untuk mesin, lower-case dan stabil, misalnya `semester-02`, `trimester-01`, atau `term-fall`;
- `period_label`: label periode yang dilihat manusia, misalnya `Semester 2`, `Trimester 1`, atau `Fall Term`;
- `project_name`: harus diawali `<period_label> • `, misalnya `Semester 2 • AKM I`;
- `source_registries`: registry yang memang menjadi dependency pack dan identity scope-nya harus cocok;
- `eval_suites`: ordered suite `core → institution → program → pack`; `scope_ref` harus sama dengan `institution_id`, `program_id`, atau pack `id` sesuai scope;
- `focus`: deskripsi pendek setiap mata kuliah untuk site; jangan hardcode focus di front-end.

Ramu sengaja tidak memiliki field universal bernama `semester`. Semester hanyalah salah satu bentuk academic period. Pack yang memang memakai semester cukup merepresentasikannya melalui `period_id`/`period_label`. Identifier pack, folder, atau versi internal boleh tetap ringkas seperti `.s2`, `semester-02/`, atau `2026-2027.s2.1` bila itu memang identitas pack tersebut; generic tooling tidak boleh mengasumsikan semua pack mengikuti bentuk itu.

## Memilih scope eval

Jangan copy sebuah regression case hanya karena pack baru membutuhkan perilaku yang sama. Tempatkan case pada scope paling sempit yang masih benar-benar reusable:

- `core` → berlaku untuk semua pack Ramu, misalnya sitasi palsu atau prompt injection;
- `institution` → berlaku lintas program/periode pada satu institusi, misalnya aturan source governance Universitas Terbuka;
- `program` → berlaku lintas periode pada satu program, tetapi tidak otomatis untuk program lain;
- `pack` → membutuhkan mata kuliah/periode/course pack tertentu.

Setiap suite memiliki `suite_id`, `scope`, dan—selain core—`scope_ref`. File contracts dan behavior harus mendeklarasikan metadata yang sama dengan manifest. ID case harus unik setelah semua suite digabung; suite yang lebih spesifik **tidak mengganti** case milik suite sebelumnya.

`scope_ref` bukan slug bebas. Nilainya harus menunjuk stable identity milik manifest:

```text
core → institution:id.ut → pack:id.ut.accounting-s1.2026-2027.s2
```

atau bila ada rule khusus S1 Akuntansi lintas periode:

```text
core → institution:id.ut → program:id.ut.accounting-s1 → pack:id.ut.accounting-s1.2026-2027.s3
```

Behavior `defaults` diproses berurutan, sehingga suite yang lebih spesifik boleh mengubah default runtime seperti threshold/token untuk case berikutnya. Perubahan default harus disengaja dan dijelaskan di PR.

## Memilih scope source

- `sources/registry.json` → global/runtime dan tidak punya identity institusi/program/pack;
- `packs/<institusi>/source-registry.json` → source institusi dan wajib `institution_id`;
- registry scope `program` → wajib `institution_id` + `program_id`;
- registry scope `pack` → wajib `institution_id` + `program_id` + `pack_id`.

ID source harus unik lintas seluruh registry. Source sekunder atau community signal tidak boleh diam-diam menjadi kanonik hanya karena berada di domain resmi.

## Validasi tanpa API

Runtime Ramu tetap tidak membutuhkan dependency Python eksternal. Dependency di bawah hanya untuk validation tooling CI/dev:

```bash
python -m pip install -r requirements-ci.txt
python scripts/validate_schemas.py
python scripts/validate_scope_identity.py
python scripts/test_architecture_contracts.py
python scripts/validate_repo.py
python scripts/validate_display_names.py
python scripts/validate_site.py
python scripts/check_source_freshness.py
python scripts/run_behavior_evals.py --dry-run --pack <pack-id>
```

`validate_schemas.py` menjalankan JSON Schema Draft 2020-12 terhadap catalog, seluruh manifest, source registry, contracts, dan behavior dataset. `validate_scope_identity.py` memeriksa relasi lintas-file. `test_architecture_contracts.py` memakai fixture sintetis yang membuktikan beberapa pack/institusi, Semester + Trimester + Term, program-level suite, dan rejection untuk cross-scope identity. Fixture tidak dipublish sebagai pack pengguna.

Untuk daftar pack:

```bash
python scripts/list_pack_ids.py
```

Untuk membuat checklist yang dapat diuji langsung di ChatGPT Projects tanpa OpenAI API:

```bash
python scripts/prepare_manual_eval.py --pack <pack-id>
```

Workflow **Manual Eval Kit** melakukan hal yang sama melalui GitHub Actions tanpa secret dan tanpa biaya API.

## Behavior eval dengan API — opsional

Automated behavior eval adalah lapisan QA tambahan, bukan dependency untuk mahasiswa atau syarat agar static CI berjalan. Jika digunakan, `OPENAI_API_KEY`, candidate model, grader model, dan pack dipilih eksplisit pada workflow **Behavior Evals**.

Jangan memasukkan API key ke commit, issue, artifact, screenshot, atau log publik.

## Pull request

Buat PR sekecil mungkin dan jelaskan:

- masalah yang diperbaiki;
- scope eval/source/pack yang terpengaruh;
- source yang digunakan bila mengubah fakta akademik;
- cara memverifikasi perubahan;
- risiko atau hal yang belum diuji.

Jika perubahan menyentuh guardrail, source routing, state, atau perilaku tutor, tambahkan/perbarui eval yang relevan pada scope yang tepat. Failure mode universal masuk core; aturan institusi/program jangan diduplikasi ke setiap pack; skenario yang benar-benar membutuhkan course pack tertentu tetap dekat dengan pack.

## Prinsip review

Perubahan tidak dinilai dari panjang prompt atau dokumentasinya. Yang dicari adalah perilaku yang jelas, sumber yang dapat ditelusuri, manifest yang self-describing, stable identity yang tidak bergantung nama tampilan, period metadata yang tidak mengunci satu sistem kalender, setup yang mudah, dan cara nyata untuk menguji ulang perubahan tersebut.
