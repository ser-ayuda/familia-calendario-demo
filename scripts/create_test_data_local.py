# Script to run inside `python manage.py shell -c "exec(open('scripts/create_test_data_local.py').read())"`
from django.contrib.auth import get_user_model
from tareas.models import Categoria, Tarea, Miembro, Evento
from django.utils import timezone

User = get_user_model()

# Delete prior test artifacts
print('Deleting old test artifacts...')
User.objects.filter(username='test_admin_local').delete()
Evento.objects.filter(tarea__nombre__startswith='Tarea prueba').delete()
Tarea.objects.filter(nombre__startswith='Tarea prueba').delete()
Miembro.objects.filter(nombre='Miembro prueba').delete()

# Create fresh test data
user, created = User.objects.get_or_create(username='test_admin_local')
user.set_password('test_admin_local')
user.is_staff = True
user.save()
cat, _ = Categoria.objects.get_or_create(nombre='Prueba')
from time import time
name = f"Tarea prueba {int(time())}"
tarea = Tarea.objects.create(nombre=name, categoria=cat, creado_por=user)
miembro, _ = Miembro.objects.get_or_create(nombre='Miembro prueba', defaults={'usuario': user})
if miembro.usuario_id != user.id:
    miembro.usuario = user
    miembro.save()

inicio = timezone.now()
fin = inicio + timezone.timedelta(minutes=30)
evento = Evento.objects.create(tarea=tarea, miembro=miembro, inicio=inicio, fin=fin, creado_por=user)

print('CREATED_EVENT_ID', evento.id)
print('CREDENTIALS: test_admin_local / test_admin_local')
