# Kebijakan Freshness Sumber

Ramu memakai **scoped source registry**, bukan satu registry untuk semua institusi selamanya.

- `sources/registry.json` — source global/runtime, misalnya dokumentasi platform AI;
- `packs/<institusi>/source-registry.json` — source institusi;
- registry level program/pack boleh ditambahkan ketika dibutuhkan.

Setiap pack menyebut registry yang menjadi dependency-nya lewat `source_registries` di `manifest.json`. Tujuannya bukan menganggap URL yang hidup pasti benar, tetapi memastikan Ramu tahu **sumber mana yang berwenang, untuk fungsi apa, dan kapan klaimnya perlu diperiksa ulang**.

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

## Source watch

Workflow mingguan menemukan seluruh `sources/registry.json` dan `packs/**/source-registry.json`, lalu memeriksa:

1. ID source tidak duplikat lintas registry;
2. tanggal verifikasi belum melewati interval review;
3. untuk source dengan `watch: true`, URL dicoba diakses;
4. kegagalan jaringan dicatat terpisah dari perubahan fakta;
5. source aktif yang overdue atau watched URL yang gagal sesuai gate akan membuat workflow meminta review.

Ramu sengaja tidak menganggap perubahan HTML/hash atau kegagalan reachability sebagai bukti otomatis bahwa fakta akademik berubah. Maintainer tetap harus membaca, membandingkan, dan memperbarui `verified_at` hanya setelah verifikasi nyata.
