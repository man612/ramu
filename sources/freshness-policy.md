# Kebijakan Freshness Sumber

Ramu memakai **scoped source registry**, bukan satu registry untuk semua institusi selamanya.

- `sources/registry.json` — source global/runtime, misalnya dokumentasi platform AI;
- `packs/<institusi>/source-registry.json` — source institusi;
- registry level program/pack boleh ditambahkan ketika dibutuhkan.

Setiap pack menyebut registry yang menjadi dependency-nya lewat `source_registries` di `manifest.json`. Tujuannya bukan menganggap URL yang hidup pasti benar, tetapi memastikan Ramu tahu **sumber mana yang berwenang, untuk fungsi apa, klaim apa yang sedang bergantung padanya, dan kapan klaim tersebut perlu diperiksa ulang**.

## Kelas freshness

- `academic-year` — dokumen resmi yang berlaku untuk tahun akademik tertentu. Periksa berkala dan setiap kali ada edisi baru.
- `institution-page` — halaman institusi yang dapat diperbarui tanpa perubahan URL.
- `product-current` — dokumentasi produk yang dapat berubah cepat; interval review lebih pendek.
- `regional-page` — sumber resmi regional yang dapat tertinggal dari sumber pusat.
- `community-signal` — hanya untuk menemukan pola masalah/UX, bukan sumber aturan.

## Arti status source

- `active` — dapat dipakai sesuai fungsi `canonical_for`;
- `secondary` — sumber pelengkap, bukan sumber kanonik untuk klaim yang sudah punya canonical source;
- `signal-only` — tidak boleh dipakai sebagai dasar aturan akademik.

## Claim-level evidence

Satu halaman resmi dapat berubah sebagian, memuat wording lama di FAQ, atau bahkan bertentangan dengan release notes resmi. Karena itu registry dapat memiliki `claims` terpisah dari daftar `sources`.

Setiap claim menyimpan:

- `status`: `confirmed`, `conflicted`, `needs-review`, atau `deprecated`;
- `evidence`: source ID + locator/bagian dokumen + observation yang benar-benar ditemukan saat review;
- `reviewed_at` dan `review_interval_days` sendiri;
- `operational_policy` ketika statusnya `conflicted`, supaya UX/runtime Ramu tetap punya perilaku aman sementara dokumentasi belum konsisten.

`conflicted` **bukan berarti salah satu source otomatis salah**. Artinya maintainer belum mempunyai dasar cukup kuat untuk menyatukan dua guidance yang berbeda menjadi satu klaim pasti. Ramu memilih fallback yang tidak membuat fungsi inti bergantung pada detail produk tersebut.

Contoh: bila satu artikel produk mengatakan fitur tersedia di Projects sementara artikel fitur khusus mengatakan sebaliknya, Ramu tidak boleh diam-diam memilih versi yang paling nyaman. Konflik dicatat sebagai claim, evidence keduanya disimpan, lalu workflow pengguna dibuat tetap berfungsi tanpa dependency pada fitur itu.

## Source watch

Workflow mingguan menemukan seluruh `sources/registry.json` dan `packs/**/source-registry.json`, lalu memeriksa:

1. ID source tidak duplikat lintas registry;
2. tanggal verifikasi source belum melewati interval review;
3. untuk source dengan `watch: true`, URL dicoba diakses;
4. kegagalan jaringan dicatat terpisah dari perubahan fakta;
5. setiap claim menunjuk source ID yang benar;
6. claim conflicted wajib punya fallback `operational_policy`;
7. tanggal review claim belum melewati interval review;
8. source atau claim yang overdue membuat workflow meminta review.

Ramu sengaja **tidak memakai hash HTML mentah sebagai kebenaran semantik**. Halaman web dinamis dapat berubah karena navigasi, timestamp, personalisasi, atau markup tanpa perubahan klaim. Sebaliknya, URL yang tidak berubah juga dapat menyimpan fakta yang sudah direvisi. Maintainer tetap harus membaca evidence yang relevan dan memperbarui `verified_at`/`reviewed_at` hanya setelah review nyata.
