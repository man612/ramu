(() => {
  ["motion.css", "mobile.css"].forEach(href => {
    if (document.querySelector(`link[href="${href}"]`)) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  });

  ["motion.js", "mobile.js"].forEach(src => {
    if (document.querySelector(`script[src="${src}"]`)) return;
    const script = document.createElement("script");
    script.src = src;
    script.defer = true;
    document.head.appendChild(script);
  });
})();

const PACK_BASE = "./packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02";

const COURSE_FOCUS = {
  EACC4104: "aturan pajak, konsep, dan kasus",
  EACC4103: "jurnal, hitungan, kasus, dan PRATON",
  EMBS4210: "rumus, hitungan, dan analisis keuangan",
  ECON4102: "konsep, grafik, dan analisis ekonomi",
  EMBS4101: "konsep manajemen dan analisis kasus"
};

async function getManifest() {
  const response = await fetch(`${PACK_BASE}/manifest.json`, { cache: "no-store" });
  if (!response.ok) throw new Error("Manifest tidak dapat dimuat");
  return response.json();
}

function renderHomeCourses(manifest) {
  const target = document.querySelector("#course-list");
  if (!target) return;
  target.innerHTML = manifest.courses.map(course => `
    <article class="course-card">
      <div class="course-top"><span>${course.code}</span><span>${course.sks} SKS</span></div>
      <h3>${course.short_name}</h3>
      <p class="course-focus">Fokus: ${COURSE_FOCUS[course.code] || "materi dan tugas mata kuliah"}</p>
    </article>
  `).join("");
}

async function copyText(text, statusEl, message = "Tersalin.") {
  try {
    await navigator.clipboard.writeText(text);
    if (statusEl) statusEl.textContent = message;
    return true;
  } catch {
    if (statusEl) statusEl.textContent = "Tidak dapat menyalin otomatis. Buka file, lalu salin teks secara manual.";
    return false;
  }
}

function storageKey(id) { return `ramu:${id}`; }
function getProgress(id) { try { return JSON.parse(localStorage.getItem(storageKey(id))) || {}; } catch { return {}; } }
function saveProgress(id, progress) { localStorage.setItem(storageKey(id), JSON.stringify(progress)); }

async function renderSetup(manifest) {
  const target = document.querySelector("#setup-courses");
  if (!target) return;
  const progress = getProgress(manifest.id);
  const instructionsUrl = `${PACK_BASE}/${manifest.project_instructions}`;
  const instructionButton = document.querySelector("#copy-instructions");
  const status = document.querySelector("#copy-status");
  const openInstructions = document.querySelector("#open-instructions");

  if (instructionButton) {
    instructionButton.addEventListener("click", async () => {
      try {
        const response = await fetch(instructionsUrl, { cache: "no-store" });
        if (!response.ok) throw new Error();
        const text = await response.text();
        const copied = await copyText(text, status, "Project Instructions sudah disalin. Tempelkan teks ini ke setiap Project.");
        if (copied) {
          instructionButton.textContent = "Sudah disalin";
          setTimeout(() => instructionButton.textContent = "Salin instruksi", 1500);
        }
      } catch {
        status.textContent = "Project Instructions tidak dapat dimuat. Buka teks, lalu salin secara manual.";
      }
    });
  }
  if (openInstructions) openInstructions.href = instructionsUrl;

  const courseCards = manifest.courses.map((course, index) => {
    const complete = Boolean(progress[course.code]);
    return `
      <details class="setup-course" data-course="${course.code}" data-complete="${complete}" ${index === 0 ? "open" : ""}>
        <summary>
          <span class="course-number">${index + 1}</span>
          <span class="setup-title"><strong>${course.short_name}</strong><span>${course.code} · ${course.sks} SKS · pack ${manifest.pack_version || "Semester 2"}</span></span>
          <span class="done-pill">${complete ? "Selesai" : "Belum"}</span>
        </summary>
        <div class="setup-body">
          <ol>
            <li>Buka aplikasi ChatGPT, lalu pilih <strong>New Project</strong>.</li>
            <li>Beri nama <strong>${course.project_name}</strong>, kemudian pilih <strong>Project-only memory</strong>.</li>
            <li>Buka pengaturan Project, lalu tempel <strong>Project Instructions</strong> yang sudah disalin pada langkah 2.</li>
            <li>Tambahkan course pack sebagai <strong>Project Source</strong>. Di HP, cara paling praktis: tekan <strong>Salin paket</strong>, lalu di Project pilih <strong>Add source</strong> (atau menu setara) dan tempel teksnya. Kalau lebih nyaman, file tetap bisa diunduh lalu diunggah.</li>
          </ol>
          <div class="inline-actions">
            <button class="small-button copy-project" type="button" data-text="${course.project_name}">Salin nama Project</button>
            <button class="small-button copy-course-pack" type="button" data-file="${course.file}">Salin paket</button>
            <a class="small-button" href="${PACK_BASE}/${course.file}" download>Unduh file</a>
            <a class="small-button" href="https://chatgpt.com/" target="_blank" rel="noopener">Buka ChatGPT</a>
          </div>
          <p class="small-note">Course pack ini adalah source tetap. Screenshot soal, rubrik, atau materi sementara cukup ditambahkan saat dibutuhkan dan tidak harus disimpan permanen.</p>
          <label class="complete-check"><input type="checkbox" data-course-check="${course.code}" ${complete ? "checked" : ""}><span>Project ${course.short_name} sudah selesai disiapkan</span></label>
        </div>
      </details>
    `;
  }).join("");

  target.innerHTML = `${courseCards}
    <div class="info-box">
      <strong>Kalau batas file Project terasa sempit</strong>
      <p>Jaga course pack sebagai source tetap. Untuk tugas harian, kirim screenshot/PDF di chat atau tambahkan hanya materi yang benar-benar relevan. Batas file memang berbeda menurut paket ChatGPT dan dapat berubah.</p>
    </div>`;

  target.querySelectorAll(".copy-project").forEach(button => {
    button.addEventListener("click", async () => {
      const copied = await copyText(button.dataset.text, null);
      if (!copied) return;
      const original = button.textContent;
      button.textContent = "Tersalin";
      setTimeout(() => button.textContent = original, 1200);
    });
  });

  target.querySelectorAll(".copy-course-pack").forEach(button => {
    button.addEventListener("click", async () => {
      const original = button.textContent;
      try {
        const response = await fetch(`${PACK_BASE}/${button.dataset.file}`, { cache: "no-store" });
        if (!response.ok) throw new Error();
        const text = await response.text();
        const copied = await copyText(text, null);
        if (!copied) return;
        button.textContent = "Paket tersalin";
      } catch {
        button.textContent = "Buka file manual";
      }
      setTimeout(() => button.textContent = original, 1600);
    });
  });

  target.querySelectorAll("[data-course-check]").forEach(input => {
    input.addEventListener("change", () => {
      progress[input.dataset.courseCheck] = input.checked;
      saveProgress(manifest.id, progress);
      const card = input.closest(".setup-course");
      card.dataset.complete = String(input.checked);
      card.querySelector(".done-pill").textContent = input.checked ? "Selesai" : "Belum";
      updateProgress(manifest, progress);
    });
  });

  document.querySelectorAll("[data-progress]").forEach(input => {
    const key = `preflight:${input.dataset.progress}`;
    input.checked = Boolean(progress[key]);
    input.addEventListener("change", () => { progress[key] = input.checked; saveProgress(manifest.id, progress); });
  });

  document.querySelectorAll("[data-copy-phrase]").forEach(button => {
    button.addEventListener("click", async () => {
      const original = button.textContent;
      const copied = await copyText(button.dataset.copyPhrase, null);
      if (!copied) return;
      button.textContent = "Tersalin";
      setTimeout(() => button.textContent = original, 1000);
    });
  });
  updateProgress(manifest, progress);
}

function updateProgress(manifest, progress) {
  const done = manifest.courses.filter(course => progress[course.code]).length;
  const title = document.querySelector("#progress-title");
  const bar = document.querySelector("#progress-bar");
  if (title) title.textContent = `${done} dari ${manifest.courses.length} Project selesai`;
  if (bar) bar.style.width = `${(done / manifest.courses.length) * 100}%`;
}

(async function init() {
  try {
    const manifest = await getManifest();
    renderHomeCourses(manifest);
    await renderSetup(manifest);
  } catch {
    const home = document.querySelector("#course-list");
    const setup = document.querySelector("#setup-courses");
    if (home) home.innerHTML = `<p class="muted">Daftar mata kuliah belum dapat dimuat. Coba muat ulang halaman.</p>`;
    if (setup) setup.innerHTML = `<p class="muted">Paket mata kuliah belum dapat dimuat. Coba muat ulang halaman.</p>`;
  }
})();
