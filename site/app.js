const PACK_BASE = "./packs/universitas-terbuka/s1-akuntansi/2026-2027/semester-02";

async function getManifest() {
  const response = await fetch(`${PACK_BASE}/manifest.json`, { cache: "no-store" });
  if (!response.ok) throw new Error("Manifest tidak dapat dimuat");
  return response.json();
}

function renderHomeCourses(manifest) {
  const target = document.querySelector("#course-list");
  if (!target) return;
  target.innerHTML = manifest.courses.map(course => `
    <div class="course-row">
      <span class="course-code">${course.code}</span>
      <span class="course-name">${course.name}</span>
      <span class="course-sks">${course.sks} SKS</span>
    </div>
  `).join("");
}

async function copyText(text, statusEl, message = "Tersalin.") {
  try {
    await navigator.clipboard.writeText(text);
    if (statusEl) statusEl.textContent = message;
  } catch {
    if (statusEl) statusEl.textContent = "Tidak bisa menyalin otomatis. Buka file lalu salin manual.";
  }
}

function storageKey(id) {
  return `ramu:${id}`;
}

function getProgress(id) {
  try {
    return JSON.parse(localStorage.getItem(storageKey(id))) || {};
  } catch {
    return {};
  }
}

function saveProgress(id, progress) {
  localStorage.setItem(storageKey(id), JSON.stringify(progress));
}

async function renderSetup(manifest) {
  const target = document.querySelector("#setup-courses");
  if (!target) return;

  const progress = getProgress(manifest.id);
  const instructionsUrl = `${PACK_BASE}/${manifest.project_instructions}`;

  const instructionButton = document.querySelector("#copy-instructions");
  const status = document.querySelector("#copy-status");
  if (instructionButton) {
    instructionButton.addEventListener("click", async () => {
      try {
        const response = await fetch(instructionsUrl);
        const text = await response.text();
        await copyText(text, status, "Project Instructions sudah disalin.");
      } catch {
        status.textContent = "Instructions tidak dapat dimuat. Buka file lalu salin manual.";
      }
    });
  }

  const openInstructions = document.querySelector("#open-instructions");
  if (openInstructions) openInstructions.href = instructionsUrl;

  target.innerHTML = manifest.courses.map((course, index) => {
    const complete = Boolean(progress[course.code]);
    return `
      <details class="setup-course" data-course="${course.code}" data-complete="${complete}">
        <summary>
          <span class="course-number">${String(index + 1).padStart(2, "0")}</span>
          <span class="setup-title">
            <strong>${course.short_name}</strong>
            <span>${course.code} · ${course.sks} SKS</span>
          </span>
          <span class="done-pill">${complete ? "Selesai" : "Belum"}</span>
        </summary>
        <div class="setup-body">
          <ol>
            <li>Buka ChatGPT dan buat Project baru dengan nama <strong>${course.project_name}</strong>.</li>
            <li>Saat Project dibuat, pilih <strong>Project-only memory</strong>.</li>
            <li>Masuk Project settings dan tempel Project Instructions.</li>
            <li>Upload course pack <strong>${course.file.split("/").pop()}</strong>.</li>
          </ol>
          <div class="inline-actions">
            <button class="small-button copy-project" type="button" data-text="${course.project_name}">Salin nama Project</button>
            <a class="small-button" href="${PACK_BASE}/${course.file}" download>Unduh course pack</a>
            <a class="small-button" href="https://chatgpt.com/" target="_blank" rel="noopener">Buka ChatGPT</a>
          </div>
          <label class="complete-check">
            <input type="checkbox" data-course-check="${course.code}" ${complete ? "checked" : ""}>
            Project ini sudah selesai disiapkan
          </label>
        </div>
      </details>
    `;
  }).join("");

  target.querySelectorAll(".copy-project").forEach(button => {
    button.addEventListener("click", () => {
      copyText(button.dataset.text, null);
      const old = button.textContent;
      button.textContent = "Tersalin";
      setTimeout(() => button.textContent = old, 1200);
    });
  });

  target.querySelectorAll("[data-course-check]").forEach(input => {
    input.addEventListener("change", () => {
      progress[input.dataset.courseCheck] = input.checked;
      saveProgress(manifest.id, progress);
      const card = input.closest(".setup-course");
      card.dataset.complete = String(input.checked);
      const pill = card.querySelector(".done-pill");
      if (pill) pill.textContent = input.checked ? "Selesai" : "Belum";
      updateProgress(manifest, progress);
    });
  });

  document.querySelectorAll("[data-progress]").forEach(input => {
    input.checked = Boolean(progress[`preflight:${input.dataset.progress}`]);
    input.addEventListener("change", () => {
      progress[`preflight:${input.dataset.progress}`] = input.checked;
      saveProgress(manifest.id, progress);
    });
  });

  updateProgress(manifest, progress);
}

function updateProgress(manifest, progress) {
  const done = manifest.courses.filter(course => progress[course.code]).length;
  const title = document.querySelector("#progress-title");
  const bar = document.querySelector("#progress-bar");
  if (title) title.textContent = `${done} dari ${manifest.courses.length} selesai`;
  if (bar) bar.style.width = `${(done / manifest.courses.length) * 100}%`;
}

(async function init() {
  try {
    const manifest = await getManifest();
    renderHomeCourses(manifest);
    await renderSetup(manifest);
  } catch (error) {
    const home = document.querySelector("#course-list");
    const setup = document.querySelector("#setup-courses");
    if (home) home.innerHTML = `<p class="muted">Daftar mata kuliah tidak dapat dimuat. Coba muat ulang halaman.</p>`;
    if (setup) setup.innerHTML = `<p class="muted">Course pack tidak dapat dimuat. Coba muat ulang halaman.</p>`;
  }
})();
