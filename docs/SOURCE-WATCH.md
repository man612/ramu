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

Saat ini halaman OpenAI Help Center pada registry global memakai policy advisory karena probe otomatis dapat menerima HTTP 403 walaupun source tetap dapat direview melalui jalur normal. Policy ini khusus untuk kualitas signal reachability, bukan penurunan standar evidence.

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
