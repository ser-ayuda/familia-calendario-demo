import requests

base = 'http://127.0.0.1:8000'
login_url = base + '/accounts/login/'
session = requests.Session()

# Get the login page to get cookies and any csrf token
r = session.get(login_url + '?next=/', timeout=5)
print('GET login status', r.status_code)

# Prefer the csrftoken from cookies (Django sets it on GET). Fallback to parsing the form.
csrf = session.cookies.get('csrftoken')
if not csrf:
    import re
    m = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', r.text)
    csrf = m.group(1) if m else None

print('csrf token found?', bool(csrf))

payload = {
    'username': 'demo',
    'password': 'demo',
}
if csrf:
    payload['csrfmiddlewaretoken'] = csrf

# Include Referer and X-CSRFToken header to satisfy Django's CSRF checks.
headers = {'Referer': login_url}
if csrf:
    headers['X-CSRFToken'] = csrf

post = session.post(login_url, data=payload, headers=headers, allow_redirects=False)
print('POST status', post.status_code)
print('Location header:', post.headers.get('Location'))

# follow
if 'Location' in post.headers:
    r2 = session.get(base + post.headers['Location'])
    print('Followed to:', r2.status_code, r2.url)
else:
    print('No redirect')
