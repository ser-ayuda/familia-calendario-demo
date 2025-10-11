from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from tareas.models import Miembro, Tarea, Categoria, Evento


class Command(BaseCommand):
    help = "Crea 5 miembros con colores únicos y 5 tareas por miembro para esta semana"

    def handle(self, *args, **options):
        # Correlacionar usuarios y miembros existentes
        from django.db import transaction
        with transaction.atomic():
            # 1. Para cada miembro sin usuario, crear usuario y asociar
            for miembro in Miembro.objects.filter(usuario__isnull=True):
                username = miembro.nombre.lower().replace(' ', '_')
                user, created = User.objects.get_or_create(username=username)
                if created or not user.has_usable_password():
                    user.set_password('Bien11')
                    user.save()
                miembro.usuario = user
                miembro.save()
            # 2. Para cada usuario sin miembro, crear miembro y asociar
            for user in User.objects.filter(miembro__isnull=True):
                nombre = user.username.capitalize()
                miembro, created = Miembro.objects.get_or_create(nombre=nombre)
                miembro.usuario = user
                miembro.save()
                if not user.has_usable_password():
                    user.set_password('Bien11')
                    user.save()
            # 3. Para todos los usuarios, si el password no es usable, poner 'Bien11'
            for user in User.objects.all():
                if not user.has_usable_password():
                    user.set_password('Bien11')
                    user.save()
        admin_user, _ = User.objects.get_or_create(
            username='admin', defaults={'is_staff': True, 'is_superuser': True}
        )
        if not admin_user.password:
            admin_user.set_password('admin')
            admin_user.save()

        colores = ["#e6194b", "#3cb44b", "#0082c8", "#f58231", "#911eb4"]
        iconos = ["👩", "👨", "🧒", "👦", "👵"]
        nombres = ["Mamá", "Papá", "Hijo 1", "Hijo 2", "Abuela"]

        miembros = []
        for idx, nombre in enumerate(nombres):
            miembro, _ = Miembro.objects.get_or_create(
                nombre=nombre, defaults={"color_hex": colores[idx], "icono": iconos[idx]}
            )
            miembros.append(miembro)

        now = timezone.localtime()
        lunes = now - timedelta(days=(now.weekday()))
        lunes = lunes.replace(hour=0, minute=0, second=0, microsecond=0)

        # Crear categorías
        categorias = [
            ("Cocina", "Tareas de cocina"),
            ("Limpieza", "Tareas de limpieza"),
            ("Mascotas", "Cuidado de mascotas"),
            ("Habitación", "Tareas de habitación"),
        ]
        cat_objs = {}
        for nombre, desc in categorias:
            # current Categoria model only has nombre and descripcion
            cat, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={"descripcion": desc})
            cat_objs[nombre] = cat

        tareas_tipos = [
            ("Lavar platos", "Cocina", 15, 1, "lavar"),
            ("Sacar basura", "Limpieza", 10, 1, "basura"),
            ("Pasear perro", "Mascotas", 30, 2, "perro"),
            ("Hacer cama", "Habitación", 10, 1, "cama"),
            ("Barrer salón", "Limpieza", 20, 2, "barrer"),
            ("Preparar desayuno", "Cocina", 18, 1, "desayuno"),
            ("Regar plantas", "Limpieza", 12, 1, "plantas"),
            ("Limpiar baño", "Limpieza", 25, 2, "baño"),
            ("Alimentar gato", "Mascotas", 8, 1, "gato"),
            ("Doblar ropa", "Habitación", 14, 1, "ropa"),
            ("Poner lavadora", "Cocina", 16, 1, "lavadora"),
            ("Limpiar ventanas", "Limpieza", 22, 2, "ventanas"),
            ("Sacar al gato", "Mascotas", 15, 1, "gato"),
            ("Ordenar juguetes", "Habitación", 10, 1, "juguetes"),
            ("Preparar cena", "Cocina", 20, 2, "cena"),
        ]

        # Limpiar duplicados de tareas generales (solo si no tienen eventos asociados)
        for nombre, _, _, _, _ in tareas_tipos:
            tareas = Tarea.objects.filter(nombre=nombre)
            if tareas.count() > 1:
                # Mantener solo una, eliminar las demás si no tienen eventos
                keep = tareas.first()
                for t in tareas[1:]:
                    if not t.eventos.exists():
                        t.delete()

        # Crear tareas generales (sin asignar a miembro ni horario) y rellenar campos vacíos
        tarea_objs = {}
        for nombre, cat, dur_min, puntos, tag in tareas_tipos:
            tarea = Tarea.objects.filter(nombre=nombre).first()
            if not tarea:
                tarea = Tarea.objects.create(
                    nombre=nombre,
                    descripcion=f"Tarea de {cat}",
                    categoria=cat_objs[cat],
                    tag=tag,
                    puntuacion=puntos,
                    premio=0.10,
                    tiempo_estimado=dur_min,
                )
            else:
                updated = False
                if not tarea.descripcion:
                    tarea.descripcion = f"Tarea de {cat}"
                    updated = True
                # icono may or may not be present in the DB; only set if variable exists
                # if icono was provided in the tuple we'd set it; currently it's not
                if not tarea.categoria:
                    tarea.categoria = cat_objs[cat]
                    updated = True
                if not tarea.tag:
                    tarea.tag = tag
                    updated = True
                if not tarea.puntuacion:
                    tarea.puntuacion = puntos
                    updated = True
                if tarea.premio is None:
                    tarea.premio = 0.10
                    updated = True
                # ensure tiempo_estimado is populated
                if getattr(tarea, 'tiempo_estimado', None) in (None, 0):
                    tarea.tiempo_estimado = dur_min
                    updated = True
                if updated:
                    tarea.save()
            tarea_objs[nombre] = tarea

        created_count = 0
        # Crear eventos para cada miembro y tarea a lo largo de la semana
        for miembro in miembros:
            for i, (nombre, _, dur_min, _, _) in enumerate(tareas_tipos):
                dia = lunes + timedelta(days=i)
                inicio = dia.replace(hour=15, minute=0)
                fin = inicio + timedelta(minutes=dur_min)
                evento, created = Evento.objects.get_or_create(
                    tarea=tarea_objs[nombre],
                    miembro=miembro,
                    inicio=inicio,
                    fin=fin,
                    defaults={
                        "estado": "pendiente",
                        "creado_por": admin_user,
                    },
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Miembros: {len(miembros)}. Tareas creadas nuevas: {created_count}. Usuario admin/admin creado o existente."
        ))

        # Usuario de pruebas (no admin)
        demo, created = User.objects.get_or_create(username='demo', defaults={'is_staff': False, 'is_superuser': False})
        if created or not demo.has_usable_password():
            demo.set_password('demo')
            demo.save()
        # Vincular miembro demo con icono
        demo_member, _ = Miembro.objects.get_or_create(nombre='Demo', defaults={'color_hex': '#111827', 'icono': '👤'})
        if not hasattr(demo, 'miembro'):
            demo_member.usuario = demo
            demo_member.save()
        # Crear eventos para Demo (esta semana) si no existen
        created_demo = 0
        for i, (nombre, _, dur_min, _, _) in enumerate(tareas_tipos):
            dia = lunes + timedelta(days=i)
            inicio = dia.replace(hour=16, minute=0)  # 16:00 para distinguir
            fin = inicio + timedelta(minutes=dur_min)
            evento, created = Evento.objects.get_or_create(
                tarea=tarea_objs[nombre],
                miembro=demo_member,
                inicio=inicio,
                fin=fin,
                defaults={
                    "estado": "pendiente",
                    "creado_por": admin_user,
                },
            )
            if created:
                created_demo += 1
        self.stdout.write(self.style.SUCCESS("Usuario de pruebas demo/demo creado o existente."))
        if created_demo:
            self.stdout.write(self.style.SUCCESS(f"Eventos demo creados: {created_demo}"))
        # Garantizar al menos 1 evento de Demo hoy a las 18:00
        hoy = timezone.localdate()
        start_hoy = timezone.localtime().replace(hour=18, minute=0, second=0, microsecond=0)
        end_hoy = start_hoy + timedelta(minutes=30)
        if not Evento.objects.filter(miembro=demo_member, inicio__date=hoy).exists():
            Evento.objects.create(
                tarea=tarea_objs["Lavar platos"],
                miembro=demo_member,
                inicio=start_hoy,
                fin=end_hoy,
                estado="pendiente",
                creado_por=admin_user,
            )
            self.stdout.write(self.style.SUCCESS("Evento de hoy para Demo creado"))

        # Crear un aviso administrativo de ejemplo
        from tareas.models import Aviso
        Aviso.objects.create(
            mensaje="Este es un aviso de ejemplo para el panel de administración.",
            nivel="INFO"
        )
        self.stdout.write(self.style.SUCCESS("Aviso administrativo de ejemplo creado."))


