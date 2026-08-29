# Ramu v0.2.1-beta — Website & UX Polish

`v0.2.1-beta` adalah patch release setelah `v0.2.0-beta` yang berfokus pada penyempurnaan website publik dan pengalaman setup Ramu.

Tidak ada perubahan pada data akademik, course pack, behavior contract, critical eval, maupun arsitektur multi-pack pada release ini. Fondasi dari `v0.2.0-beta` tetap sama.

## Yang berubah

### Copy website lebih langsung

Teks homepage dan halaman setup dirapikan agar lebih cepat menjelaskan fungsi Ramu sebagai konfigurasi belajar untuk ChatGPT Projects. Wording yang terlalu editorial atau marketing-oriented dihapus atau dibuat lebih langsung.

### Custom pack picker

Native browser `<select>` diganti custom pack picker yang konsisten dengan design system Ramu dan memiliki keyboard navigation, focus state, `aria-expanded`, `aria-selected`, serta listbox semantics.

Jika hanya ada satu pack, picker tampil sebagai field statis. Untuk katalog multi-pack pada mobile, menu menggunakan panel yang lebih sesuai untuk touch interaction.

CI juga memiliki regression guard agar native pack `<select>` tidak kembali tanpa sengaja.

### Setup wording lebih defensif

Petunjuk upload source tidak lagi bergantung pada satu label UI ChatGPT seperti `Add from library`. Panduan menjelaskan intent setup sambil mengakui label dan lokasi kontrol dapat berubah antar versi/rollout produk.

### Desktop visual scale lebih compact

Overall scale desktop dipadatkan sekitar 10–15% melalui ukuran layout aktual, bukan browser zoom atau `transform: scale()`.

Yang dipadatkan mencakup container, header, hero, heading, tombol, mockup ChatGPT, section spacing, cards, pack picker, dan step cards. Mobile tetap mempertahankan ukuran teks serta touch target yang nyaman.

## Validation

Perubahan release ini melewati current Ramu validation suite dan downstream GitHub Pages deployment pada snapshot yang sama.

Release snapshot:

`036a970bfa49a1e8318444e61c6eefd646107bb0`

Validation tetap mencakup schema/repository integrity, scope identity, multi-pack proof, eval trust boundary, critical behavior gates, manual/pilot evidence contracts, site contract, source freshness, dan composable eval wiring.

## Yang tidak berubah

Release ini tidak mengubah:

- pack Universitas Terbuka · S1 Akuntansi · Semester 2 · 2026/2027;
- daftar mata kuliah atau SKS;
- source registry akademik;
- Project Instructions behavior contract;
- E01–E16 dan critical set E01/E05/E08/E13;
- manual evidence architecture;
- pilot evidence architecture;
- multi-pack architecture.

## Status

Ramu tetap **Public Beta**.

Release ini tidak mengklaim full manual E01–E16 pada ChatGPT Projects asli, pilot nyata 5–10 mahasiswa, automated OpenAI API behavior benchmark, atau bahwa semua output AI selalu benar.

OpenAI API tetap tidak diperlukan untuk menggunakan Ramu.

---

**Release:** `v0.2.1-beta`  
**Previous release:** `v0.2.0-beta`  
**Channel:** Public Beta  
**Focus:** Website & UX polish
