## Masalah

<!-- Masalah apa yang diperbaiki? -->

## Perubahan

<!-- Ringkas file/perilaku yang berubah. -->

## Verifikasi

- [ ] `python scripts/validate_schemas.py`
- [ ] `python scripts/validate_repo.py`
- [ ] `python scripts/validate_scope_identities.py`
- [ ] `python scripts/validate_display_names.py`
- [ ] `python scripts/validate_site.py`
- [ ] `python scripts/check_source_freshness.py`
- [ ] `python scripts/run_behavior_evals.py --dry-run --pack <pack-id>` untuk pack yang terdampak
- [ ] Source resmi dicantumkan bila mengubah fakta akademik
- [ ] Tidak ada API key, data pribadi, materi kuliah privat, atau materi berhak cipta yang ikut dikomit

## Risiko / belum diuji

<!-- Jelaskan failure mode atau pengujian yang belum dilakukan. CI tetap menjadi gate final. -->
