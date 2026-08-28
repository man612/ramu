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
- pack semester/program/institusi baru.

## Menambah pack baru

Tooling Ramu menemukan pack melalui [`packs/index.json`](packs/index.json). Jangan menambahkan path baru ke JavaScript atau Python secara manual.

Untuk pack baru:

1. buat struktur `packs/<institusi>/<program>/<tahun>/<periode>/`;
2. buat `manifest.json` mengikuti `schemas/pack-manifest.schema.json`;
3. tentukan `period_label` yang manusiawi, misalnya `Semester 3`, `Trimester 1`, atau istilah resmi lain yang dipakai institusi;
4. taruh course pack di folder `courses/` dan Project Instructions di pack tersebut;
5. pakai registry yang sudah ada atau buat scoped `source-registry.json` jika source-nya belum punya tempat yang tepat;
6. tentukan eval suite yang benar-benar berlaku untuk pack tersebut;
7. buat eval khusus pack di `<pack>/evals/contracts.json` dan `<pack>/evals/behavior.json`;
8. daftarkan semua suite berurutan pada `eval_suites` di manifest;
9. daftarkan pack di `packs/index.json`;
10. jalankan validasi. Validator akan gagal jika menemukan manifest yang belum masuk katalog, wiring suite yang salah, entry yang menunjuk file hilang, atau nama Project yang tidak mengikuti `period_label`.

Field penting:

- `status`: `source-verified`, `verified`, `community`, `experimental`, atau `deprecated`;
- `maintainer`: `ramu` atau `community`;
- `semester`: nilai terstruktur untuk periode bila format pack memang memakai semester;
- `period_label`: label yang dilihat manusia, misalnya `Semester 2`;
- `project_name`: harus diawali `<period_label> • `, misalnya `Semester 2 • AKM I`;
- `source_registries`: registry yang memang menjadi dependency pack;
- `eval_suites`: ordered suite `core → institution → program → pack` yang memang berlaku untuk pack;
- `focus`: deskripsi pendek setiap mata kuliah untuk site; jangan hardcode focus di front-end.

`id`, folder, atau versi internal boleh tetap ringkas seperti `.s2`, `semester-02/`, atau `2026-2027.s2.1`. Aturan label eksplisit berlaku untuk teks yang ditampilkan ke pengguna, bukan identifier mesin.

## Memilih scope eval

Jangan copy sebuah regression case hanya karena pack baru membutuhkan perilaku yang sama. Tempatkan case pada scope paling sempit yang masih benar-benar reusable:

- `core` → berlaku untuk semua pack Ramu, misalnya sitasi palsu atau prompt injection;
- `institution` → berlaku lintas program/periode pada satu institusi, misalnya aturan source governance Universitas Terbuka;
- `program` → berlaku lintas periode pada satu program, tetapi tidak otomatis untuk program lain;
- `pack` → membutuhkan mata kuliah/periode/course pack tertentu.

Setiap suite memiliki `suite_id`, `scope`, dan—selain core—`scope_ref`. File contracts dan behavior harus mendeklarasikan metadata yang sama dengan manifest. ID case harus unik setelah semua suite digabung; suite yang lebih spesifik **tidak mengganti** case milik suite sebelumnya.

Urutan di manifest harus dari umum ke spesifik. Contoh:

```text
core → institution:universitas-terbuka → pack:Semester-2
```

atau bila suatu hari ada rule khusus S1 Akuntansi lintas semester:

```text
core → institution:universitas-terbuka → program:s1-akuntansi → pack:Semester-3
```

Behavior `defaults` diproses berurutan, sehingga suite yang lebih spesifik boleh mengubah default runtime seperti threshold/token untuk case berikutnya. Perubahan default harus disengaja dan dijelaskan di PR.

## Memilih scope source

- `sources/registry.json` → global/runtime, misalnya dokumentasi platform;
- `packs/<institusi>/source-registry.json` → source institusi;
- registry program/pack → hanya bila source benar-benar lebih sempit.

ID source harus unik lintas seluruh registry. Source sekunder atau community signal tidak boleh diam-diam menjadi kanonik hanya karena berada di domain resmi.

## Validasi tanpa API

Gunakan Python 3.12 atau versi kompatibel:

```bash
python scripts/validate_repo.py
python scripts/validate_display_names.py
python scripts/validate_site.py
python scripts/check_source_freshness.py
python scripts/run_behavior_evals.py --dry-run --pack <pack-id>
```

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

Perubahan tidak dinilai dari panjang prompt atau dokumentasinya. Yang dicari adalah perilaku yang jelas, sumber yang dapat ditelusuri, manifest yang self-describing, label yang tidak membingungkan pengguna, setup yang mudah, dan cara nyata untuk menguji ulang perubahan tersebut.
