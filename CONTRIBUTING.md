# Berkontribusi ke Ramu

Terima kasih sudah ingin membantu Ramu. Kontribusi paling berguna adalah perubahan yang membuat perilaku belajar lebih dapat diuji, sumber lebih dapat dipercaya, setup lebih mudah, atau course pack lebih mudah dipelihara.

## Sebelum membuat perubahan

1. Jangan menambahkan BMP, modul, materi kuliah berbayar, kunci jawaban, atau dokumen lain yang tidak boleh didistribusikan ulang.
2. Untuk fakta akademik, prioritaskan sumber resmi dan catat sumbernya di `sources/registry.json` bila memang menjadi dependency paket.
3. Pisahkan fakta yang terverifikasi dari asumsi, pengalaman komunitas, atau keputusan desain.
4. Jangan mengunci runtime ke satu nama model AI. Model yang tersedia berubah dari waktu ke waktu; behavior Ramu harus diuji terhadap model yang dipilih saat eval dijalankan.

## Jalur kontribusi

- Perbaikan dokumentasi dan onboarding.
- Perbaikan protocol, Project Instructions, atau course pack.
- Sumber resmi yang berubah atau tidak lagi dapat diakses.
- Behavior eval baru untuk failure mode yang realistis.
- Perbaikan validator, source watcher, atau tooling eval.
- Course pack baru untuk program/semester lain yang sumbernya dapat diverifikasi.

## Validasi lokal

Gunakan Python 3.12 atau versi kompatibel, lalu jalankan:

```bash
python scripts/validate_repo.py
python scripts/run_behavior_evals.py --dry-run
python scripts/check_source_freshness.py
```

Behavior eval nyata memerlukan `OPENAI_API_KEY` dan model kandidat/judge yang dipilih secara eksplisit. Jangan memasukkan API key ke commit, issue, artifact, screenshot, atau log publik.

## Pull request

Buat PR sekecil mungkin dan jelaskan:

- masalah yang diperbaiki;
- file/perilaku yang berubah;
- sumber yang digunakan bila mengubah fakta akademik;
- cara memverifikasi perubahan;
- risiko atau hal yang belum diuji.

Jika perubahan menyentuh guardrail, source routing, state, atau perilaku tutor, tambahkan atau perbarui eval yang relevan bila memungkinkan.

## Prinsip review

Perubahan tidak dinilai dari seberapa panjang prompt atau dokumentasinya. Yang dicari adalah perilaku yang jelas, dapat ditelusuri ke sumber bila faktual, mudah dipakai mahasiswa, dan punya cara untuk diuji ulang.
