"""Small local test: create user/staff, miembro, tarea, evento and attempt DELETE via test Client.
Run: python manage.py runscript scripts.test_delete_event or execute via shell.
"""

from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone
from tareas.models import Miembro, Tarea, Evento, Categoria

User = get_user_model()


def run():
    print('Starting local delete-event test')
    # Create staff user
    user, created = User.objects.get_or_create(username='test_admin_local')
    # Always ensure password and staff flag (idempotent)
    user.set_password('test_admin_local')
    user.is_staff = True
    user.save()
    if created:
        print('Created staff user test_admin_local')
    else:
        print('Found existing user test_admin_local - updated password/staff flag')
    # Ensure category
    cat, _ = Categoria.objects.get_or_create(nombre='Prueba')
    import time
    tarea_name = f"Tarea prueba {int(time.time())}"
    tarea = Tarea.objects.create(nombre=tarea_name, categoria=cat, creado_por=user)
    miembro, _ = Miembro.objects.get_or_create(nombre='Miembro prueba', defaults={'usuario': user})
    # Ensure miembro.usuario is set to our user
    if miembro.usuario_id != user.id:
        miembro.usuario = user
        miembro.save()
    inicio = timezone.now()
    fin = inicio + timezone.timedelta(minutes=30)
    evento = Evento.objects.create(tarea=tarea, miembro=miembro, inicio=inicio, fin=fin, creado_por=user)
    print('Created evento id=', evento.id)

    c = Client()
    logged = c.login(username='test_admin_local', password='test_admin_local')
    print('Login ok?', logged)
    # perform DELETE
    url = f'/api/eventos/{evento.id}/'
    print('Calling DELETE', url)
    resp = c.delete(url)
    print('Status code:', resp.status_code)
    try:
        print('Body:', resp.json())
    except Exception:
        print('Body not JSON or empty')

if __name__ == '__main__':
    run()
