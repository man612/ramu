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

## Source-watch retry proof

`python tests/test_source_freshness_probe.py` menguji reachability probe tanpa akses jaringan nyata. Test memastikan:

- kegagalan sesaat dapat pulih pada attempt berikutnya;
- jeda retry tetap terbatas dan deterministik;
- kegagalan yang bertahan sampai attempt terakhir tetap dianggap gagal;
- source yang langsung reachable tidak melakukan retry yang tidak perlu.

Test ini menjaga supaya hardening terhadap false alarm tidak berubah menjadi mekanisme yang diam-diam mengabaikan source yang benar-benar tidak dapat dijangkau.
