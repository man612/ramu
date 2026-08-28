# Berkontribusi ke Ramu

Terima kasih sudah ingin membantu Ramu. Kontribusi paling berguna adalah perubahan yang membuat perilaku belajar lebih dapat diuji, sumber lebih dapat dipercaya, setup lebih mudah, atau pack lebih mudah dipelihara.

## Sebelum membuat perubahan

1. Jangan menambahkan BMP, modul, materi kuliah berbayar, kunci jawaban, atau dokumen lain yang tidak boleh didistribusikan ulang.
2. Untuk fakta akademik, prioritaskan sumber resmi dan masukkan source ke registry dengan scope yang tepat.
3. Pisahkan fakta terverifikasi dari asumsi, pengalaman komunitas, dan keputusan desain.
4. Jangan mengunci runtime ke satu nama model AI. Model/plan dapat berubah; kontrak Ramu harus tetap masuk akal ketika model berganti.
5. Jangan menyebut pack Ramu sebagai pack “resmi” dari universitas. Gunakan `maintainer: ramu` (Ramu Maintained) atau `maintainer: community`.
6. Gunakan label periode yang jelas untuk pengguna. Jangan memakai `S2`, `S3`, dan bentuk singkat serupa sebagai pengganti “Semester 2/3” pada nama Project karena dapat tertukar dengan jenjang pendidikan.
7. Pisahkan label manusia dari identity mesin. Nama institusi/program boleh berubah tampilannya, tetapi `institution_id`, `program_id`, dan `pack id` harus stabil dan tidak boleh dipakai ulang untuk entitas berbeda.

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
2. tentukan `institution_id` yang stabil dan machine-safe untuk institusi tersebut;
3. tentukan `program_id` yang stabil dan unik secara global untuk program tersebut;
4. buat `manifest.json` mengikuti `schemas/pack-manifest.schema.json`;
5. tentukan `period_id` machine-safe, misalnya `semester-03`, `trimester-01`, `quarter-fall`, atau `term-02`;
6. tentukan `period_label` yang manusiawi sesuai istilah institusi, misalnya `Semester 3`, `Trimester 1`, `Fall Quarter`, atau `Term 2`;
7. taruh course pack di folder `courses/` dan Project Instructions di pack tersebut;
8. pakai registry yang sudah ada atau buat scoped `source-registry.json` jika source-nya belum punya tempat yang tepat; scoped registry harus membawa identity institusi/program/pack yang sesuai;
9. tentukan eval suite yang benar-benar berlaku untuk pack tersebut;
10. buat eval khusus pack di `<pack>/evals/contracts.json` dan `<pack>/evals/behavior.json`;
11. daftarkan semua suite berurutan pada `eval_suites` di manifest; `scope_ref` harus menunjuk identity mesin yang sesuai;
12. daftarkan pack di `packs/index.json` dengan identity, `period_id`, dan `period_label` yang sama dengan manifest;
13. jalankan seluruh validasi sebelum membuka PR.

Field penting:

- `institution_id`: identity mesin stabil untuk institusi, misalnya `universitas-terbuka`;
- `institution`: label manusia, misalnya `Universitas Terbuka`;
- `program_id`: identity mesin unik secara global untuk program, misalnya `universitas-terbuka.s1-akuntansi`;
- `program`: label manusia, misalnya `S1 Akuntansi`;
- `status`: `source-verified`, `verified`, `community`, `experimental`, atau `deprecated`;
- `maintainer`: `ramu` atau `community`;
- `period_id`: ID periode untuk mesin, lower-case dan stabil, misalnya `semester-02`, `trimester-01`, atau `term-fall`;
- `period_label`: label periode yang dilihat manusia, misalnya `Semester 2`, `Trimester 1`, atau `Fall Term`;
- `project_name`: harus diawali `<period_label> • `, misalnya `Semester 2 • AKM I`;
- `source_registries`: registry yang memang menjadi dependency pack;
- `eval_suites`: ordered suite `core → institution → program → pack` yang memang berlaku untuk pack;
- `focus`: deskripsi pendek setiap mata kuliah untuk site; jangan hardcode focus di front-end.

Ramu sengaja tidak memiliki field universal bernama `semester`. Semester hanyalah salah satu bentuk academic period. Pack yang memang memakai semester cukup merepresentasikannya melalui `period_id`/`period_label`. Identifier pack, folder, atau versi internal boleh tetap ringkas seperti `.s2`, `semester-02/`, atau `2026-2027.s2.1` bila itu memang identitas pack tersebut; generic tooling tidak boleh mengasumsikan semua pack mengikuti bentuk itu.

## Memilih scope eval

Jangan copy sebuah regression case hanya karena pack baru membutuhkan perilaku yang sama. Tempatkan case pada scope paling sempit yang masih benar-benar reusable:

- `core` → berlaku untuk semua pack Ramu, misalnya sitasi palsu atau prompt injection;
- `institution` → berlaku lintas program/periode pada satu institusi, misalnya aturan source governance Universitas Terbuka;
- `program` → berlaku lintas periode pada satu program, tetapi tidak otomatis untuk program lain;
- `pack` → membutuhkan mata kuliah/periode/course pack tertentu.

Setiap suite memiliki `suite_id`, `scope`, dan—selain core—`scope_ref`. `scope_ref` bukan label bebas:

- `institution` harus sama dengan `institution_id` manifest;
- `program` harus sama dengan `program_id` manifest;
- `pack` harus sama dengan `id` pack;
- `core` tidak boleh mempunyai `scope_ref`.

File contracts dan behavior harus mendeklarasikan metadata yang sama dengan manifest. ID case harus unik setelah semua suite digabung; suite yang lebih spesifik **tidak mengganti** case milik suite sebelumnya.

Urutan di manifest harus dari umum ke spesifik. Contoh:

```text
core → institution:universitas-terbuka → pack:id.ut.accounting-s1.2026-2027.s2
```

atau bila ada rule khusus S1 Akuntansi lintas periode:

```text
core → institution:universitas-terbuka → program:universitas-terbuka.s1-akuntansi → pack:<pack-id>
```

Behavior `defaults` diproses berurutan, sehingga suite yang lebih spesifik boleh mengubah default runtime seperti threshold/token untuk case berikutnya. Perubahan default harus disengaja dan dijelaskan di PR.

## Memilih scope source

- `sources/registry.json` → global/runtime, misalnya dokumentasi platform; registry global tidak membawa identity institusi/program/pack;
- `packs/<institusi>/source-registry.json` → source institusi dan wajib membawa `institution_id` + label institusi;
- registry program → wajib membawa `institution_id`, `program_id`, dan label manusianya;
- registry pack → wajib membawa identity institusi + program + `pack_id`.

Cross-file identity validator memastikan pack tidak dapat diam-diam memakai scoped registry atau eval suite milik institusi/program lain. ID source tetap harus unik lintas seluruh registry. Source sekunder atau community signal tidak boleh diam-diam menjadi kanonik hanya karena berada di domain resmi.

## Validasi tanpa API

Gunakan Python 3.12 atau versi kompatibel. Dependency di `requirements-dev.txt` hanya untuk validation tooling dan bukan dependency runtime mahasiswa.

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

`validate_schemas.py` melakukan dua hal berbeda dari semantic validator: memastikan setiap schema Ramu sendiri valid sebagai JSON Schema Draft 2020-12, lalu memvalidasi katalog, semua manifest, semua source registry, dan semua eval JSON terhadap schema yang dipublish. `validate_repo.py` dan `validate_scope_identities.py` tetap diperlukan untuk invariant lintas-file yang tidak cukup dinyatakan oleh satu JSON Schema instance.

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

Perubahan tidak dinilai dari panjang prompt atau dokumentasinya. Yang dicari adalah perilaku yang jelas, sumber yang dapat ditelusuri, manifest yang self-describing, identity institusi/program yang stabil, period metadata yang tidak mengunci satu sistem kalender, label yang tidak membingungkan pengguna, setup yang mudah, dan cara nyata untuk menguji ulang perubahan tersebut.
