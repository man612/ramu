# Proses Release Ramu

Dokumen ini menjaga agar release Ramu menjadi snapshot yang dapat ditelusuri, bukan sekadar label yang dipindahkan mengikuti `main`.

## Prinsip versi

Ramu mengikuti Semantic Versioning sebagai bahasa perubahan:

- `0.x.0-beta` — perubahan fitur/arsitektur yang cukup berarti selama public beta;
- `0.x.y-beta` — perbaikan kompatibel yang tidak mengubah kemampuan utama;
- release tanpa `-beta` hanya dipertimbangkan setelah behavior validation dan pilot pengguna memberi evidence yang cukup.

Contoh saat ini:

- `v0.1.0-beta` = public-beta baseline pertama;
- `v0.2.0-beta` = kandidat untuk fondasi multi-pack + no-API manual validation + catalog-driven site.

Jangan memindahkan tag release yang sudah dipublikasikan agar menunjuk commit baru. Jika code berubah setelah release, buat versi baru.

## Sebelum membuat release

1. Pastikan target commit sudah berada di `main`.
2. Pastikan workflow **Validate Ramu** hijau pada commit tersebut.
3. Pastikan **Deploy Pages** hijau bila perubahan menyentuh site/pack/schema yang dipublish.
4. Periksa `CHANGELOG.md` dan pindahkan item `Unreleased` ke versi yang akan dirilis.
5. Periksa source review date. Jangan mengubah `verified_at` hanya supaya terlihat baru; tanggal harus mencerminkan review manusia sungguhan.
6. Pastikan status behavior validation ditulis apa adanya. Static CI tidak sama dengan bukti bahwa semua respons model lolos.
7. API **tidak wajib** untuk membuat public-beta release. Manual validation di ChatGPT Projects dan status pilot harus tetap dijelaskan terpisah.

## Membuat release di GitHub

Dari repository:

1. buka **Releases → Draft a new release**;
2. buat **tag baru**, jangan reuse/memindahkan tag release lama;
3. targetkan tag ke commit `main` yang sudah divalidasi;
4. gunakan versi Semantic Versioning, misalnya `v0.2.0-beta`;
5. beri judul yang menjelaskan fokus release;
6. gunakan generated release notes sebagai bahan bantu bila berguna, lalu kurasi terhadap `CHANGELOG.md`;
7. tandai **Set as a pre-release** selama status Ramu masih public beta;
8. cek ulang seluruh release notes sebelum publish.

Jika GitHub menyediakan **release immutability** pada repository, aktifkan sebelum release berikutnya melalui repository Settings. Release immutable mengunci tag dan asset release setelah dipublikasikan, sehingga snapshot tidak dapat diubah diam-diam.

## Setelah publish

1. buka tag release dan pastikan SHA-nya sama dengan commit `main` yang memang diniatkan;
2. bandingkan release lama → release baru dan pastikan perubahan penting tercakup di notes;
3. cek bahwa release berstatus pre-release bila masih beta;
4. update link/version di `CHANGELOG.md` bila belum dilakukan pada commit release;
5. jangan menaikkan status pack menjadi `verified` hanya karena release berhasil dibuat.

## Aturan klaim

Release notes boleh mengatakan:

- static validation aktif;
- Manual Eval Kit tersedia;
- behavior contracts tersedia;
- source telah direview pada tanggal tertentu;
- pilot/manual validation sedang atau sudah dilakukan dengan cakupan yang disebutkan.

Release notes jangan mengatakan:

- “semua jawaban akurat”;
- “prompt-injection proof”;
- “terbukti meningkatkan nilai”;
- “fully validated”;

kecuali benar-benar ada evidence yang sesuai dengan klaim tersebut.

## Automated Behavior Evals

Automated eval melalui OpenAI API tetap opsional. Bila digunakan:

- API key hanya disimpan sebagai repository secret;
- candidate dan judge dipilih saat run;
- sebisa mungkin candidate dan judge berbeda;
- hasil model judge tetap perlu sampling/review manusia;
- kegagalan yang reproducible diubah menjadi regression case.

Tidak adanya saldo/API key tidak boleh memblokir static validation, Manual Eval Kit, penggunaan Ramu, atau pilot pengguna.
