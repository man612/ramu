# Landasan Pembelajaran Ramu

Ramu tidak dirancang sebagai mesin yang selalu memberi jawaban secepat mungkin. Tujuan utamanya adalah membantu mahasiswa menyelesaikan kebutuhan kuliah sambil tetap membangun kemampuan yang dapat digunakan tanpa AI.

## 1. AI tutor membutuhkan scaffolding, bukan hanya jawaban yang benar

Kestin dkk. (2025) melaporkan randomized controlled trial pada mahasiswa yang membandingkan AI tutor berbasis prinsip pedagogis dengan active learning di kelas. Desain tutor menekankan scaffolding dan praktik pedagogis, bukan sekadar akses ke model bahasa.

Implikasi untuk Ramu:

- mode belajar memakai tangga bantuan;
- worked example diikuti pengurangan bantuan;
- sesi ditutup dengan cek pemahaman, bukan hanya final answer.

Sumber: Kestin, G., Miller, K., Klales, A., et al. (2025). *AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting*. Scientific Reports, 15, 17458. https://doi.org/10.1038/s41598-025-97652-6

## 2. Bantuan tanpa guardrail dapat meningkatkan performa saat AI tersedia tetapi merusak belajar mandiri

Bastani dkk. (2025) menemukan bahwa akses generative AI dapat meningkatkan performa ketika alat tersedia, tetapi kelompok dengan akses tanpa guardrail dapat tampil lebih buruk ketika AI kemudian dicabut. Tutor dengan safeguards berbasis hint mengurangi dampak negatif tersebut.

Implikasi untuk Ramu:

- intent `belajar` dan `latihan ujian` tidak langsung membocorkan semua jawaban;
- mahasiswa diberi giliran mencoba;
- bantuan dinaikkan hanya jika diperlukan;
- latihan ujian membedakan jawaban mandiri dan jawaban setelah hint.

Sumber: Bastani, H., Bastani, O., Sungu, A., et al. (2025). *Generative AI without guardrails can harm learning: Evidence from high school mathematics*. Proceedings of the National Academy of Sciences, 122(26), e2422633122. https://doi.org/10.1073/pnas.2422633122

## 3. Self-regulated learning perlu state yang terlihat dan dapat diperbarui

Systematic mapping review Banihashem dkk. (2025) memetakan 84 studi pada persilangan AI dan self-regulated learning. Banyak implementasi AI berperan dalam personalisasi, tutoring, assessment, prediction, dan dukungan proses regulasi belajar.

Implikasi untuk Ramu:

- kemajuan penting tidak hanya dibiarkan sebagai memory implisit;
- tersedia learner state, mastery map, misconception log, dan review queue;
- catatan harus dapat diperbaiki atau dihapus oleh mahasiswa;
- status penguasaan harus berdasarkan bukti dari latihan/pekerjaan, bukan karena materi pernah dijelaskan AI.

Sumber: Banihashem, S. K., Bond, M., Bergdahl, N., Khosravi, H., & Noroozi, O. (2025). *A systematic mapping review at the intersection of artificial intelligence and self-regulated learning*. International Journal of Educational Technology in Higher Education, 22, 50. https://doi.org/10.1186/s41239-025-00548-8

## 4. Grounding sumber membantu, tetapi freshness dan hallucination tetap perlu diawasi

Li dkk. (2025) meninjau 51 studi RAG untuk aplikasi pendidikan. Review tersebut menyoroti manfaat retrieval untuk factual accuracy dan knowledge freshness sekaligus masalah yang masih tersisa: hallucination, kelengkapan retrieval, timeliness, dan multimodality.

Ramu saat ini tidak menjalankan vector RAG sendiri; ChatGPT Project dan file mata kuliah menjadi lapisan grounding pengguna. Karena itu Ramu menambahkan source registry dan freshness policy agar sumber yang digunakan memiliki fungsi, otoritas, dan tanggal verifikasi yang eksplisit.

Sumber: Li, Z., Wang, Z., Wang, W., Hung, K., Xie, H., & Wang, F. L. (2025). *Retrieval-augmented generation for educational application: A systematic survey*. Computers and Education: Artificial Intelligence, 8, 100417. https://doi.org/10.1016/j.caeai.2025.100417

## Prinsip desain yang diturunkan

Dari temuan di atas, Ramu memakai prinsip berikut:

1. bantuan adaptif, bukan answer dump sebagai default;
2. active recall sebelum melihat jawaban pada mode latihan;
3. pengurangan bantuan setelah mahasiswa mulai mampu;
4. learner state eksplisit dan dapat dikoreksi;
5. source hierarchy dan freshness yang dapat diaudit;
6. eval/regression contract agar guardrail tidak hilang saat prompt berkembang.

Riset ini tidak berarti satu desain akan cocok untuk semua mahasiswa atau semua mata kuliah. Protokol Ramu tetap harus proporsional terhadap tujuan pengguna, aturan kampus, karakter materi, dan bukti dari pemakaian nyata.
