import requests

url = 'http://127.0.0.1:8000/accounts/login/?next=/'
try:
    r = requests.get(url, timeout=5)
    with open('tmp_login_response.html', 'w', encoding='utf-8') as f:
        f.write(f"<!-- STATUS: {r.status_code} -->\n")
        f.write(r.text)
    print('WROTE tmp_login_response.html', r.status_code)
except Exception as e:
    print('ERROR', e)
