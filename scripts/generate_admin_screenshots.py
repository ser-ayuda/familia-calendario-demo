"""Generate admin screenshots using Playwright and the admin_demo account.

Requires Playwright and browsers installed in .venv.
"""
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
ADMIN_USER = 'admin_demo'
ADMIN_PASS = 'admin_demo'

pages = [
    '/gestion/',
    '/admin/',
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 900})

    # go to login
    page.goto(f'{BASE}/accounts/login/')
    page.fill('input[name="username"]', ADMIN_USER)
    page.fill('input[name="password"]', ADMIN_PASS)
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle')

    for path in pages:
        url = f'{BASE}{path}'
        print('Capturing', url)
        page.goto(url)
        page.wait_for_load_state('networkidle')
        filename = OUT_DIR / (path.strip('/').replace('/', '_') or 'admin')
        filename = str(filename) + '.png'
        page.screenshot(path=filename, full_page=True)
        print('Saved', filename)

    browser.close()

print('Admin screenshots generated in', OUT_DIR)
