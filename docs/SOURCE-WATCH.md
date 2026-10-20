# Source Freshness Watch

Source Watch menjaga dua hal yang berbeda dan sengaja tidak menyamakannya:

1. **freshness semantik** — kapan source atau claim terakhir benar-benar direview;
2. **reachability** — apakah URL dapat dijangkau oleh probe otomatis saat workflow berjalan.

URL yang hidup tidak membuktikan isi masih current. Sebaliknya, kegagalan probe otomatis juga tidak otomatis berarti isi source berubah atau source hilang.

## Freshness semantik

`verified_at` pada source dan `reviewed_at` pada claim dibandingkan dengan `review_interval_days`.

Jika source aktif atau claim non-deprecated melewati intervalnya, Source Watch gagal dan meminta review. Tanggal hanya diperbarui setelah evidence benar-benar dibaca kembali; jangan memperbaruinya hanya agar workflow hijau.

## Reachability policy

Watched source dapat memakai field opsional:

```json
"reachability_policy": "strict"
```

atau:

```json
"reachability_policy": "advisory"
```

Jika field tidak ada, policy default tetap **`strict`** agar source lama tidak diam-diam menjadi lebih permisif.

### `strict`

Gunakan bila kegagalan URL dari environment GitHub Actions memang cukup kuat untuk dianggap kondisi yang perlu ditinjau.

Setelah retry habis, kegagalan strict:

- muncul di diagnostics;
- membuat `--fail-on-network` exit non-zero;
- dapat membuka/memperbarui issue Source Watch.

### `advisory`

Gunakan untuk source yang sah tetapi diketahui dapat menolak bot/HEAD/automated request, sehingga reachability dari GitHub Actions bukan indikator yang cukup andal.

Setelah retry habis, kegagalan advisory:

- tetap muncul sebagai `URL INCONCLUSIVE` di diagnostics;
- tidak membuat workflow gagal hanya karena reachability;
- tidak membuka issue hanya karena probe tersebut;
- **tidak** memperpanjang `verified_at` atau `reviewed_at`;
- **tidak** menganggap claim masih benar secara otomatis.

Halaman OpenAI Help Center pada registry global memakai policy advisory setelah probe GitHub Actions berulang kali menerima HTTP 403 sepanjang September–Oktober 2026, sementara halaman resmi dapat diperiksa melalui jalur web biasa. Hal ini bukan bukti kontennya tidak berubah: verifikasi semantik tetap wajib dan tanggal review tidak boleh diperpanjang otomatis.

## Bedakan validasi pull request dan Source Watch

- **Validate Ramu** (`pull_request`/push ke main) menjalankan `python scripts/check_source_freshness.py --report-only-overdue`. Keterlambatan review source/claim tetap tercetak sebagai `REVIEW REQUIRED`, tetapi tidak memblokir perubahan kode yang sehat. Metadata tidak valid, ID duplikat, atau claim yang mengacu ke source tidak dikenal tetap menjadi error.
- **Source Freshness Watch** (mingguan/manual) tetap menjalankan `--online --fail-on-network` tanpa `--report-only-overdue`. Source/claim overdue dan kegagalan strict network tetap meminta review melalui issue dan membuat job gagal.
- Pengubahan sumber atau status pack tetap membutuhkan verifikasi evidence manusia sebelum status `source-verified`/`verified` dinaikkan. CI hijau sendiri tidak menjamin semua fakta source mutakhir.
- Pada 19 Oktober 2026, banyak URL UT memperoleh `URLError` dalam run yang sama. Cari penyebab jaringan runner sebelum menganggap semua sumber tersebut mati.

## Retry

Probe mencoba sampai tiga kali dengan jeda terbatas. Tujuannya menyerap kegagalan jaringan sesaat tanpa mengabaikan failure yang konsisten.

`HEAD` digunakan lebih dulu. Untuk response tertentu seperti 403/405, checker mencoba request `GET` ringan sebagai fallback. Hasil akhir tetap tunduk pada `reachability_policy` source.

## Menjalankan lokal

Freshness tanpa network:

```bash
python scripts/check_source_freshness.py
```

Freshness + reachability:

```bash
python scripts/check_source_freshness.py --online
```

Mode yang juga memblokir strict network failure:

```bash
python scripts/check_source_freshness.py --online --fail-on-network
```

Regression test retry/policy tidak membutuhkan akses internet:

```bash
python tests/test_source_freshness_probe.py
```

## Kapan mengubah policy?

Jangan mengubah `strict` menjadi `advisory` hanya untuk menghilangkan workflow merah. Ubah policy bila ada evidence bahwa automated reachability dari CI memang bukan signal yang stabil untuk source tersebut.

Jika source sebelumnya advisory mulai menyediakan endpoint yang stabil untuk automated probe, policy boleh dikembalikan ke strict setelah perilakunya diverifikasi.
