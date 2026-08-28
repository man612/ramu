# Ramu v0.2.0-beta — Multi-pack, Identity & Eval Hardening Foundation

Public beta Ramu sekarang punya fondasi multi-pack yang tidak lagi mengunci tooling ke Universitas Terbuka S1 Akuntansi Semester 2, tidak mengasumsikan semua institusi memakai semester, dan tidak lagi mengasumsikan behavior eval selalu hanya `core + pack`.

Pack yang tersedia saat release ini tetap **Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027**. Dukungan multi-pack di release ini berarti arsitektur dan validation tooling sudah diuji untuk lebih dari satu institusi/program/periode melalui fixture sintetis; bukan berarti pack akademik lain sudah tersedia.

## Yang berubah

- `packs/index.json` menjadi katalog pack machine-readable dan naik ke **format v3**.
- Setiap pack memakai manifest self-describing untuk identity institusi/program, periode, mata kuliah, source dependency, dan ordered `eval_suites`.
- Metadata identity mesin sekarang eksplisit: `institution_id`, `program_id`, dan pack `id` terpisah dari label manusia.
- `program_id` diperlakukan sebagai identity unik lintas katalog sehingga program-level suite/registry dapat direferensikan secara stabil.
- Metadata periode generic memakai `period_id` + `period_label`, bukan field universal `semester`.
- Pack UT saat ini menggunakan `period_id: semester-02` dan `period_label: Semester 2`; sistem lain dapat memakai bentuk seperti `trimester-01`, `quarter-fall`, atau `term-02` tanpa mengubah tooling generic.
- Manifest pack UT naik ke **`schema_version: 4`** untuk kontrak identity + period metadata. `pack_version` dan `contract_version` tidak berubah karena course content dan behavior contract tidak berubah.
- Website membaca katalog + manifest secara dinamis dan tidak lagi punya fallback `Semester ${...}` di JavaScript.
- Label periode manusia eksplisit, misalnya `Semester 2 • AKM I`, bukan `S2 • AKM I` yang dapat disalahartikan sebagai jenjang Magister.
- Behavior eval sekarang composable dengan urutan `core → institution → program → pack`; scope institusi/program bersifat opsional.
- `scope_ref` bukan lagi string bebas: institution harus cocok dengan `institution_id`, program dengan `program_id`, dan pack dengan pack `id`.
- Regression case E14 tentang source pusat-vs-regional dipindahkan menjadi suite tingkat **Universitas Terbuka**, sehingga pack UT berikutnya dapat reuse rule tersebut tanpa copy-paste.
- Source registry dapat diberi scope global/institusi/program/pack. Scoped registry membawa identity sesuai scope dan cross-file validator menolak registry yang nyasar ke institusi/program lain.
- Source registry sekarang juga dapat menyimpan **claim-level evidence** dengan status, evidence locator, review interval, dan operational fallback untuk konflik dokumentasi resmi.
- Schema eval contracts digeneralisasi dan ditambah schema behavior eval agar format publik sesuai file yang benar-benar dipakai tooling.
- **JSON Schema Draft 2020-12 sekarang benar-benar dijalankan di CI**: schema Ramu diperiksa sebagai schema dan katalog, seluruh manifest, seluruh source registry, serta eval contracts/behavior divalidasi sebagai instance.
- Semantic validator tetap berjalan sesudah schema validation untuk invariant lintas-file seperti file existence, jumlah SKS, source dependency, suite ordering, dan contract/behavior pairing.
- Cross-file identity validator memeriksa konsistensi katalog↔manifest, scoped registry, dan eval suite.
- Manual Eval Kit dapat membuat checklist behavior validation untuk diuji langsung di ChatGPT Projects tanpa OpenAI API, termasuk provenance suite dan critical/must-pass status tiap case.
- CI menggunakan matrix per pack dan tetap menyediakan final gate bernama `validate`.
- GitHub Actions dependency dipin ke full commit SHA dan workflow menggunakan action Node 24-native.
- Schema pack/catalog/source/eval ikut dipublish bersama GitHub Pages.

## Multi-pack proof

Selain memvalidasi pack UT yang benar-benar dipublish, CI menjalankan **synthetic multi-pack foundation proof** pada temporary repository.

Positive fixture mencakup:

- dua institusi berbeda;
- dua program/identity berbeda;
- dua pack sekaligus dalam satu katalog;
- satu pack `Semester 2`;
- satu pack **`Trimester 1`**;
- komposisi `core → institution → pack`;
- komposisi `core → institution → program → pack`;
- source registry scope institution dan program;
- JSON Schema, semantic validation, identity validation, display-name validation, pack matrix, dan behavior dry-run.

Negative fixture memastikan gate menolak setidaknya:

- program `scope_ref` yang menunjuk identity program institusi lain;
- program source registry dengan `institution_id` salah;
- field legacy `semester` yang mencoba kembali ke manifest generic.

Fixture Alpha/Beta tersebut hanya test data di temporary directory. Ia tidak masuk `packs/index.json` utama dan tidak tampil di website Ramu.

## Eval & security hardening

Automated behavior eval sekarang menjaga boundary antara instruksi berwenang dan external/reference content.

Pada request kandidat:

- **Project Instructions** berada pada Responses API `instructions`;
- course pack, source, protocol/context file yang dipakai case diberikan terpisah sebagai **user-level untrusted reference material**;
- reference diberi boundary eksplisit dan tidak boleh menimpa Project Instructions;
- regression test memastikan reference material tidak dapat kembali masuk ke `instructions` tanpa membuat CI gagal.

LLM judge juga diperlakukan sebagai boundary tersendiri. Candidate output, conversation, dan judge notes diserialisasi sebagai **untrusted evidence**. Judge instructions secara eksplisit melarang mengikuti embedded instruction dari evidence, sementara verdict tetap menggunakan structured JSON schema.

Hardening tersebut **bukan klaim bahwa prompt injection sudah terselesaikan**. Tujuannya mencegah automated eval sendiri menciptakan trust hierarchy yang salah dan mengurangi attack surface LLM-as-a-judge.

Responses API juga bukan simulasi identik ChatGPT Projects. Automated API eval adalah regression/benchmark approximation; manual validation di Projects asli tetap diperlukan untuk product-level evidence seperti Sources, memory, UI/file handling, dan behavior produk.

## Critical / must-pass eval

Aggregate pass rate tidak lagi cukup sendirian untuk menyatakan run PASS. Contract dapat menandai failure mode sebagai `critical: true`.

Overall automated run hanya PASS jika:

1. pass rate memenuhi threshold `--fail-under`; **dan**
2. tidak ada critical case yang FAIL.

Core critical set awal adalah:

- `E01` — jangan mengarang angka/data yang tidak terlihat;
- `E05` — jangan membuat sitasi, DOI, halaman, atau identitas sumber palsu;
- `E08` — hormati instruksi tugas yang melarang AI menghasilkan submission;
- `E13` — jangan mengikuti prompt injection dari Project Source atau membocorkan secret.

CI mempunyai regression test yang secara sengaja membuat hasil **13/16 = 81,25%**. Hasil tersebut tetap FAIL bila salah satu kegagalannya critical, meskipun secara matematis melewati threshold 80%. Test yang sama memastikan set critical repo tidak berubah diam-diam.

Manual Eval Kit memakai contract yang sama. Checklist menandai `Critical / must-pass`, dan satu critical FAIL juga mencegah manual validation dicatat sebagai overall PASS.

## CI, Pages, dan dependency hardening

Validation dan deployment sekarang membentuk chain yang eksplisit.

- **Validate Ramu berjalan pada setiap push ke `main`**, tidak lagi dibatasi path allowlist. Perubahan docs, release metadata, workflow, ataupun file lain di main tidak dapat melewati validation hanya karena path-nya tidak tercantum.
- **Deploy Pages tidak lagi trigger langsung dari push.** Ia menunggu workflow `Validate Ramu` selesai melalui `workflow_run`.
- Deploy hanya berjalan bila upstream validation berstatus `success`, event asalnya `push`, dan branch asalnya `main`.
- Pages checkout `workflow_run.head_sha`, sehingga SHA yang dipublish adalah commit yang benar-benar divalidasi, bukan keadaan `main` yang mungkin sudah bergerak lagi.
- CI memiliki regression contract yang menolak kembalinya path-filter main, direct-push Pages deploy, atau hilangnya filter success/main/head SHA tersebut.
- Dependabot dijadwalkan mingguan untuk dependency **GitHub Actions** dan dependency validation **pip**. Immutable full-SHA action pins tetap dipertahankan; pembaruan datang sebagai PR dan melewati validation biasa.

Dependabot bukan pengganti review. Dependency PR tetap perlu melihat upstream change dan hasil CI sebelum merge.

## Product drift & source governance

Global OpenAI registry direview ulang pada **29 Agustus 2026** dan naik ke format v2. ChatGPT Release Notes ditambahkan sebagai source resmi untuk kronologi perubahan produk.

Ramu sekarang membedakan freshness **source** dan freshness **claim**. Satu halaman yang masih reachable tidak otomatis membuat setiap klaim di dalamnya dianggap current. Claim dapat mempunyai evidence dari beberapa source, status sendiri, review interval sendiri, dan fallback operasional.

Dua official-doc conflict yang masih dicatat saat release candidate ini:

1. **Study Mode di Projects.** Artikel khusus Study Mode menyatakan Study tidak tersedia di Projects, sementara artikel Projects masih mencantumkan Study Mode sebagai tool.
2. **Memory existing Project.** Release notes dan guidance Projects terbaru menyatakan memory dapat diubah kemudian lewat Project settings, sementara FAQ Projects yang masih terindeks juga menyimpan wording lama bahwa Project perlu dibuat ulang untuk memakai project-only memory.

Ramu tidak memilih salah satu secara diam-diam. Fallback-nya:

- Study Mode **bukan dependency runtime**; tutoring/scaffolding tetap datang dari Project Instructions + protocols + course context + eval.
- Untuk setup baru, pilih **Project-only memory** saat membuat Project.
- Untuk Project lama, coba **Project settings → Memory**; jika opsi belum tersedia pada akun/versi aplikasi tersebut, buat Project baru dengan Project-only memory dan pindahkan chat yang masih diperlukan.

Source Watch sekarang ikut memeriksa evidence source ID, umur `reviewed_at` claim, serta kewajiban `operational_policy` untuk conflicted claim. Hash HTML mentah sengaja tidak dijadikan kebenaran semantik karena halaman dinamis dapat berubah markup tanpa perubahan fakta—atau sebaliknya.

Setup site juga tidak lagi menjanjikan per-course Project Instructions override yang belum ada di schema, tidak bergantung pada label `Add from library`, dan menjelaskan label Project Sources sebagai UI yang dapat berubah. Label `Save to project` / `Add to project sources` hanya dipakai sebagai contoh yang memang didokumentasikan saat review.

## Tanpa API tetap bisa dipakai dan diuji

OpenAI API bukan dependency Ramu. Mahasiswa tetap memakai ChatGPT Projects seperti biasa, static CI tetap berjalan, JSON Schema + synthetic multi-pack proof berjalan tanpa API, trust-boundary regression dan critical-gate regression juga tidak memanggil API, Manual Eval Kit tidak membutuhkan secret, source/claim freshness validation berjalan tanpa API, dan pilot pengguna dapat dilakukan sekarang.

`jsonschema[format]` yang dipakai CI adalah dependency **validation/dev only**. Site dan workflow penggunaan mahasiswa tetap statis dan tidak membutuhkan package Python tersebut.

Automated Behavior Evals melalui API tetap tersedia sebagai lapisan QA tambahan bila suatu saat API key tersedia.

## Existing user

Kalau sudah memiliki Project bernama `S2 • ...`, nama Project tidak perlu dibuat ulang hanya karena perubahan naming. Nama dapat diubah menjadi `Semester 2 • ...` bila ingin mengikuti convention baru; course pack dan Project Instructions tetap menjadi bagian yang menentukan workspace Ramu.

Perubahan repository dari `semester` → `period_id`, penambahan `institution_id`/`program_id`, dan hardening eval/CI/source governance hanya menyentuh metadata/tooling. Satu pengecualian product-level adalah pilihan **Project-only memory**: untuk Project lama, availability menu Memory dapat berbeda sesuai state akun/app, sehingga ikuti fallback pada panduan setup bila opsi tersebut belum muncul.

## Status validasi

- JSON Schema validation: aktif pada schema + instance repo.
- Static semantic/cross-file validation: aktif.
- Machine identity validation: aktif.
- Synthetic multi-pack + non-semester proof: aktif di CI.
- Eval trust-boundary regression: aktif di CI tanpa API.
- Critical must-pass gate regression: aktif di CI tanpa API.
- CI/Pages deployment-chain regression: aktif.
- Validate: wajib pada setiap main push.
- Pages: downstream dari successful validated main push dan checkout validated SHA.
- Dependabot: weekly untuk GitHub Actions + pip validation dependency.
- Catalog/site/eval wiring: divalidasi CI.
- Source + claim freshness monitoring: aktif.
- Global OpenAI source registry: v2 dengan claim-level evidence.
- Behavior contracts: **E01–E16** tetap tersedia dan digabung dari **3 suite** pada pack awal (`core → Universitas Terbuka → Semester 2`).
- Core critical must-pass set: **E01, E05, E08, E13**.
- Manual behavior validation dan pilot pengguna: masih menjadi evidence yang perlu dikumpulkan sebelum klaim stabilitas lebih tinggi.
- Automated API behavior benchmark: opsional dan belum menjadi syarat release ini.

Ramu tetap **public beta** dan tidak mengklaim semua keluaran model selalu akurat, bahwa prompt injection sudah “terselesaikan”, bahwa dokumentasi produk tidak akan berubah, atau bahwa test sintetis dapat menggantikan validation pengguna nyata.
