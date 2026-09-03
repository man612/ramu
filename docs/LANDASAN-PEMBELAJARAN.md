# Landasan Pembelajaran Ramu

Ramu dibuat untuk membantu mahasiswa menyelesaikan kebutuhan kuliah tanpa mengorbankan proses belajarnya. Karena itu, desainnya tidak berhenti pada “jawaban benar”, tetapi juga mengatur kapan bantuan perlu diberikan, kapan pengguna perlu mencoba sendiri, dan bagaimana progres dibawa ke sesi berikutnya.

## 1. Scaffolding lebih berguna daripada sekadar jawaban cepat

Kestin dkk. (2025) melaporkan randomized controlled trial pada mahasiswa yang membandingkan AI tutor berbasis prinsip pedagogis dengan active learning di kelas. Tutor tersebut menekankan scaffolding, feedback, pengelolaan cognitive load, dan self-pacing—bukan sekadar akses ke model bahasa.

Implikasinya:

- mode belajar memakai tangga bantuan;
- worked example diikuti pengurangan bantuan;
- sesi ditutup dengan cek pemahaman, bukan hanya final answer.

Sumber: Kestin, G., Miller, K., Klales, A., et al. (2025). *AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting*. Scientific Reports, 15, 17458. https://doi.org/10.1038/s41598-025-97652-6

## 2. Bantuan berlebihan bisa mengganggu belajar mandiri

Bastani dkk. (2025) menemukan bahwa akses generative AI dapat meningkatkan performa saat alat tersedia, tetapi kelompok yang mendapat bantuan tanpa guardrail dapat tampil lebih buruk ketika AI kemudian dilepas. Tutor dengan safeguards berbasis hint mengurangi dampak tersebut.

Karena itu:

- intent `belajar` dan `latihan ujian` tidak langsung membuka seluruh jawaban;
- mahasiswa diberi ruang untuk mencoba;
- bantuan dinaikkan bila memang diperlukan;
- latihan membedakan jawaban mandiri dari jawaban setelah hint.

Sumber: Bastani, H., Bastani, O., Sungu, A., et al. (2025). *Generative AI without guardrails can harm learning: Evidence from high school mathematics*. Proceedings of the National Academy of Sciences, 122(26), e2422633122. https://doi.org/10.1073/pnas.2422633122

## 3. Progress perlu terlihat, bukan hanya tersimpan samar di memory

Systematic mapping review Banihashem dkk. (2025) memetakan 84 studi di persilangan AI dan self-regulated learning. Banyak implementasi memakai AI untuk personalisasi, tutoring, assessment, prediction, dan dukungan proses regulasi belajar.

Di Ramu, temuan ini diterjemahkan menjadi learner state yang dapat dilihat dan diperbaiki:

- kemajuan penting tidak hanya dibiarkan sebagai memory implisit;
- mastery map, misconception log, dan review queue dapat menyimpan progres yang relevan;
- catatan bisa dikoreksi atau dihapus;
- status penguasaan didasarkan pada bukti dari latihan/pekerjaan, bukan karena materi pernah dijelaskan AI.

Sumber: Banihashem, S. K., Bond, M., Bergdahl, N., Khosravi, H., & Noroozi, O. (2025). *A systematic mapping review at the intersection of artificial intelligence and self-regulated learning*. International Journal of Educational Technology in Higher Education, 22, 50. https://doi.org/10.1186/s41239-025-00548-8

## 4. Grounding membantu, tetapi sumber tetap perlu diawasi

Li dkk. (2025) meninjau 51 studi RAG untuk aplikasi pendidikan. Review tersebut menunjukkan manfaat retrieval untuk factual accuracy dan knowledge freshness, sekaligus menyoroti masalah yang masih tersisa seperti hallucination, kelengkapan retrieval, timeliness, dan multimodality.

Ramu tidak menjalankan vector RAG sendiri. ChatGPT Project dan file mata kuliah menjadi lapisan grounding pengguna, sementara source registry mencatat fungsi sumber, otoritas, dan tanggal review agar perubahan bisa ditelusuri.

Sumber: Li, Z., Wang, Z., Wang, W., Hung, K., Xie, H., & Wang, F. L. (2025). *Retrieval-augmented generation for educational application: A systematic survey*. Computers and Education: Artificial Intelligence, 8, 100417. https://doi.org/10.1016/j.caeai.2025.100417

## Prinsip yang dipakai

Dari landasan di atas, desain pembelajaran mengikuti beberapa prinsip:

1. bantuan adaptif, bukan answer dump sebagai default;
2. active recall sebelum melihat jawaban pada mode latihan;
3. bantuan dikurangi setelah mahasiswa mulai mampu;
4. learner state eksplisit dan dapat dikoreksi;
5. source hierarchy dan freshness dapat diperiksa ulang;
6. behavior eval dipakai agar guardrail penting tidak hilang saat prompt atau pack berkembang.

Prinsip tersebut bukan resep universal. Cara bantuan tetap perlu menyesuaikan tujuan pengguna, aturan kampus, karakter mata kuliah, dan bukti dari pemakaian nyata.
