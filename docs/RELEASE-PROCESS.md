# Proses Release

Release diperlakukan sebagai snapshot yang bisa ditelusuri, bukan label yang ikut bergerak bersama `main`.

## Versi

Ramu memakai Semantic Versioning selama public beta:

- `0.x.0-beta` — perubahan fitur atau arsitektur yang cukup berarti;
- `0.x.y-beta` — perbaikan kompatibel tanpa perubahan kemampuan utama;
- release tanpa `-beta` baru layak dipertimbangkan setelah behavior validation dan pilot memberi evidence yang cukup.

Release yang sudah terbit:

- `v0.1.0-beta` — baseline public beta pertama;
- `v0.2.0-beta` — fondasi multi-pack, identity/schema validation, eval/security hardening, dan Pages yang gated oleh validation;
- `v0.2.1-beta` — patch website/UX dan setup copy;
- `v0.2.2-beta` — public-readiness cleanup, support surface, repository security, dan sinkronisasi release workflow.

Tag release yang sudah dipublikasikan tidak dipindahkan atau dipakai ulang. Perubahan setelah release tetap berada di `Unreleased` sampai versi berikutnya dibuat.

## Validation dan deployment

Setiap push ke `main` menjalankan **Validate Ramu**, termasuk perubahan dokumentasi dan workflow.

**Deploy Pages** berjalan setelah Validate Ramu selesai dan hanya deploy bila:

- upstream conclusion = `success`;
- upstream event = `push`;
- upstream branch = `main`.

Pages checkout `workflow_run.head_sha`. Dengan begitu commit yang diterbitkan adalah SHA yang memang baru lolos validation, bukan keadaan `main` lain yang kebetulan lebih baru saat deploy berjalan.

Dependency GitHub Actions dipin ke full commit SHA. Dependabot boleh membuka update, tetapi PR dependency tetap direview dan melewati validation seperti perubahan lain.

## Sebelum release

1. Pastikan target commit sudah ada di `main`.
2. Pastikan **Validate Ramu** hijau pada SHA tersebut.
3. Jika release menyentuh site/pack/schema yang dipublish, cek **Deploy Pages** downstream untuk SHA yang sama.
4. Pindahkan item `Unreleased` di `CHANGELOG.md` ke versi yang akan dirilis sebelum membuat tag.
5. Periksa tanggal review source. Jangan memperbarui `verified_at` hanya agar terlihat baru.
6. Tulis status behavior validation apa adanya. Static CI bukan bukti bahwa seluruh respons model sudah lolos.
7. API tidak wajib untuk public-beta release; manual validation dan status pilot tetap dicatat terpisah.
8. Review dependency PR yang relevan secara normal, jangan menahannya hanya demi membuat release terlihat bersih.

## Membuat release di GitHub

1. buka **Releases → Draft a new release**;
2. buat tag baru;
3. targetkan ke commit `main` yang sudah divalidasi;
4. pilih versi sesuai perubahan;
5. beri judul yang menjelaskan fokus release;
6. gunakan generated release notes sebagai bahan bantu bila berguna, lalu cocokkan dengan `CHANGELOG.md`;
7. tandai **Set as a pre-release** selama status masih public beta;
8. cek ulang notes sebelum publish.

Release immutability yang sudah digunakan sebaiknya tetap dipertahankan agar tag dan asset release tidak dapat berubah diam-diam.

## Setelah publish

1. pastikan tag menunjuk SHA yang benar;
2. bandingkan release lama dengan release baru;
3. cek status pre-release bila masih beta;
4. pastikan `CHANGELOG.md` punya section dan compare link yang sesuai;
5. simpan snapshot release notes di `docs/` bila memang perlu dirujuk dari repository;
6. jangan menaikkan status pack menjadi `verified` hanya karena release berhasil dibuat.

## Cara menulis klaim release

Klaim yang aman dan bisa diperiksa misalnya:

- static/schema/identity validation aktif;
- Pages deploy setelah validated main push;
- Manual Eval Kit tersedia;
- behavior contracts dan critical gates tersedia;
- source direview pada tanggal tertentu;
- pilot/manual validation dilakukan dengan cakupan yang disebutkan.

Hindari klaim seperti “semua jawaban akurat”, “prompt-injection proof”, “terbukti meningkatkan nilai”, atau “fully validated” tanpa evidence yang benar-benar mendukungnya.

## Automated Behavior Evals

Eval melalui OpenAI API tetap opsional. Bila digunakan:

- API key hanya disimpan sebagai repository secret;
- candidate dan judge dipilih saat run;
- candidate dan judge sebaiknya berbeda bila memungkinkan;
- hasil model judge tetap perlu sampling/review manusia;
- critical case harus lulus selain memenuhi aggregate threshold;
- failure yang reproducible masuk regression case.

Ketiadaan API key atau saldo tidak memblokir static validation, Manual Eval Kit, penggunaan normal, atau pilot.
