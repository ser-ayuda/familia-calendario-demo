import requests
r = requests.get('http://127.0.0.1:8000/accounts/login/?next=/', timeout=10)
print('Status', r.status_code)
html = r.text
print('Occurrences of "Entrar":', html.count('Entrar'))
print('Occurrences of "Salir":', html.count('Salir'))
print('Count of <form:', html.count('<form'))
