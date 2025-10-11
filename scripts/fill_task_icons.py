"""
Fill missing Tarea.icono values based on category.

Usage:
  python manage.py shell -c "from scripts import fill_task_icons; fill_task_icons.run()"
This import-based invocation avoids encoding/exec issues on Windows.
"""
from tareas.models import Tarea

# Map category name (lower) to emoji
MAP = {
    'cocina': '🍽️',
    'limpieza': '🧹',
    'mascotas': '🐶',
    'habitación': '🛏️',
    'habitacion': '🛏️',
}


def run():
    updated = 0
    examples = []
    for t in Tarea.objects.all():
        if not t.icono or t.icono.strip() == '':
            cat = (t.categoria.nombre.lower() if t.categoria and t.categoria.nombre else '')
            icon = MAP.get(cat, '🛠️')
            t.icono = icon
            t.save(update_fields=['icono'])
            updated += 1
            if len(examples) < 8:
                examples.append((t.id, t.nombre, t.categoria.nombre if t.categoria else None, t.icono))

    print('UPDATED_TASK_ICONS', updated)
    for e in examples:
        print('EX', e)


if __name__ == '__main__':
    run()
