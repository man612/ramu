# Tests

Folder ini berisi regression/proof test untuk **tooling Ramu**, bukan pack akademik pengguna.

## Multi-pack foundation proof

`python tests/test_multipack_foundation.py` membangun repository sintetis di temporary directory lalu menjalankan validator Ramu yang asli melalui `RAMU_REPO_ROOT`.

Fixture positif sengaja mencakup:

- dua institusi berbeda;
- dua `institution_id` dan `program_id` berbeda;
- dua pack sekaligus dalam katalog;
- satu periode `Semester 2`;
- satu periode non-semester `Trimester 1`;
- komposisi `core → institution → pack`;
- komposisi `core → institution → program → pack`;
- source registry scope institution dan program;
- JSON Schema validation, semantic validation, identity validation, display-name validation, pack matrix, dan behavior dry-run.

Fixture negatif memastikan gate menolak setidaknya:

- `scope_ref` program yang menunjuk program milik institusi lain;
- program source registry dengan `institution_id` yang salah;
- field legacy `semester` pada manifest generic.

Data Alpha/Beta dalam test adalah **synthetic fixture**, bukan institusi atau pack Ramu yang dipublish. Fixture tidak ditambahkan ke `packs/index.json` repository utama dan tidak muncul di site.

`RAMU_REPO_ROOT` adalah override khusus tooling/test agar script validation yang sama dapat diarahkan ke repository fixture. Penggunaan normal tetap memakai root repository aktual secara otomatis.

## Source-watch retry dan reachability policy

`python tests/test_source_freshness_probe.py` menguji reachability probe tanpa akses jaringan nyata. Test memastikan:

- kegagalan sesaat dapat pulih pada attempt berikutnya;
- jeda retry tetap terbatas dan deterministik;
- kegagalan yang bertahan sampai attempt terakhir tetap dianggap gagal;
- source yang langsung reachable tidak melakukan retry yang tidak perlu;
- source lama tanpa policy eksplisit tetap `strict`;
- `advisory` tetap menjadi signal non-blocking;
- policy yang tidak dikenal ditolak.

Test ini menjaga supaya hardening terhadap false alarm tidak berubah menjadi mekanisme yang diam-diam mengabaikan source yang benar-benar perlu dipantau.

## Starter dan pack builder

`python tests/test_starter_builder.py` menguji generator personal Starter di temporary directory: artefak wajib, default nama Project, trust marker `public_pack: false`/`source_verified: false`, perlindungan overwrite, dan mode non-interaktif.

`python tests/test_pack_builder.py` menguji scaffold community pack dengan periode non-semester. Test menjaga agar draft selalu mulai sebagai `experimental` + `community`, total SKS dan identity konsisten, eval tidak dikarang otomatis, output tidak dioverwrite tanpa `--force`, dan input berisiko seperti URL non-HTTPS, machine ID tidak valid, atau tanggal review masa depan ditolak.

## Browser-level site regression

`python tests/test_site_browser.py` menjalankan Chromium melalui Playwright terhadap staging lokal yang disusun seperti artifact GitHub Pages. Cakupannya sengaja menguji behavior yang tidak dapat dibuktikan hanya dengan mencari marker HTML/JavaScript:

- render katalog dan manifest aktif;
- keyboard behavior custom pack picker;
- perpindahan pack melalui query string;
- fallback untuk pack ID yang tidak dikenal;
- render setup per course;
- persistensi progress `localStorage`;
- Project Instructions dapat diambil;
- download course pack benar-benar terpicu;
- kegagalan write `localStorage` tidak memecahkan interaksi halaman.

Untuk menjalankannya lokal:

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python tests/test_site_browser.py
```

CI memasang Chromium beserta system dependencies dan menjadikan browser job bagian dari required `validate` gate.
