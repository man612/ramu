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

function courseDisplayCode(course) {
  return course.display_code || course.code;
}

function courseSelectionNote(course) {
  const selection = course.selection;
  if (!selection || selection.mode !== "choose-one" || !Array.isArray(selection.options)) return "";
  const options = selection.options.map(option => option.name).filter(Boolean).join(", ");
  return `Pilih 1 ${selection.basis}: ${options}.`;
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
  const status = statusLabel(manifest.status, manifest.maintainer);
  const title = `${manifest.institution} · ${manifest.program} · ${period}`;
  const meta = `${manifest.academic_year} · ${manifest.total_sks} SKS · ${manifest.courses.length} mata kuliah`;

  setText("#hero-course-count", manifest.courses.length);
  setText("#hero-preview-pack", title);
  setText("#hero-preview-meta", meta);
  setText("#hero-preview-status", status);
  setText("#pack-kicker", entry.maintainer === "ramu" ? "Ramu Maintained pack" : "Community pack");
  setText("#pack-title", title);
  setText("#pack-meta", `${meta} · pack ${manifest.pack_version}`);
  setText("#pack-status", status);
  setText("#closing-pack-label", title);
  bindSetupLinks(entry);

  const preview = document.querySelector("#hero-preview-courses");
  if (preview) {
    const visible = manifest.courses.slice(0, 4);
    preview.innerHTML = visible.map(course => `
      <div class="preview-course">
        <code>${escapeHtml(courseDisplayCode(course))}</code>
        <strong>${escapeHtml(course.short_name)}</strong>
        <span>${escapeHtml(course.sks)} SKS</span>
      </div>
    `).join("") + (manifest.courses.length > visible.length
      ? `<div class="preview-more">+${manifest.courses.length - visible.length} mata kuliah lain di pack ini</div>`
      : "");
  }

  const target = document.querySelector("#course-list");
  if (!target) return;
  target.innerHTML = manifest.courses.map(course => `
    <article class="course-card">
      <div class="course-top"><span class="course-code">${escapeHtml(courseDisplayCode(course))}</span><span class="course-sks">${escapeHtml(course.sks)} SKS</span></div>
      <h3>${escapeHtml(course.short_name)}</h3>
      <p class="course-focus">${escapeHtml(course.focus || "Materi dan tugas mata kuliah")}</p>
      ${courseSelectionNote(course) ? `<p class="small-note">${escapeHtml(courseSelectionNote(course))}</p>` : ""}
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
function saveProgress(id, progress) {
  try {
    localStorage.setItem(storageKey(id), JSON.stringify(progress));
    return true;
  } catch {
    return false;
  }
}

// Progres lokal hanya mencatat konfirmasi pengguna, bukan keadaan ChatGPT.
 // Hash isi aktual membedakan revisi tanpa menggantungkan semuanya pada pack_version.
const contentHashes = new Map();
async function hashBytes(bytes) {
  if (!globalThis.crypto?.subtle) throw new Error("Digest tidak tersedia");
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, "0")).join("");
}

function sourceHash(url) {
  if (!contentHashes.has(url)) {
    const promise = fetch(url, { cache: "no-store" }).then(async response => {
      if (!response.ok) throw new Error("Source tidak dapat dimuat");
      return hashBytes(await response.arrayBuffer());
    });
    contentHashes.set(url, promise);
    promise.catch(() => { if (contentHashes.get(url) === promise) contentHashes.delete(url); });
  }
  return contentHashes.get(url);
}

// Sidik komponen disimpan terpisah: pengguna mendapat tindakan yang sesuai,
 // tanpa mengira website dapat membaca keadaan ChatGPT Project mereka.
async function courseRevision(base, instructionsUrl, course, manifest) {
  const [instructions, material, academic] = await Promise.all([
    sourceHash(instructionsUrl),
    sourceHash(`${base}/${course.file}`),
    hashBytes(new TextEncoder().encode(JSON.stringify({
      pack_id: manifest.id,
      academic_year: manifest.academic_year,
      period_id: manifest.period_id,
      course
    })))
  ]);
  const parts = { instructions, material, academic, version: manifest.pack_version };
  // Formula gabungan tetap sama dengan versi website sebelumnya agar konfirmasi
  // v1 yang cocok tidak perlu diulang, tetapi konfirmasi boolean tetap ditinjau.
  const revision = await hashBytes(new TextEncoder().encode(JSON.stringify({
    pack_id: manifest.id,
    pack_version: manifest.pack_version,
    academic_year: manifest.academic_year,
    period_id: manifest.period_id,
    course,
    instructionHash: instructions,
    courseHash: material
  })));
  return { revision, parts };
}

function changeGuidance(savedParts, parts) {
  if (!savedParts || typeof savedParts !== "object" ||
    !["instructions", "material", "academic", "version"].every(key =>
      typeof savedParts[key] === "string")) {
    return ["Progres sebelumnya tidak menyimpan rincian revisi. Bandingkan Project Instructions, course pack, dan identitas mata kuliah sebelum mengonfirmasi lagi."];
  }
  const guidance = [];
  if (savedParts.instructions !== parts.instructions) {
    guidance.push("Project Instructions berubah. Periksa lalu tempel instruksi baru di Project settings; perubahan ini sendiri tidak mengharuskan upload ulang course pack.");
  }
  if (savedParts.material !== parts.material) {
    guidance.push("Isi course pack berubah. Unduh file yang baru dan ganti hanya course pack lama di Project Sources; pertahankan chat serta materi pribadi.");
  }
  if (savedParts.academic !== parts.academic) {
    guidance.push("Identitas atau metadata akademik mata kuliah berubah. Cocokkan kode, nama, dan periode dengan registrasi sebelum mengganti Project lama.");
  }
  if (savedParts.version !== parts.version) {
    guidance.push("Nomor versi pack berubah. Tinjau catatan pembaruan; perubahan versi saja tidak membuktikan file perlu diunggah ulang.");
  }
  return guidance.length ? guidance : [
    "Jejak revisi tidak cocok meski komponennya tampak sama. Periksa Project yang ada sebelum konfirmasi ulang."
  ];
}

async function inspectCourseProgress(saved, base, instructionsUrl, course, manifest) {
  if (!saved) return { status: "new", guidance: [] };
  try {
    const revisionData = await courseRevision(base, instructionsUrl, course, manifest);
    const current = typeof saved === "object" && saved.completed === true
      && saved.revision === revisionData.revision;
    return current
      ? { status: "current", ...revisionData, migrate: !saved.parts, guidance: [] }
      : { status: "review", ...revisionData,
          guidance: changeGuidance(saved?.parts, revisionData.parts) };
  } catch {
    return { status: "unavailable", guidance: [
      "Versi materi belum dapat diperiksa. Muat ulang ketika online sebelum mengonfirmasi; progres lama tidak dihapus."
    ] };
  }
}

function revisionNoteText(state) {
  return (state.guidance || []).join(" ");
}

function updateCourseState(card, state) {
  const isCurrent = state.status === "current";
  card.dataset.complete = String(isCurrent);
  card.dataset.progressStatus = state.status;
  card.querySelector(".done-pill").textContent =
    isCurrent ? "Selesai" : state.status === "review" ? "Perlu ditinjau"
      : state.status === "unavailable" ? "Belum dapat dicek" : "Belum";
  const note = card.querySelector(".revision-note");
  note.hidden = !["review", "unavailable"].includes(state.status);
  note.textContent = revisionNoteText(state);
}

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
  setText("#setup-pack-count", `${manifest.courses.length} mata kuliah · ${manifest.total_sks} SKS`);
  setText("#setup-pack-meta", `${manifest.academic_year} · ${statusLabel(manifest.status, manifest.maintainer)}`);
  const list = document.querySelector("#setup-summary-list");
  if (list) {
    const visible = manifest.courses.slice(0, 3);
    const remaining = Math.max(0, manifest.courses.length - visible.length);
    list.innerHTML = visible.map(course => `<li>${escapeHtml(course.short_name)}</li>`).join("") +
      (remaining ? `<li>+${remaining} mata kuliah lain</li>` : "");
  }
  document.title = `Setup ${manifest.name} — Ramu`;
}

async function renderSetup(entry, manifest) {
  const target = document.querySelector("#setup-courses");
  if (!target) return;
  const base = packBase(entry);
  const progress = getProgress(manifest.id);
  const instructionsUrl = `${base}/${manifest.project_instructions}`;
  const historyUrl = "https://github.com/man612/ramu/blob/main/packs/"
    + entry.manifest.replace(/\/manifest\.json$/, "/PACK-CHANGES.md");
  const states = Object.fromEntries(await Promise.all(manifest.courses.map(async course => [
    course.code,
    await inspectCourseProgress(progress[course.code], base, instructionsUrl, course, manifest)
  ])));
  // Upgrade progres lama yang sudah punya fingerprint cocok tanpa kehilangan
  // konfirmasi; boolean lama tetap review karena tidak punya jejak revisi.
  for (const course of manifest.courses) {
    const state = states[course.code];
    if (state.migrate && state.status === "current") {
      progress[course.code] = {
        completed: true, revision: state.revision,
        packVersion: manifest.pack_version, parts: state.parts
      };
    }
  }
  if (manifest.courses.some(course => states[course.code].migrate)) {
    saveProgress(manifest.id, progress);
  }
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
    const state = states[course.code];
    const complete = state.status === "current";
    const needsReview = state.status === "review" || state.status === "unavailable";
    return `
      <details class="setup-course" data-course="${escapeHtml(course.code)}" data-complete="${complete}" data-progress-status="${state.status}" ${index === 0 ? "open" : ""}>
        <summary>
          <span class="course-number">${index + 1}</span>
          <span class="setup-title"><strong>${escapeHtml(course.short_name)}</strong><span>${escapeHtml(courseDisplayCode(course))} · ${escapeHtml(course.sks)} SKS · pack ${escapeHtml(manifest.pack_version)}</span></span>
          <span class="done-pill">${complete ? "Selesai" : state.status === "review" ? "Perlu ditinjau" : state.status === "unavailable" ? "Belum dapat dicek" : "Belum"}</span>
        </summary>
        <div class="setup-body">
          <p class="course-focus"><strong>Fokus:</strong> ${escapeHtml(course.focus || "materi dan tugas mata kuliah")}</p>
          ${courseSelectionNote(course) ? `<p class="small-note"><strong>Pilihan:</strong> ${escapeHtml(courseSelectionNote(course))}</p>` : ""}
          <ol>
            <li>Jika belum ada Project untuk mata kuliah ini, buka ChatGPT lalu pilih <strong>New Project</strong>. Jika sudah ada, <strong>gunakan Project lama</strong> dan ikuti panduan update—jangan membuat duplikat.</li>
            <li>Untuk Project baru, beri nama <strong>${escapeHtml(course.project_name)}</strong>, kemudian pilih <strong>Project-only memory</strong> bila tersedia; Project lama bisa memeriksa pilihan itu melalui Project settings.</li>
            <li>Buka <strong>⋯ → Project settings → Project Instructions</strong>, lalu tempel instruksi Ramu dari langkah 2.</li>
            <li>Untuk Project baru, tekan <strong>Unduh paket (.txt)</strong>. Untuk Project lama, unduh ulang hanya jika isi course pack perlu diperbarui.</li>
            <li>Di Project, buka area <strong>Sources</strong> atau <strong>Project Sources</strong>, lalu unggah file yang baru diunduh. Saat update, cocokkan versi dan hapus hanya source course pack lama yang tergantikan; jangan hapus materi pribadi atau chat. Nama tombol dapat berbeda antar versi ChatGPT.</li>
          </ol>
          <div class="inline-actions">
            <button class="small-button copy-project" type="button" data-text="${escapeHtml(course.project_name)}">Salin nama Project</button>
            <button class="small-button download-course-pack" type="button" data-course="${escapeHtml(course.code)}">Unduh paket (.txt)</button>
            <a class="small-button" href="https://chatgpt.com/" target="_blank" rel="noopener">Buka ChatGPT</a>
          </div>
          <p class="small-note">Course pack menjadi source Project. Screenshot soal, rubrik, atau materi tambahan cukup dimasukkan saat dibutuhkan.</p>
          <p class="small-note revision-note" role="status" ${needsReview ? "" : "hidden"}>${escapeHtml(revisionNoteText(state))}</p>
          <a class="small-note revision-history" href="${escapeHtml(historyUrl)}" target="_blank" rel="noopener" ${needsReview ? "" : "hidden"}>Baca riwayat perubahan pack →</a>
          <label class="complete-check"><input type="checkbox" data-course-check="${escapeHtml(course.code)}" ${complete ? "checked" : ""}><span>Aku sudah memastikan Project ini menggunakan instruksi dan course pack yang ditinjau.</span></label>
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
    input.addEventListener("change", async () => {
      const code = input.dataset.courseCheck;
      const card = input.closest(".setup-course");
      if (!input.checked) {
        progress[code] = false;
        states[code] = { status: "new" };
      } else {
        input.disabled = true;
        try {
          const course = manifest.courses.find(item => item.code === code);
          if (!course) throw new Error("Mata kuliah tidak ditemukan");
          const { revision, parts } = await courseRevision(base, instructionsUrl, course, manifest);
          progress[code] = {
            completed: true,
            revision,
            packVersion: manifest.pack_version,
            parts
          };
          states[code] = { status: "current", revision, parts, guidance: [] };
        } catch {
          input.checked = false;
          states[code] = { status: "unavailable", guidance: [
            "Versi materi belum dapat diperiksa. Muat ulang ketika online sebelum mengonfirmasi."
          ] };
        } finally {
          input.disabled = false;
        }
      }
      saveProgress(manifest.id, progress);
      updateCourseState(card, states[code]);
      updateProgress(manifest, states);
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
  updateProgress(manifest, states);
}

function updateProgress(manifest, states) {
  const done = manifest.courses.filter(course => states[course.code]?.status === "current").length;
  const review = manifest.courses.filter(course =>
    ["review", "unavailable"].includes(states[course.code]?.status)
  ).length;
  const title = document.querySelector("#progress-title");
  const bar = document.querySelector("#progress-bar");
  if (title) title.textContent = `${done} dari ${manifest.courses.length} dikonfirmasi`
    + (review ? ` · ${review} perlu dicek` : "");
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