import re
import requests
from urllib.parse import urljoin

BASE = 'http://127.0.0.1:8000'

s = requests.Session()
print('GET /')
r = s.get(BASE, timeout=10)
print('Status', r.status_code)
html = r.text

m_token = re.search(r"name=[\'\"]csrfmiddlewaretoken[\'\"]\s+value=[\'\"]([^\'\"]+)[\'\"]", html)
if not m_token:
    m_token = re.search(r"<input[^>]+name=[\'\"]csrfmiddlewaretoken[\'\"][^>]+value=[\'\"]([^\'\"]+)[\'\"]", html)

m_action = re.search(r"<form[^>]+action=[\'\"]([^\'\"]+)[\'\"]", html)

if m_token:
    token = m_token.group(1)
    print('Found CSRF token:', token[:8] + '...')
else:
    token = None
    print('No CSRF token found')

if m_action:
    action = m_action.group(1)
    print('Found form action:', action)
    logout_url = urljoin(BASE, action)
else:
    logout_url = urljoin(BASE, '/accounts/logout/')
    print('No form action found, using', logout_url)

# Send POST
print('POST to', logout_url)
headers = {}
if token:
    headers['Referer'] = BASE + '/'
    # include token in data and header
    data = {'csrfmiddlewaretoken': token}
    # set header X-CSRFToken from session cookies if present
    if 'csrftoken' in s.cookies:
        headers['X-CSRFToken'] = s.cookies['csrftoken']
    r2 = s.post(logout_url, data=data, headers=headers, allow_redirects=False, timeout=10)
else:
    r2 = s.post(logout_url, allow_redirects=False, timeout=10)

print('POST status:', r2.status_code)
print('Location header:', r2.headers.get('Location'))
print('Response length:', len(r2.text))
