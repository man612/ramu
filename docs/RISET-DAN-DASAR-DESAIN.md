# Riset dan Dasar Desain

Struktur Ramu tidak dibangun dari asumsi bahwa prompt panjang otomatis menghasilkan pendamping belajar yang baik. Keputusan desainnya ditarik dari dokumentasi produk, riset pembelajaran, RAG pendidikan, self-regulated learning, dan masalah yang muncul saat Project dipakai dalam jangka panjang.

## 1. AI sebaiknya membimbing, bukan selalu mengambil alih

Randomized controlled trial Kestin dkk. (2025) pada mahasiswa menemukan AI tutor yang dirancang dengan praktik pedagogis dapat menghasilkan learning gain tinggi dan waktu belajar lebih singkat dibanding kondisi active-learning yang diuji. Desain tutor menekankan active learning, cognitive load, scaffolding, feedback, akurasi, dan self-pacing.

Salah satu catatan penting dari penelitian itu adalah bahwa **system prompt saja tidak selalu cukup** untuk menjaga urutan scaffolding pada soal multipart. Di Ramu, alasan ini ikut mendorong pemisahan Project Instructions, course context, workflow, dan verifier.

Bastani dkk. (PNAS, 2025) juga menunjukkan GenAI tanpa guardrail dapat menaikkan performa saat bantuan tersedia tetapi merugikan performa ketika bantuan dilepas. Tutor dengan safeguards mengurangi masalah tersebut.

Implikasinya: mode belajar, review, dan latihan tidak otomatis berubah menjadi generator jawaban final.

Sumber:
- https://doi.org/10.1038/s41598-025-97652-6
- https://doi.org/10.1073/pnas.2422633122

## 2. Self-regulated learning tetap perlu dimiliki mahasiswa

Systematic mapping review Banihashem dkk. (2025) terhadap 84 studi menemukan penggunaan AI untuk SRL banyak berfokus pada adaptive/personalized systems, intelligent tutoring, assessment/evaluation, prediction, dan profiling.

Workflow Ramu menerjemahkan ide tersebut menjadi alur:

**pahami → rencanakan → kerjakan → periksa → refleksikan → perbaiki**

Feedback tutor juga tidak perlu berhenti sebagai satu chat. Bagian pentingnya bisa diringkas menjadi lesson learned atau learner state yang dipakai pada pekerjaan berikutnya.

Sumber:
- https://doi.org/10.1186/s41239-025-00548-8

## 3. Materi eksternal lebih aman daripada mengandalkan ingatan model

Systematic survey RAG untuk pendidikan (2025) merangkum 51 studi dan menunjukkan manfaat retrieval untuk grounding, freshness, dan kredibilitas jawaban pendidikan. Masalah seperti hallucination, kelengkapan sumber, timeliness, dan multimodality tetap ada.

Repository ini tidak menjalankan vector database. Prinsip yang diambil adalah **grounding**: course pack memberi aturan dan konteks, sementara BMP, rubrik, materi, screenshot, atau file pengguna ditambahkan ke Project saat diperlukan.

Sumber:
- https://doi.org/10.1016/j.caeai.2025.100417

## 4. Project kecil lebih mudah dijaga

Dokumentasi OpenAI menyatakan Project dapat memakai percakapan lain di Project yang sama sebagai konteks. Dengan project-only memory, konteks dari luar Project dipisahkan.

Di komunitas, penggunaan Project jangka panjang juga memunculkan permintaan berulang soal retrieval yang lebih eksplisit, memory yang lebih transparan, dan kontrol yang lebih baik atas knowledge Project. Sinyal komunitas bukan spesifikasi produk, tetapi berguna untuk mengenali failure mode.

Default yang dipakai:

- satu mata kuliah satu Project;
- satu pekerjaan besar satu chat;
- source eksplisit untuk keputusan atau feedback penting;
- hindari satu Project besar untuk seluruh semester.

Sumber resmi:
- https://help.openai.com/en/articles/10169521-projects-in-chatgpt

Sinyal komunitas:
- https://community.openai.com/t/projects-are-containers-not-archives-large-projects-need-retrieval-not-just-memory/1383739
- https://community.openai.com/t/feature-request-make-project-memory-transparent-searchable-and-user-controlled/1385159
- https://community.openai.com/t/feature-request-bring-project-scoped-retrieval-to-chatgpt/1385141
- https://community.openai.com/t/persistent-project-workspaces/1385395

## 5. Academic integrity mengikuti konteks kampus dan tugas

Panduan Kemdiktisaintek 2025, UNESCO, dan sumber regulator pendidikan tinggi internasional sama-sama menekankan penggunaan GenAI yang human-centred, menjaga agency mahasiswa, privasi, transparansi, dan integritas assessment.

Tidak ada satu kebijakan AI yang cocok untuk semua kampus atau tugas. Course pack perlu mengikuti aturan institusi, tutor, dan rubrik yang berlaku. Jika sebuah assessment membatasi penggunaan AI untuk menghasilkan jawaban, bantuan dialihkan ke pemahaman konsep, review, atau bentuk lain yang masih sesuai aturan tersebut.

Sumber:
- https://kemdiktisaintek.go.id/library/book/122191
- https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research
- https://www.teqsa.gov.au/guides-resources/higher-education-good-practice-hub/gen-ai-knowledge-hub/gen-ai-academic-integrity-and-assessment-reform

## 6. Desain perlu diuji ulang

LLM bersifat nondeterministic. Pack yang terasa baik pada satu percobaan belum tentu konsisten pada skenario lain.

Folder `evals/` menyimpan case yang sengaja menekan failure mode penting, misalnya:

- screenshot soal terpotong;
- konflik modul lama dengan regulasi baru;
- sitasi yang tidak bisa diverifikasi;
- kesalahan hitung;
- rubrik yang lebih spesifik daripada default pack;
- feedback tutor yang perlu dibawa ke pekerjaan berikutnya.

Status pack karena itu tidak hanya bergantung pada seberapa lengkap dokumentasinya. Source, static validation, manual behavior check, dan evidence penggunaan nyata tetap dinilai secara terpisah.
