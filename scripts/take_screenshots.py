"""Playwright ile uygulamanın 10+ ekran görüntüsünü otomatik al.

Çalıştırmak için: Flask 5050'de çalışıyor olmalı.
    cd ~/Desktop/ikincielmarket
    venv/bin/python scripts/take_screenshots.py
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page

BASE = "http://localhost:5050"
OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "img"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Demo giriş bilgileri (seed-demo komutundan)
ADMIN = ("admin@ikincielmarket.local", "admin1234")
ALICE = ("alice@demo.local", "demo1234")


def shot(page: Page, name: str, full: bool = True, viewport: str = "desktop") -> None:
    path = OUT_DIR / f"{name}.png"
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)  # animasyon/hover yerleşsin
    page.screenshot(path=str(path), full_page=full)
    print(f"  ✓ {path.name} ({path.stat().st_size // 1024} KB, {viewport})")


def login(page: Page, email: str, password: str) -> None:
    page.goto(f"{BASE}/auth/login")
    page.wait_for_load_state("networkidle")
    page.locator('input[name="email"]').fill(email)
    page.locator('input[name="password"]').fill(password)
    print(f"  → login submit: {email}")
    # "Giriş yap" submit butonu (navbar search değil!)
    with page.expect_navigation(timeout=10000):
        page.get_by_role("button", name="Giriş yap").click()
    print(f"  → after submit URL: {page.url}")
    if "/auth/login" in page.url:
        # Sayfada hata mesajı var mı?
        try:
            alert = page.locator(".alert").first.text_content(timeout=2000)
            print(f"  ⚠ ALERT: {alert}")
        except Exception:
            print("  ⚠ Login başarısız ama alert yok")
        raise RuntimeError(f"Login fail: {email}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # === Masaüstü ekran görüntüleri ===
        ctx = browser.new_context(
            viewport={"width": 1366, "height": 850},
            locale="tr-TR",
        )

        # 01 — Anasayfa (anonim, Hero görünür)
        page = ctx.new_page()
        page.goto(BASE)
        shot(page, "01-anasayfa-hero")

        # 02 — Kategori filtresi (Elektronik)
        page.goto(f"{BASE}/?kategori=elektronik")
        shot(page, "02-kategori-elektronik")

        # 03 — Arama sonucu
        page.goto(f"{BASE}/?q=iphone")
        shot(page, "03-arama-iphone")

        # 04 — İlan detay (ID 1)
        page.goto(f"{BASE}/ilan/1")
        shot(page, "04-ilan-detay")

        # 05 — Kayıt formu
        page.goto(f"{BASE}/auth/register")
        shot(page, "05-kayit-formu")

        # 06 — Giriş formu
        page.goto(f"{BASE}/auth/login")
        shot(page, "06-giris-formu")

        # 07 — 404 özel sayfa
        page.goto(f"{BASE}/yokboyle-bir-sayfa")
        shot(page, "07-404-sayfasi")

        # 08 — API JSON (raw)
        page.goto(f"{BASE}/api/v1/listings")
        shot(page, "08-api-json-listings")

        page.close()
        ctx.close()

        # === Giriş yapmış kullanıcı (alice) ===
        ctx2 = browser.new_context(viewport={"width": 1366, "height": 850}, locale="tr-TR")
        page = ctx2.new_page()
        login(page, *ALICE)
        page.goto(f"{BASE}/auth/profil/alice")
        shot(page, "09-profil-sayfasi")

        # 10 — Yeni ilan formu (login gerektiriyor)
        page.goto(f"{BASE}/ilan/yeni")
        shot(page, "10-yeni-ilan-formu")

        # 11 — Favoriler
        page.goto(f"{BASE}/ilan/favorilerim")
        shot(page, "11-favorilerim")

        page.close()
        ctx2.close()

        # === Admin paneli ===
        ctx3 = browser.new_context(viewport={"width": 1366, "height": 850}, locale="tr-TR")
        page = ctx3.new_page()
        login(page, *ADMIN)

        page.goto(f"{BASE}/admin/")
        shot(page, "12-admin-dashboard")

        page.goto(f"{BASE}/admin/ilanlar")
        shot(page, "13-admin-ilanlar")

        page.goto(f"{BASE}/admin/kategoriler")
        shot(page, "14-admin-kategoriler")

        page.close()
        ctx3.close()

        # === Mesaj thread (alice → satıcı) ===
        ctx_msg = browser.new_context(viewport={"width": 1366, "height": 850}, locale="tr-TR")
        page = ctx_msg.new_page()
        login(page, *ALICE)
        page.goto(f"{BASE}/mesaj/")
        shot(page, "18-mesaj-inbox")
        # Inbox'taki ilk thread'e tıkla (varsa)
        try:
            page.locator("a.list-group-item").first.click()
            page.wait_for_load_state("networkidle", timeout=5000)
            shot(page, "19-mesaj-thread")
        except Exception as e:
            print(f"  ⚠ thread tıklanamadı: {e}")
        page.close()
        ctx_msg.close()

        # === İngilizce arayüz ===
        ctx4 = browser.new_context(viewport={"width": 1366, "height": 850}, locale="en-US")
        page = ctx4.new_page()
        page.goto(f"{BASE}/dil/en")
        page.goto(BASE)
        shot(page, "15-anasayfa-english")
        page.close()
        ctx4.close()

        # === Mobil viewport ===
        ctx5 = browser.new_context(
            viewport={"width": 390, "height": 844},  # iPhone 13
            device_scale_factor=2,
            is_mobile=True,
            locale="tr-TR",
        )
        page = ctx5.new_page()
        page.goto(BASE)
        shot(page, "16-mobil-anasayfa", viewport="mobile")

        page.goto(f"{BASE}/ilan/1")
        shot(page, "17-mobil-ilan-detay", viewport="mobile")
        page.close()
        ctx5.close()

        browser.close()

    print(f"\n✓ Tüm ekran görüntüleri: {OUT_DIR}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"HATA: {e}", file=sys.stderr)
        sys.exit(1)
