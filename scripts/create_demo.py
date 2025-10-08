# Script para aplicar migraciones y crear datos demo
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hogar.settings')

import django
from django.core.management import call_command

django.setup()

def run_migrations():
    # Do not run makemigrations in the demo script to avoid interactive prompts.
    # Assume migrations files are present in the repo. Only run migrate.
    print('Running migrate...')
    try:
        call_command('migrate', verbosity=2)
    except Exception as e:
        print('migrate error:', e)

def create_demo_user_and_data():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username = 'demo_admin'
    password = 'demo1234'
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, 'demo@example.com', password)
        print(f'Created superuser: {username} / {password}')
    else:
        print('Superuser already exists:', username)

    from tareas.models import Categoria, Miembro, Tarea, Evento
    from django.utils import timezone
    from datetime import timedelta

    c, _ = Categoria.objects.get_or_create(nombre='Demo', defaults={'descripcion': 'Categoría demo para portfolio'})
    m, _ = Miembro.objects.get_or_create(nombre='Ana', defaults={'color_hex': '#FF8888'})
    t1, _ = Tarea.objects.get_or_create(nombre='Recoger juguetes', defaults={'descripcion': 'Ordenar la sala y guardar juguetes', 'categoria': c, 'puntuacion': 1})
    t2, _ = Tarea.objects.get_or_create(nombre='Poner lavadora', defaults={'descripcion': 'Separar ropa y poner lavadora', 'categoria': c, 'puntuacion': 2})
    now = timezone.now()
    e1, _ = Evento.objects.get_or_create(tarea=t1, miembro=m, inicio=now, fin=now + timedelta(minutes=30), defaults={'estado': 'pendiente'})

    print('Demo data created: Categoria id', c.id, 'Miembro id', m.id, 'Tareas ids', t1.id, t2.id)


def run_management_seed_commands():
    """Invoke bundled management commands that create the full original demo dataset.

    The project already contains two management commands under
    `tareas/management/commands/`: `crear_demo` and `seed_data`.
    `seed_data` is the script that creates the original default members,
    categories, tasks and example events. We call them here so the demo
    DB matches the original project dataset.
    """
    try:
        print('Running management command: crear_demo')
        call_command('crear_demo')
    except Exception as e:
        print('crear_demo failed:', e)
    try:
        print('Running management command: seed_data')
        # seed_data creates members, categories, tasks and sample events
        call_command('seed_data')
    except Exception as e:
        print('seed_data failed:', e)

if __name__ == '__main__':
    run_migrations()
    create_demo_user_and_data()
    # Populate the fuller original demo dataset using built-in management commands
    run_management_seed_commands()
    print('Done.')
