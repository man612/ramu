# Berkontribusi ke Ramu

Terima kasih sudah ingin membantu Ramu. Kontribusi paling berguna adalah perubahan yang membuat perilaku belajar lebih dapat diuji, sumber lebih dapat dipercaya, setup lebih mudah, atau pack lebih mudah dipelihara.

## Sebelum membuat perubahan

1. Jangan menambahkan BMP, modul, materi kuliah berbayar, kunci jawaban, atau dokumen lain yang tidak boleh didistribusikan ulang.
2. Untuk fakta akademik, prioritaskan sumber resmi dan masukkan source ke registry dengan scope yang tepat.
3. Pisahkan fakta terverifikasi dari asumsi, pengalaman komunitas, dan keputusan desain.
4. Jangan mengunci runtime ke satu nama model AI. Model/plan dapat berubah; kontrak Ramu harus tetap masuk akal ketika model berganti.
5. Jangan menyebut pack Ramu sebagai pack “resmi” dari universitas. Gunakan `maintainer: ramu` (Ramu Maintained) atau `maintainer: community`.

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

1. buat struktur `packs/<institusi>/<program>/<tahun>/<semester>/`;
2. buat `manifest.json` mengikuti `schemas/pack-manifest.schema.json`;
3. taruh course pack di folder `courses/` dan Project Instructions di pack tersebut;
4. pakai registry yang sudah ada atau buat scoped `source-registry.json` jika source-nya belum punya tempat yang tepat;
5. buat eval khusus pack di `<pack>/evals/contracts.json` dan `<pack>/evals/behavior.json`;
6. jangan copy eval universal tanpa alasan—failure mode umum berasal dari `evals/core/`;
7. daftarkan pack di `packs/index.json`;
8. jalankan validasi. Validator akan gagal jika menemukan `manifest.json` yang belum masuk katalog atau entry katalog yang menunjuk file yang tidak ada.

Field penting:

- `status`: `source-verified`, `verified`, `community`, `experimental`, atau `deprecated`;
- `maintainer`: `ramu` atau `community`;
- `source_registries`: registry yang memang menjadi dependency pack;
- `evals`: lokasi core + pack eval yang harus digabung runner;
- `focus`: deskripsi pendek setiap mata kuliah untuk site; jangan hardcode focus di front-end.

## Memilih scope source

- `sources/registry.json` → global/runtime, misalnya dokumentasi platform;
- `packs/<institusi>/source-registry.json` → source institusi;
- registry program/pack → hanya bila source benar-benar lebih sempit.

ID source harus unik lintas seluruh registry. Source sekunder atau community signal tidak boleh diam-diam menjadi kanonik hanya karena berada di domain resmi.

## Validasi tanpa API

Gunakan Python 3.12 atau versi kompatibel:

```bash
python scripts/validate_repo.py
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
- pack/core yang terpengaruh;
- source yang digunakan bila mengubah fakta akademik;
- cara memverifikasi perubahan;
- risiko atau hal yang belum diuji.

Jika perubahan menyentuh guardrail, source routing, state, atau perilaku tutor, tambahkan/perbarui eval yang relevan. Jika failure mode berlaku untuk semua pack, tempatkan kontraknya di core; bila spesifik institusi/mata kuliah, tempatkan dekat pack.

## Prinsip review

Perubahan tidak dinilai dari panjang prompt atau dokumentasinya. Yang dicari adalah perilaku yang jelas, sumber yang dapat ditelusuri, manifest yang self-describing, setup yang mudah, dan cara yang nyata untuk menguji ulang perubahan tersebut.
