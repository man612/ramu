# Kebijakan Freshness Sumber

Registry sumber ada di [`registry.json`](registry.json). Tujuannya bukan menganggap URL yang hidup pasti benar, tetapi memastikan Ramu tahu **kapan sebuah klaim perlu diperiksa ulang**.

## Kelas freshness

- `academic-year` — dokumen resmi yang berlaku untuk tahun akademik tertentu. Periksa berkala dan setiap kali ada edisi baru.
- `institution-page` — halaman institusi yang dapat diperbarui tanpa perubahan URL.
- `product-current` — dokumentasi produk yang dapat berubah sewaktu-waktu; interval review lebih pendek.
- `regional-page` — sumber resmi regional yang dapat tertinggal dari sumber pusat.
- `community-signal` — hanya untuk menemukan pola masalah/UX, bukan sumber aturan.

## Arti status

- `active` — dapat dipakai sesuai fungsi `canonical_for`;
- `secondary` — sumber pelengkap, bukan sumber kanonik;
- `signal-only` — tidak boleh dipakai sebagai dasar aturan akademik.

## Source watch

Workflow mingguan menjalankan pemeriksaan:

1. format registry valid;
2. tanggal verifikasi belum melewati interval review;
3. untuk sumber dengan `watch: true`, URL dicoba diakses;
4. kegagalan jaringan dicatat sebagai warning, bukan otomatis dianggap perubahan fakta;
5. jika review sudah jatuh tempo, workflow gagal agar maintainer mendapat sinyal untuk verifikasi manual.

Ramu sengaja tidak menganggap perubahan HTML/hash sebagai bukti bahwa fakta akademik berubah. Dokumen baru tetap harus dibaca dan dibandingkan sebelum pack diubah.
