const PACK_INDEX_URL = "./packs/index.json";

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function fetchJson(url) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error(`Tidak dapat memuat ${url}`);
  return response.json();
}

function periodLabel(item) {
  return item.period_label || item.period_id || "Periode";
}

function entryLabel(entry) {
  return `${entry.institution} · ${entry.program} · ${entry.academic_year} · ${periodLabel(entry)}`;
}

function currentPackEntry(catalog) {
  const requested = new URLSearchParams(window.location.search).get("pack");
  return catalog.packs.find(item => item.id === requested)
    || catalog.packs.find(item => item.id === catalog.default_pack_id)
    || catalog.packs[0];
}

function manifestUrl(entry) {
  return `./packs/${entry.manifest}`;
}

function packBase(entry) {
  const parts = entry.manifest.split("/");
  parts.pop();
  return `./packs/${parts.join("/")}`;
}

function setupUrl(packId) {
  return `setup.html?pack=${encodeURIComponent(packId)}`;
}

function packPickerOptions(root) {
  return Array.from(root.querySelectorAll(".pack-picker-option"));
}

function closePackPicker(root, returnFocus = false) {
  const trigger = root.querySelector("[data-pack-picker-trigger]");
  const menu = root.querySelector("[data-pack-picker-menu]");
  if (!trigger || !menu) return;
  trigger.setAttribute("aria-expanded", "false");
  menu.hidden = true;
  if (returnFocus) trigger.focus();
}

function openPackPicker(root, focusMode = "selected") {
  const trigger = root.querySelector("[data-pack-picker-trigger]");
  const menu = root.querySelector("[data-pack-picker-menu]");
  if (!trigger || !menu || trigger.disabled) return;
  trigger.setAttribute("aria-expanded", "true");
  menu.hidden = false;
  const options = packPickerOptions(root);
  if (!options.length) return;
  const selected = options.find(option => option.getAttribute("aria-selected") === "true");
  const target = focusMode === "last" ? options.at(-1) : (selected || options[0]);
  requestAnimationFrame(() => target?.focus());
}

function navigateToPack(packId) {
  const url = new URL(window.location.href);
  url.searchParams.set("pack", packId);
  window.location.assign(url.toString());
}

function bindPackPickerKeyboard(root) {
  const trigger = root.querySelector("[data-pack-picker-trigger]");
  const menu = root.querySelector("[data-pack-picker-menu]");
  if (!trigger || !menu) return;

  trigger.addEventListener("keydown", event => {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      openPackPicker(root, "selected");
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      openPackPicker(root, "last");
    } else if (event.key === "Escape") {
      closePackPicker(root);
    }
  });

  menu.addEventListener("keydown", event => {
    const options = packPickerOptions(root);
    const index = options.indexOf(document.activeElement);
    if (!options.length) return;

    let nextIndex = index;
    if (event.key === "ArrowDown") nextIndex = Math.min(index + 1, options.length - 1);
    else if (event.key === "ArrowUp") nextIndex = Math.max(index - 1, 0);
    else if (event.key === "Home") nextIndex = 0;
    else if (event.key === "End") nextIndex = options.length - 1;
    else if (event.key === "Escape") {
      event.preventDefault();
      closePackPicker(root, true);
      return;
    } else return;

    event.preventDefault();
    options[nextIndex]?.focus();
  });
}

function renderPackPickers(catalog, active) {
  document.querySelectorAll("[data-pack-picker]").forEach((root, index) => {
    const trigger = root.querySelector("[data-pack-picker-trigger]");
    const value = root.querySelector("[data-pack-picker-value]");
    const menu = root.querySelector("[data-pack-picker-menu]");
    if (!trigger || !value || !menu) return;

    const menuId = `pack-picker-menu-${index + 1}`;
    menu.id = menuId;
    trigger.setAttribute("aria-controls", menuId);
    trigger.setAttribute("aria-expanded", "false");
    value.textContent = entryLabel(active);

    menu.innerHTML = catalog.packs.map(entry => {
      const selected = entry.id === active.id;
      return `<button class="pack-picker-option" type="button" role="option" aria-selected="${selected}" data-pack-id="${escapeHtml(entry.id)}">
        <span>${escapeHtml(entryLabel(entry))}</span>
        ${selected ? '<span class="pack-picker-option-state">Aktif</span>' : ""}
      </button>`;
    }).join("");

    if (catalog.packs.length <= 1) {
      root.querySelector(".pack-picker")?.classList.add("is-single");
      trigger.disabled = true;
      trigger.setAttribute("aria-label", `${entryLabel(active)}. Satu pack tersedia.`);
    } else {
      trigger.addEventListener("click", () => {
        const open = trigger.getAttribute("aria-expanded") === "true";
        if (open) closePackPicker(root);
        else openPackPicker(root);
      });

      menu.querySelectorAll(".pack-picker-option").forEach(option => {
        option.addEventListener("click", () => {
          const packId = option.dataset.packId;
          if (!packId || packId === active.id) {
            closePackPicker(root, true);
            return;
          }
          navigateToPack(packId);
        });
      });

      bindPackPickerKeyboard(root);
      document.addEventListener("click", event => {
        if (!root.contains(event.target)) closePackPicker(root);
      });
    }
  });
}

function setText(selector, value) {
  const el = document.querySelector(selector);
  if (el) el.textContent = value;
}

function statusLabel(status, maintainer) {
  const statusMap = {
    "source-verified": "Sumber terverifikasi",
    verified: "Terverifikasi",
    community: "Community pack",
    experimental: "Eksperimental",
    deprecated: "Kedaluwarsa"
  };
  const base = statusMap[status] || status;
  return maintainer === "ramu" ? `${base} · Ramu Maintained` : `${base} · Community`;
}

function bindSetupLinks(entry) {
  document.querySelectorAll("[data-setup-link]").forEach(link => {
    link.href = setupUrl(entry.id);
  });
}

function renderHomePack(entry, manifest) {
  const period = periodLabel(manifest);
  setText("#hero-course-count", manifest.courses.length);
  setText("#pack-kicker", entry.maintainer === "ramu" ? "Ramu Maintained pack" : "Community pack");
  setText("#pack-title", `${manifest.institution} · ${manifest.program} · ${period}`);
  setText("#pack-meta", `${manifest.academic_year} · ${manifest.total_sks} SKS · ${manifest.courses.length} mata kuliah · pack ${manifest.pack_version}`);
  setText("#pack-status", statusLabel(manifest.status, manifest.maintainer));
  setText("#closing-pack-label", `${manifest.institution} · ${manifest.program} · ${period}`);
  bindSetupLinks(entry);

  const target = document.querySelector("#course-list");
  if (!target) return;
  target.innerHTML = manifest.courses.map(course => `
    <article class="course-card">
      <div class="course-top"><span>${escapeHtml(course.code)}</span><span>${escapeHtml(course.sks)} SKS</span></div>
      <h3>${escapeHtml(course.short_name)}</h3>
      <p class="course-focus">Fokus: ${escapeHtml(course.focus || "materi dan tugas mata kuliah")}</p>
    </article>
  `).join("");
}

async function copyText(text, statusEl, message = "Tersalin.") {
  try {
    await navigator.clipboard.writeText(text);
    if (statusEl) statusEl.textContent = message;
    return true;
  } catch {
    if (statusEl) statusEl.textContent = "Tidak dapat menyalin otomatis. Buka teks, lalu salin secara manual.";
    return false;
  }
}

function storageKey(id) { return `ramu:${id}`; }
function getProgress(id) { try { return JSON.parse(localStorage.getItem(storageKey(id))) || {}; } catch { return {}; } }
function saveProgress(id, progress) { localStorage.setItem(storageKey(id), JSON.stringify(progress)); }

async function downloadCoursePack(base, course, button) {
  const original = button.textContent;
  try {
    const response = await fetch(`${base}/${course.file}`, { cache: "no-store" });
    if (!response.ok) throw new Error();
    const text = await response.text();
    const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `ramu-${course.code.toLowerCase()}-${course.short_name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "")}.txt`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    button.textContent = "File siap";
  } catch {
    button.textContent = "Gagal mengunduh";
  }
  setTimeout(() => button.textContent = original, 1800);
}

function renderSetupSummary(entry, manifest) {
  setText("#setup-pack-name", `${manifest.institution} · ${manifest.program} · ${periodLabel(manifest)}`);
  setText("#setup-pack-count", `${manifest.courses.length} course pack`);
  setText("#setup-pack-meta", `${manifest.academic_year} · ${manifest.total_sks} SKS · ${statusLabel(manifest.status, manifest.maintainer)}`);
  const list = document.querySelector("#setup-summary-list");
  if (list) list.innerHTML = manifest.courses.map(course => `<li>${escapeHtml(course.short_name)}</li>`).join("");
  document.title = `Setup ${manifest.name} — Ramu`;
}

async function renderSetup(entry, manifest) {
  const target = document.querySelector("#setup-courses");
  if (!target) return;
  const base = packBase(entry);
  const progress = getProgress(manifest.id);
  const instructionsUrl = `${base}/${manifest.project_instructions}`;
  const instructionButton = document.querySelector("#copy-instructions");
  const status = document.querySelector("#copy-status");
  const openInstructions = document.querySelector("#open-instructions");

  renderSetupSummary(entry, manifest);

  if (instructionButton) {
    instructionButton.addEventListener("click", async () => {
      try {
        const response = await fetch(instructionsUrl, { cache: "no-store" });
        if (!response.ok) throw new Error();
        const text = await response.text();
        const copied = await copyText(text, status, "Project Instructions sudah disalin. Tempelkan lewat Project settings → Project Instructions.");
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
      <details class="setup-course" data-course="${escapeHtml(course.code)}" data-complete="${complete}" ${index === 0 ? "open" : ""}>
        <summary>
          <span class="course-number">${index + 1}</span>
          <span class="setup-title"><strong>${escapeHtml(course.short_name)}</strong><span>${escapeHtml(course.code)} · ${escapeHtml(course.sks)} SKS · pack ${escapeHtml(manifest.pack_version)}</span></span>
          <span class="done-pill">${complete ? "Selesai" : "Belum"}</span>
        </summary>
        <div class="setup-body">
          <p class="course-focus"><strong>Fokus:</strong> ${escapeHtml(course.focus || "materi dan tugas mata kuliah")}</p>
          <ol>
            <li>Buka ChatGPT, lalu pilih <strong>New Project</strong>.</li>
            <li>Beri nama <strong>${escapeHtml(course.project_name)}</strong>, kemudian pilih <strong>Project-only memory</strong>.</li>
            <li>Buka <strong>⋯ → Project settings → Project Instructions</strong>, lalu tempel instruksi Ramu dari langkah 2.</li>
            <li>Tekan <strong>Unduh paket (.txt)</strong> di bawah.</li>
            <li>Di Project, buka area <strong>Sources</strong> atau <strong>Project Sources</strong>, pilih tombol untuk menambahkan source, lalu unggah file yang baru diunduh. Nama tombol dapat berbeda antar versi ChatGPT.</li>
          </ol>
          <div class="inline-actions">
            <button class="small-button copy-project" type="button" data-text="${escapeHtml(course.project_name)}">Salin nama Project</button>
            <button class="small-button download-course-pack" type="button" data-course="${escapeHtml(course.code)}">Unduh paket (.txt)</button>
            <a class="small-button" href="https://chatgpt.com/" target="_blank" rel="noopener">Buka ChatGPT</a>
          </div>
          <p class="small-note">Course pack menjadi source Project. Screenshot soal, rubrik, atau materi tambahan cukup dimasukkan saat dibutuhkan.</p>
          <label class="complete-check"><input type="checkbox" data-course-check="${escapeHtml(course.code)}" ${complete ? "checked" : ""}><span>Project ${escapeHtml(course.short_name)} sudah selesai disiapkan</span></label>
        </div>
      </details>
    `;
  }).join("");

  target.innerHTML = `${courseCards}
    <div class="info-box">
      <strong>Kenapa course pack berupa file?</strong>
      <p>Course pack dibuat sebagai file teks agar dapat diunggah langsung ke Project Sources tanpa bergantung pada satu label tombol ChatGPT tertentu.</p>
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

  target.querySelectorAll(".download-course-pack").forEach(button => {
    button.addEventListener("click", () => {
      const course = manifest.courses.find(item => item.code === button.dataset.course);
      if (course) downloadCoursePack(base, course, button);
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
    const catalog = await fetchJson(PACK_INDEX_URL);
    if (!Array.isArray(catalog.packs) || !catalog.packs.length) throw new Error("Katalog pack kosong");
    const entry = currentPackEntry(catalog);
    const manifest = await fetchJson(manifestUrl(entry));
    renderPackPickers(catalog, entry);
    renderHomePack(entry, manifest);
    await renderSetup(entry, manifest);
  } catch (error) {
    console.error(error);
    const home = document.querySelector("#course-list");
    const setup = document.querySelector("#setup-courses");
    if (home) home.innerHTML = `<p class="muted">Katalog Ramu belum dapat dimuat. Coba muat ulang halaman.</p>`;
    if (setup) setup.innerHTML = `<p class="muted">Paket Ramu belum dapat dimuat. Coba muat ulang halaman.</p>`;
  }
})();