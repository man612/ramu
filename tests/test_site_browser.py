#!/usr/bin/env python3
"""Browser-level regression untuk static site Ramu memakai staging yang sama seperti Pages."""

from __future__ import annotations

import json
import shutil
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import Page, expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return


def stage_site(target: Path) -> None:
    shutil.copytree(ROOT / "site", target, dirs_exist_ok=True)
    shutil.copytree(ROOT / "packs", target / "packs")
    shutil.copytree(ROOT / "schemas", target / "schemas")
    (target / ".nojekyll").touch()


def load_catalog(stage: Path) -> dict:
    return json.loads((stage / "packs/index.json").read_text(encoding="utf-8"))


def pack_manifest(stage: Path, entry: dict) -> dict:
    return json.loads((stage / "packs" / entry["manifest"]).read_text(encoding="utf-8"))


def active_entry(catalog: dict, pack_id: str | None = None) -> dict:
    if pack_id:
        for item in catalog["packs"]:
            if item["id"] == pack_id:
                return item
    default_id = catalog.get("default_pack_id")
    return next((item for item in catalog["packs"] if item["id"] == default_id), catalog["packs"][0])


def assert_no_page_errors(page: Page, errors: list[str], label: str) -> None:
    if errors:
        raise AssertionError(f"{label} menghasilkan page error: {errors}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ramu-browser-") as tmp:
        stage = Path(tmp)
        stage_site(stage)
        catalog = load_catalog(stage)
        if not catalog.get("packs"):
            raise AssertionError("Katalog pack kosong pada browser regression.")

        handler = partial(QuietHandler, directory=str(stage))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = f"http://127.0.0.1:{server.server_port}"

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                context = browser.new_context(accept_downloads=True)
                page = context.new_page()
                errors: list[str] = []
                page.on("pageerror", lambda exc: errors.append(str(exc)))

                default_entry = active_entry(catalog)
                default_manifest = pack_manifest(stage, default_entry)

                # Homepage harus benar-benar merender data katalog, bukan sekadar punya marker statis.
                page.goto(f"{base_url}/", wait_until="networkidle")
                cards = page.locator("#course-list .course-card")
                expect(cards).to_have_count(len(default_manifest["courses"]))
                if default_manifest["period_label"] not in page.locator("#pack-title").inner_text():
                    raise AssertionError("Homepage tidak menampilkan period_label pack aktif.")
                preview = page.locator("#hero-preview-courses .preview-course")
                expect(preview).to_have_count(min(4, len(default_manifest["courses"])))
                if page.locator(".phone-stage").count() != 0:
                    raise AssertionError("Homepage Phase 2 tidak boleh mengembalikan fake phone mockup.")
                if page.locator('a[href*="starter/README.md"]').count() < 1:
                    raise AssertionError("Homepage kehilangan jalur Ramu Starter untuk course tanpa public pack.")

                # Custom picker harus bisa dipakai lewat keyboard dan memilih pack lain bila tersedia.
                picker = page.locator("[data-pack-picker]").first
                trigger = picker.locator("[data-pack-picker-trigger]")
                if len(catalog["packs"]) > 1:
                    trigger.press("ArrowDown")
                    if trigger.get_attribute("aria-expanded") != "true":
                        raise AssertionError("ArrowDown tidak membuka pack picker.")
                    page.keyboard.press("Escape")
                    if trigger.get_attribute("aria-expanded") != "false":
                        raise AssertionError("Escape tidak menutup pack picker.")

                    alternate = next(item for item in catalog["packs"] if item["id"] != default_entry["id"])
                    trigger.click()
                    picker.locator(f'[data-pack-id="{alternate["id"]}"]').click()
                    page.wait_for_url(f"**?pack={alternate['id']}", wait_until="networkidle")
                    alternate_manifest = pack_manifest(stage, alternate)
                    if alternate_manifest["period_label"] not in page.locator("#pack-title").inner_text():
                        raise AssertionError("Navigasi pack picker tidak mengganti manifest yang dirender.")

                # Semester 1 punya choice slot agama: UI harus memakai label manusia, bukan ID internal.
                s1_entry = next((item for item in catalog["packs"] if item["id"] == "id.ut.accounting-s1.2026-2027.s1"), None)
                if s1_entry:
                    page.goto(f"{base_url}/?pack={s1_entry['id']}", wait_until="networkidle")
                    religion_card = page.locator("#course-list .course-card").filter(has_text="Pendidikan Agama")
                    religion_card.wait_for(state="visible")
                    if religion_card.count() != 1:
                        raise AssertionError("Homepage Semester 1 tidak merender tepat satu choice slot Pendidikan Agama.")
                    religion_text = religion_card.inner_text()
                    if "Pilih 1" not in religion_text or "sesuai data pribadi dan registrasi UT" not in religion_text:
                        raise AssertionError("Choice slot Pendidikan Agama kehilangan display_code atau basis pemilihan.")
                    if "religion-choice" in religion_text:
                        raise AssertionError("Homepage membocorkan ID internal choice slot sebagai kode akademik.")

                    page.goto(f"{base_url}/setup.html?pack={s1_entry['id']}", wait_until="networkidle")
                    religion_setup = page.locator('.setup-course[data-course="religion-choice"]')
                    religion_setup.wait_for(state="visible")
                    if religion_setup.count() != 1:
                        raise AssertionError("Setup Semester 1 tidak merender choice slot Pendidikan Agama.")
                    religion_setup.locator("summary").click()
                    setup_text = religion_setup.inner_text()
                    if "Pilih 1" not in setup_text or "sesuai data pribadi dan registrasi UT" not in setup_text:
                        raise AssertionError("Setup choice slot tidak menjelaskan pilihan resmi Semester 1.")
                    if "religion-choice ?" in setup_text:
                        raise AssertionError("Setup membocorkan ID internal choice slot sebagai kode akademik.")

                # Unknown pack ID harus fallback ke default, bukan memecahkan halaman.
                page.goto(f"{base_url}/?pack=does-not-exist", wait_until="networkidle")
                if default_manifest["period_label"] not in page.locator("#pack-title").inner_text():
                    raise AssertionError("Unknown pack tidak fallback ke default pack.")

                # Setup page: render, progress persistence, instructions, dan download course pack.
                page.goto(f"{base_url}/setup.html?pack={default_entry['id']}", wait_until="networkidle")
                layout_display = page.locator(".setup-layout").evaluate("el => getComputedStyle(el).display")
                nav_position = page.locator(".setup-nav").evaluate("el => getComputedStyle(el).position")
                if layout_display != "grid" or nav_position != "sticky":
                    raise AssertionError("Setup desktop kehilangan workspace grid atau sticky step navigation.")
                if page.locator("#setup-summary-list li").count() > 4:
                    raise AssertionError("Ringkasan pack setup kembali terlalu panjang untuk desktop workspace.")
                page.evaluate("document.querySelector('#langkah-2').scrollIntoView({block: 'center'})")
                expect(page.locator('.setup-nav a[href="#langkah-2"]')).to_have_attribute("aria-current", "step")
                setup_cards = page.locator("#setup-courses .setup-course")
                if setup_cards.count() != len(default_manifest["courses"]):
                    raise AssertionError("Setup page tidak merender seluruh course dari manifest.")

                first_course = default_manifest["courses"][0]
                checkbox = page.locator(f'[data-course-check="{first_course["code"]}"]')
                checkbox.check()
                page.reload(wait_until="networkidle")
                if not page.locator(f'[data-course-check="{first_course["code"]}"]').is_checked():
                    raise AssertionError("Progress setup tidak bertahan setelah reload.")

                open_instructions = page.locator("#open-instructions")
                instructions_href = open_instructions.get_attribute("href")
                if not instructions_href:
                    raise AssertionError("Setup page tidak memberi href Project Instructions.")
                instructions_url = urljoin(page.url, instructions_href)
                instructions_response = page.request.get(instructions_url)
                if not instructions_response.ok:
                    raise AssertionError("Project Instructions tidak dapat diambil dari setup page.")
                if "Project Instructions" not in instructions_response.text():
                    raise AssertionError("Project Instructions response tidak berisi contract yang diharapkan.")

                with page.expect_download() as download_info:
                    page.locator(f'[data-course="{first_course["code"]}"] .download-course-pack').click()
                download = download_info.value
                if not download.suggested_filename.startswith(f"ramu-{first_course['code'].lower()}-"):
                    raise AssertionError(f"Nama download course pack tidak sesuai: {download.suggested_filename}")

                assert_no_page_errors(page, errors, "normal browser flow")
                context.close()

                # localStorage bisa ditolak browser/privacy mode; interaksi tidak boleh melempar page error.
                blocked_context = browser.new_context()
                blocked_context.add_init_script(
                    "Storage.prototype.setItem = function () { throw new DOMException('blocked', 'SecurityError'); };"
                )
                blocked_page = blocked_context.new_page()
                blocked_errors: list[str] = []
                blocked_page.on("pageerror", lambda exc: blocked_errors.append(str(exc)))
                blocked_page.goto(f"{base_url}/setup.html?pack={default_entry['id']}", wait_until="networkidle")
                blocked_page.locator(f'[data-course-check="{first_course["code"]}"]').check()
                assert_no_page_errors(blocked_page, blocked_errors, "blocked localStorage flow")
                blocked_context.close()

                # Mobile viewport adalah UX contract tersendiri, bukan sekadar desktop yang dipersempit.
                mobile_context = browser.new_context(
                    viewport={"width": 390, "height": 844},
                    is_mobile=True,
                    has_touch=True,
                )
                mobile_page = mobile_context.new_page()
                mobile_errors: list[str] = []
                mobile_page.on("pageerror", lambda exc: mobile_errors.append(str(exc)))
                mobile_page.goto(f"{base_url}/", wait_until="networkidle")
                expect(mobile_page.locator(".product-preview")).to_be_visible()
                expect(mobile_page.locator(".hero-actions .primary")).to_be_visible()
                expect(mobile_page.locator("#course-list .course-card").first).to_be_visible()
                if mobile_page.locator(".mobile-dock").count():
                    raise AssertionError("Homepage mobile masih membuat bottom dock lama.")
                if mobile_page.locator('script[src="mobile.js"]').count():
                    raise AssertionError("Homepage masih memuat mobile.js lama.")
                primary_height = mobile_page.locator(".hero-actions .primary").evaluate("el => el.getBoundingClientRect().height")
                if primary_height < 44:
                    raise AssertionError(f"CTA utama mobile terlalu kecil: {primary_height}px.")
                overflow = mobile_page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                if overflow > 1:
                    raise AssertionError(f"Homepage mobile overflow horizontal {overflow}px.")
                mobile_page.goto(f"{base_url}/setup.html?pack={default_entry['id']}", wait_until="networkidle")
                expect(mobile_page.locator("#setup-courses .setup-course").first).to_be_visible()
                if mobile_page.locator(".site-header nav").is_visible():
                    raise AssertionError("Setup mobile masih menampilkan navigation links yang mengganggu task flow.")
                mobile_nav = mobile_page.locator(".setup-nav")
                if mobile_nav.evaluate("el => getComputedStyle(el).position") != "sticky":
                    raise AssertionError("Setup mobile kehilangan sticky step rail.")
                step_links = mobile_nav.locator('a[href^="#langkah-"]')
                if step_links.count() != 4:
                    raise AssertionError("Setup mobile harus mempertahankan empat langkah linear.")
                if any(step_links.nth(i).evaluate("el => el.getBoundingClientRect().height") < 44 for i in range(4)):
                    raise AssertionError("Target langkah mobile harus minimal 44px.")
                if any(not step_links.nth(i).get_attribute("aria-label") for i in range(4)):
                    raise AssertionError("Step rail mobile kehilangan aria-label saat label visual disembunyikan.")
                mobile_page.locator("#langkah-2").scroll_into_view_if_needed()
                mobile_page.wait_for_timeout(150)
                if step_links.nth(1).get_attribute("aria-current") != "step":
                    raise AssertionError("Step rail mobile tidak mengikuti langkah aktif.")
                setup_overflow = mobile_page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                if setup_overflow > 1:
                    raise AssertionError(f"Setup mobile overflow horizontal {setup_overflow}px.")
                assert_no_page_errors(mobile_page, mobile_errors, "mobile browser flow")
                mobile_context.close()

                narrow_context = browser.new_context(viewport={"width": 320, "height": 740}, is_mobile=True, has_touch=True)
                narrow_page = narrow_context.new_page()
                narrow_page.goto(f"{base_url}/", wait_until="networkidle")
                if narrow_page.evaluate("document.documentElement.scrollWidth - window.innerWidth") > 1:
                    raise AssertionError("Homepage pecah pada viewport 320px.")
                narrow_page.goto(f"{base_url}/setup.html?pack={default_entry['id']}", wait_until="networkidle")
                if narrow_page.evaluate("document.documentElement.scrollWidth - window.innerWidth") > 1:
                    raise AssertionError("Setup pecah pada viewport 320px.")
                narrow_context.close()
                browser.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    print("Site browser regression — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
