"""Generate demo screenshots using Playwright (headless Chromium).

This script logs in with the demo user and captures pages:
- / (home after login)
- /tareas/
- /calendario/
- /gestion/ (requires staff; demo is not staff so skip)

Fallback: if Playwright is not installed, prints instructions to install it.
"""
import os
import sys
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / 'demo_screenshots'
OUT_DIR.mkdir(exist_ok=True)

try:
    from playwright.sync_api import sync_playwright
except Exception:
    print("Playwright not installed. Install with: .venv\\Scripts\\python.exe -m pip install playwright && .venv\\Scripts\\playwright.exe install chromium")
    sys.exit(1)

BASE = 'http://127.0.0.1:8000'
DEMO_USER = 'demo'
DEMO_PASS = 'demo'

pages = [
    '/',
    '/tareas/',
    '/calendario/',
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 800})

    # go to login
    page.goto(f'{BASE}/accounts/login/')
    page.fill('input[name="username"]', DEMO_USER)
    page.fill('input[name="password"]', DEMO_PASS)
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle')

    for path in pages:
        url = f'{BASE}{path}'
        print('Capturing', url)
        page.goto(url)
        page.wait_for_load_state('networkidle')
        filename = OUT_DIR / (path.strip('/').replace('/', '_') or 'home')
        # ensure filename safe
        filename = str(filename) + '.png'
        page.screenshot(path=filename, full_page=True)
        print('Saved', filename)

    browser.close()

print('Screenshots generated in', OUT_DIR)
