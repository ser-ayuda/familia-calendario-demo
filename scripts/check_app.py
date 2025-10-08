#!/usr/bin/env python3
"""Smoke test for the local Django app.

Usage: run inside the project's virtualenv from the repo root:
  python scripts/check_app.py

It will try to log in with demo_admin/demo1234 and request a few pages.
"""
import re
import sys
from urllib.parse import urljoin

try:
    import requests
except Exception:
    print('The requests package is required. Install with: pip install requests')
    raise

BASE = 'http://127.0.0.1:8000'
LOGIN_URL = urljoin(BASE, '/accounts/login/')

def get_csrf_from_html(html):
    m = re.search(r"name=['\"]csrfmiddlewaretoken['\"]\s+value=['\"](?P<t>[^'\"]+)['\"]", html)
    if m:
        return m.group('t')
    # fallback: look for csrftoken cookie later
    return None

def main():
    s = requests.Session()
    print('GET', LOGIN_URL)
    r = s.get(LOGIN_URL, timeout=10)
    print('Login page status:', r.status_code)
    csrf = get_csrf_from_html(r.text)
    if not csrf:
        csrf = s.cookies.get('csrftoken')
    if not csrf:
        print('Could not find CSRF token; aborting')
        sys.exit(2)

    payload = {
        'username': 'demo_admin',
        'password': 'demo1234',
        'csrfmiddlewaretoken': csrf,
        'next': '/',
    }

    headers = {'Referer': LOGIN_URL}
    print('POST login')
    r2 = s.post(LOGIN_URL, data=payload, headers=headers, timeout=10)
    print('Login POST status:', r2.status_code)

    # After login, try key pages
    pages = ['/', '/tareas/', '/miembros/']
    for p in pages:
        url = urljoin(BASE, p)
        try:
            rr = s.get(url, timeout=10)
            print(f'GET {p} ->', rr.status_code)
        except Exception as e:
            print(f'GET {p} failed:', e)

    # quick content check for dashboard
    rhome = s.get(BASE, timeout=10)
    print('Home page length:', len(rhome.text))

if __name__ == '__main__':
    main()
