"""Script de comprobación de endpoints para demo.

Hace peticiones a las rutas principales y muestra estado y fragmentos del contenido.
Usa autenticación básica para la ruta `/api/`.
"""
import requests
from requests.auth import HTTPBasicAuth

BASE = 'http://127.0.0.1:8000'
ADMIN_USER = 'demo_admin'
ADMIN_PASS = 'demo1234'

endpoints = [
    '/',
    '/tareas/',
    '/calendario/',
    '/eventos/',
    '/admin/',
    '/api/',
]

if __name__ == '__main__':
    for ep in endpoints:
        url = BASE + ep
        try:
            if ep.startswith('/api'):
                r = requests.get(url, auth=HTTPBasicAuth(ADMIN_USER, ADMIN_PASS), timeout=5)
            else:
                r = requests.get(url, timeout=5)
            print(f'{url} -> {r.status_code} ({len(r.text)} bytes)')
            snippet = r.text[:400].replace('\n', ' ')
            print('  snippet:', snippet[:300])
        except Exception as e:
            print(f'{url} -> ERROR: {e}')
