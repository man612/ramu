# Riset dan Dasar Desain

Ramu tidak dibangun dari asumsi bahwa prompt yang panjang otomatis menghasilkan pendamping belajar yang baik. Struktur proyek diturunkan dari dokumentasi produk, riset pembelajaran, RAG pendidikan, self-regulated learning, serta masalah nyata yang muncul pada penggunaan Project jangka panjang.

## 1. AI sebaiknya membimbing, bukan selalu mengambil alih

Randomized controlled trial Kestin dkk. (2025) pada mahasiswa menemukan AI tutor yang sengaja dirancang dengan praktik pedagogis dapat menghasilkan learning gain tinggi dan waktu belajar lebih singkat dibanding kondisi active-learning yang diuji. Desain yang mereka tekankan mencakup active learning, pengelolaan cognitive load, scaffolding, feedback yang tepat waktu, akurasi, dan self-pacing.

Hal penting lain dari penelitian tersebut: **system prompt saja tidak selalu cukup** untuk menjaga urutan scaffolding pada soal multipart. Karena itu Ramu memisahkan instruksi, course context, workflow, dan verifier.

Bastani dkk. (PNAS, 2025) juga menunjukkan akses GenAI tanpa guardrail dapat meningkatkan performa saat bantuan tersedia tetapi menimbulkan dampak buruk ketika bantuan dilepas; desain tutor dengan safeguards mengurangi masalah tersebut. Implikasinya untuk Ramu: mode belajar, review, dan latihan tidak boleh otomatis berubah menjadi generator jawaban final.

Sumber:
- https://doi.org/10.1038/s41598-025-97652-6
- https://doi.org/10.1073/pnas.2422633122

## 2. Self-regulated learning harus tetap dimiliki mahasiswa

Systematic mapping review Banihashem dkk. (2025) terhadap 84 studi menemukan penggunaan AI untuk SRL banyak berfokus pada adaptive/personalized systems, intelligent tutoring, assessment/evaluation, prediction, dan profiling. Ramu menerjemahkannya menjadi alur:

**pahami → rencanakan → kerjakan → periksa → refleksikan → perbaiki**

Feedback tutor tidak berhenti sebagai satu chat; hasilnya dapat diringkas menjadi lesson learned yang dipakai pada tugas berikutnya.

Sumber:
- https://doi.org/10.1186/s41239-025-00548-8

## 3. Materi eksternal lebih aman daripada mengandalkan ingatan model

Systematic survey RAG untuk pendidikan (2025) merangkum 51 studi dan menunjukkan manfaat retrieval untuk meningkatkan grounding, freshness, dan kredibilitas jawaban pendidikan. Namun RAG tetap memiliki tantangan: hallucination, kelengkapan sumber, timeliness, dan multimodality.

Ramu tidak menjalankan vector database sendiri. Prinsip yang diambil adalah **grounding**: course pack memberi aturan sumber, sementara BMP/rubrik/materi mahasiswa dimasukkan sebagai sumber Project saat diperlukan.

Sumber:
- https://doi.org/10.1016/j.caeai.2025.100417

## 4. Project harus kecil dan fokus

Dokumentasi OpenAI menyatakan Project dapat memakai percakapan lain dalam Project sebagai konteks. Dengan project-only memory, Project tidak mengambil percakapan dari luar.

Di sisi komunitas, pengguna Project jangka panjang berulang kali meminta retrieval yang lebih eksplisit, memory yang lebih transparan, dan kontrol lebih baik atas pengetahuan Project. Dalam salah satu respons komunitas resmi, OpenAI Support juga menyarankan mempertahankan running project summary untuk pekerjaan panjang. Sinyal ini bukan spesifikasi produk, tetapi cukup relevan sebagai failure mode yang perlu diantisipasi.

Karena itu default Ramu:

- satu mata kuliah satu Project;
- satu pekerjaan besar satu chat;
- source eksplisit untuk keputusan/feedback penting;
- hindari satu Project besar untuk seluruh semester.

Sumber resmi:
- https://help.openai.com/en/articles/10169521-projects-in-chatgpt

Sinyal komunitas:
- https://community.openai.com/t/projects-are-containers-not-archives-large-projects-need-retrieval-not-just-memory/1383739
- https://community.openai.com/t/feature-request-make-project-memory-transparent-searchable-and-user-controlled/1385159
- https://community.openai.com/t/feature-request-bring-project-scoped-retrieval-to-chatgpt/1385141
- https://community.openai.com/t/persistent-project-workspaces/1385395

## 5. Academic integrity harus mengikuti konteks kampus/tugas

Panduan Kemdiktisaintek 2025, UNESCO, dan sumber regulator pendidikan tinggi internasional sama-sama menekankan penggunaan GenAI yang human-centred, menjaga agency mahasiswa, privasi, transparansi, dan integritas assessment.

Ramu tidak memaksakan satu kebijakan AI untuk semua kampus. Course pack harus membedakan aturan institusi, tutor, dan tugas. Jika sebuah assessment melarang penggunaan AI untuk menghasilkan jawaban, sistem tetap boleh membantu memahami konsep atau mereview pekerjaan sesuai aturan yang berlaku, tetapi tidak mengabaikan larangan tersebut.

Sumber:
- https://kemdiktisaintek.go.id/library/book/122191
- https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research
- https://www.teqsa.gov.au/guides-resources/higher-education-good-practice-hub/gen-ai-knowledge-hub/gen-ai-academic-integrity-and-assessment-reform

## 6. Ramu perlu diuji, bukan hanya terlihat bagus

LLM bersifat nondeterministic. Pack yang terasa bagus pada satu percobaan belum tentu konsisten pada skenario lain.

Folder `evals/` menyimpan skenario manual yang sengaja menguji failure mode penting, misalnya:

- screenshot soal terpotong;
- konflik modul lama vs regulasi baru;
- sitasi yang tidak bisa diverifikasi;
- kesalahan hitung;
- rubrik yang lebih spesifik daripada default pack;
- feedback tutor yang harus dibawa ke pekerjaan berikutnya.

Pack baru sebaiknya tidak diberi status `Terverifikasi` hanya karena dokumentasinya lengkap; minimal harus lolos skenario inti yang relevan dengan bidangnya.
