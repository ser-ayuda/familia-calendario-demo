from django.utils.dateparse import parse_date
import json
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test

# Endpoint para borrar eventos futuros de una tarea desde una fecha
@require_POST
@login_required
@user_passes_test(lambda u: u.is_staff)
def borrar_eventos_futuros(request, tarea_id):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body.decode())
        fecha_desde = parse_date(data.get('fecha_desde'))
        if not fecha_desde:
            return JsonResponse({'ok': False, 'error': 'Fecha inválida'})
        borrados = Evento.objects.filter(tarea_id=tarea_id, inicio__date__gte=fecha_desde).delete()
        return JsonResponse({'ok': True, 'borrados': borrados[0]})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

# Vista para marcar un aviso como visto
@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def marcar_aviso_visto(request, aviso_id):
    from .models import Aviso
    try:
        aviso = Aviso.objects.get(id=aviso_id)
        aviso.visto = True
        aviso.save(update_fields=["visto"])
        return JsonResponse({"ok": True})
    except Aviso.DoesNotExist:
        return JsonResponse({"ok": False, "error": "No existe"}, status=404)
from django.shortcuts import render, redirect
from django import forms
from .models import Evento, Miembro, Categoria, Aviso, Tarea
from django.utils.timezone import now
def registrar_auditoria(usuario, accion, objeto, tipo_objeto):
    try:
        mensaje = f"[{accion.upper()}] {tipo_objeto}: {str(objeto)} por {usuario.username if usuario else 'sistema'}"
        Aviso.objects.create(
            mensaje=mensaje,
            nivel="INFO",
            creado_en=now(),
            usuario=usuario if usuario.is_authenticated else None
        )
    except Exception:
        pass
from decimal import Decimal
# --- Iconos sugeridos por categoría ---
ICONOS_DEPORTE = [
    "🏆","💪","🎯","🥇","🥈","🥉","🏅","🎽","⚡","🧗","🏃","🚴","🤸","🏋️","🤼","🤽","🏄","🏊","⛹️","🤾","🧘","🛹","🛼","🪂","🧗‍♀️","🧗‍♂️","🏓","🏸","🏒","🏑","🏏","🥅","⛳","🏹","🎣","🤿","🥊","🥋","🛷","⛸️","🥌","🛶","🚣","🏇","🏂","🏄‍♂️","🏄‍♀️","🏊‍♂️","🏊‍♀️","🤽‍♂️","🤽‍♀️","🚴‍♂️","🚴‍♀️","🚵‍♂️","🚵‍♀️","🤸‍♂️","🤸‍♀️","🤾‍♂️","🤾‍♀️","🤹‍♂️","🤹‍♀️","🥏","🏐","🏈","🏉","🏀","⚽"
]
ICONOS_PREMIOS = [
    "🏆","🥇","🥈","🥉","🎖️","🎗️","🏵️","🎫","🎟️","🎉","🎊","🏅","👑","🌟","⭐","💎","🎀","🪙","💰","🤑","🎁","🥂","🍾","🍬","🍭","🍫","🍪","🍩","🍦","🍰","🍧","🍨","🍮","🍯","🍎","🍏","🍊","🍋","🍉","🍇","🍓","🍒","🍑","🍍","🥭","🥝","🍅","🥥","🥧"
]
ICONOS_PERSONAS = [
    "😀","🤩","😎","👨‍👩‍👧‍👦","👶","👦","👧","👨","👩","🧑","👴","👵","🧓","👨‍🎓","👩‍🎓","🦸","🦸‍♀️","🦹","🦹‍♀️","🧑‍🏫","🧑‍🔬","🧑‍💻","🧑‍🎨","🧑‍🚀","🧑‍🚒","🧑‍⚕️","🧑‍🍳","🧑‍🔧","🧑‍🌾","🧑‍🎤","🧑‍✈️","🧑‍🚗","🧑‍🏭","🧑‍🔬"
]
ICONOS_CASA = [
    "🏠","🏡","🏘️","🏚️","🏢","🏫","🏥","🏦","🏛️","🏖️","🏕️","🏜️","🏞️","🌄","🌅","🌃","🌌","🌠","🌈","🧹","🧑‍🍳","🛏️","🧺","🪑","🛋️","🚪","🪟","🛁","🚿","🚽","🧻","🪠","🧼","🪥","🧽","🧴","🧯","🛒","🧊","🧂","🥄","🍴","🍽️","🥣","🥡","🥢","🥤","🧃","🧉"
]
ICONOS_ESTUDIO = [
    "📚","📝","🚩","💡","⏳","✅","🌱","💼","📈","📉","📊","📅","📆","🗂️","🗃️","🗄️","📋","📁","📂","🗒️","🖊️","🖋️","✏️","🖍️","🖌️","🖥️","💻","🖱️","⌨️","📱","📲","📞","☎️","📟","📠","🧮","📐","📏","📎","🖇️","📌","📍","✂️","📢","📣","📯","🔔","🔕","🔊","🔉","🔈","🔇"
]
ICONOS_ARTE = [
    "🎨","🎭","🎬","🎤","🎧","🎼","🎹","🥁","🎷","🎺","🎸","🪕","🎻","🖼️","📝","✏️","🖌️","🖍️","🖋️","🖊️"
]
ICONOS_JUEGOS = [
    "🎲","🎯","🎮","🕹️","🎰","🧩","🧸","🪁","🪀","🃏","🀄","🎴"
]


# Reto-related functionality removed for public demo. If you need to restore it, check the backups in templates/reto-backup/ and tareas/models.py.reto.bak



def es_admin(user):
    return user.is_staff

# Reto-related views removed for the public demo. These stubs return 404 to avoid runtime errors
from django.http import Http404

def admin_retos(request):
    raise Http404("La funcionalidad 'retos' no está disponible en esta versión pública.")

def aprobar_reto(request, reto_id):
    raise Http404("La funcionalidad 'retos' no está disponible en esta versión pública.")

def rechazar_reto(request, reto_id):
    raise Http404("La funcionalidad 'retos' no está disponible en esta versión pública.")


def demo_public(request):
    """Vista pública mínima para demo/portafolio: lista algunas tareas."""
    try:
        tareas_qs = Tarea.objects.all()[:10]
    except Exception:
        tareas_qs = []
    html = "<html><head><title>Demo - Tareas</title></head><body>"
    html += "<h1>Demo - Tareas</h1><ul>"
    for t in tareas_qs:
        html += f"<li><strong>{t.nombre}</strong>: {str(t.descripcion)[:120]}</li>"
    html += "</ul>"
    html += "<p>Usuario demo: <code>demo</code> / <code>demo</code></p>"
    html += "</body></html>"
    return HttpResponse(html)
# Vista de administración de eventos generados
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
@user_passes_test(es_admin)
def admin_eventos(request):
    eventos = Evento.objects.select_related('tarea', 'miembro', 'tarea__categoria')
    miembro_f = request.GET.get('miembro')
    categoria_f = request.GET.get('categoria')
    estado_f = request.GET.get('estado')
    if miembro_f:
        eventos = eventos.filter(miembro_id=miembro_f)
    if categoria_f:
        eventos = eventos.filter(tarea__categoria_id=categoria_f)
    if estado_f:
        eventos = eventos.filter(estado=estado_f)
    total_eventos = eventos.count()
    eventos = eventos.order_by('-inicio')
    paginator = Paginator(eventos, 12)
    page_number = request.GET.get('page')
    eventos_paginated = paginator.get_page(page_number)
    miembros_qs = Miembro.objects.filter(usuario__isnull=False, usuario__is_staff=False)
    miembros = list(miembros_qs.values('id', 'nombre'))
    categorias = Categoria.objects.all()
    avisos = Aviso.objects.filter(visto=False).order_by('-creado_en')
    from django.contrib import messages
    tareas_qs = Tarea.objects.all().order_by('nombre')
    tareas = list(tareas_qs.values('id', 'nombre'))
    horas = [f"{h:02d}:00" for h in range(7, 23)]
    return render(request, "admin_eventos.html", {
        "eventos_paginated": eventos_paginated,
        "miembros": miembros,
        "categorias": categorias,
        "total_eventos": total_eventos,
        "avisos": avisos,
        "tareas": tareas,
        "horas": horas,
    })
    categorias = Categoria.objects.all()
    return render(request, "admin_eventos.html", {
        "eventos_paginated": eventos_paginated,
        "miembros": miembros,
        "categorias": categorias,
        "total_eventos": total_eventos,
    })

def es_admin(user):
    return user.is_staff

@user_passes_test(es_admin)
@login_required
def admin_miembros(request):
    from django.contrib import messages
    # Ejemplo: messages.info(request, "Vista de administración de miembros cargada correctamente.")
    avisos = Aviso.objects.filter(visto=False).order_by('-creado_en')
    return render(request, "admin_miembros.html", {"avisos": avisos})
@login_required
def home(request):
    # Calcular miembros_stats igual que en calendario_context
    from .models import Miembro, Evento
    from django.db.models import Sum
    import calendar
    from django.utils import timezone
    from datetime import timedelta
    hoy = timezone.localdate()
    lunes = hoy - timedelta(days=hoy.weekday())
    domingo = lunes + timedelta(days=6)
    month_start = hoy.replace(day=1)
    _, month_last = calendar.monthrange(hoy.year, hoy.month)
    month_end = hoy.replace(day=month_last)
    miembros = Miembro.objects.filter(usuario__isnull=False, usuario__is_staff=False)
    miembros_stats = []
    year_start = hoy.replace(month=1, day=1)
    year_end = hoy.replace(month=12, day=31)
    # Para mostrar info personalizada al usuario conectado
    semana_total_usuario = None
    mes_total_usuario = None
    semana_rango = None
    mes_nombre = None

    import locale
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except:
            pass

    if request.user.is_authenticated and hasattr(request.user, 'miembro') and request.user.miembro:
        m = request.user.miembro
        semana_total_usuario = (
            Evento.objects.filter(
                miembro=m,
                inicio__date__gte=lunes,
                inicio__date__lte=domingo,
                estado='aprobada',
            ).aggregate(total=Sum('tarea__premio'))['total'] or 0
        )
        mes_total_usuario = (
            Evento.objects.filter(
                miembro=m,
                inicio__date__gte=month_start,
                inicio__date__lte=month_end,
                estado='aprobada',
            ).aggregate(total=Sum('tarea__premio'))['total'] or 0
        )
        mes_es = hoy.strftime('%B').capitalize()
        semana_rango = f"Semana del {lunes.strftime('%d/%m')} al {domingo.strftime('%d/%m')} de {mes_es} de {hoy.year}"
        mes_nombre = f"{mes_es} del {hoy.year}"

    for m in miembros:
        semana_sum = (
            Evento.objects.filter(
                miembro=m,
                inicio__date__gte=lunes,
                inicio__date__lte=domingo,
                estado='aprobada',
            ).aggregate(total=Sum('tarea__puntuacion'))['total'] or 0
        )
        semana_premio = (
            Evento.objects.filter(
                miembro=m,
                inicio__date__gte=lunes,
                inicio__date__lte=domingo,
                estado='aprobada',
            ).aggregate(total=Sum('tarea__premio'))['total'] or 0
        )
        mes_sum = (
            Evento.objects.filter(
                miembro=m,
                inicio__date__gte=month_start,
                inicio__date__lte=month_end,
                estado='aprobada',
            ).aggregate(total=Sum('tarea__puntuacion'))['total'] or 0
        )
        mes_premio = (
            Evento.objects.filter(
                miembro=m,
                inicio__date__gte=month_start,
                inicio__date__lte=month_end,
                estado='aprobada',
            ).aggregate(total=Sum('tarea__premio'))['total'] or 0
        )
        year_sum = (
            Evento.objects.filter(
                miembro=m,
                inicio__date__gte=year_start,
                inicio__date__lte=year_end,
                estado='aprobada',
            ).aggregate(total=Sum('tarea__puntuacion'))['total'] or 0
        )
        year_premio = (
            Evento.objects.filter(
                miembro=m,
                inicio__date__gte=year_start,
                inicio__date__lte=year_end,
                estado='aprobada',
            ).aggregate(total=Sum('tarea__premio'))['total'] or 0
        )
        semana_pendientes = Evento.objects.filter(
            miembro=m,
            inicio__date__gte=lunes,
            inicio__date__lte=domingo,
            estado='pendiente',
        ).count()
        mes_pendientes = Evento.objects.filter(
            miembro=m,
            inicio__date__gte=month_start,
            inicio__date__lte=month_end,
            estado='pendiente',
        ).count()
        miembros_stats.append({
            'id': m.id,
            'nombre': m.nombre,
            'color_hex': m.color_hex,
            'icono': m.icono,
            'semana': semana_sum,
            'semana_premio': semana_premio,
            'mes': mes_sum,
            'mes_premio': mes_premio,
            'anio': year_sum,
            'anio_premio': year_premio,
            'semana_pendientes': semana_pendientes,
            'mes_pendientes': mes_pendientes,
        })
    return render(request, "home.html", {
        "miembros_stats": miembros_stats,
        "year": hoy.year,
        "semana_total_usuario": semana_total_usuario,
        "mes_total_usuario": mes_total_usuario,
        "semana_rango": semana_rango,
        "mes_nombre": mes_nombre,
    })
@login_required
def calendario(request):
    vista = request.GET.get('vista', 'semanal')
    ctx = calendario_context(request, vista)
    return render(request, "calendario.html", ctx)



from datetime import timedelta, date, datetime, time
import calendar


@login_required
def lista_tareas(request):
    # Lista de todas las tareas generales with paginación
    from django.core.paginator import Paginator
    # Ensure a consistent ordering for pagination
    tareas = Tarea.objects.all().order_by('nombre')
    paginator = Paginator(tareas, 12)
    page_number = request.GET.get('page')
    try:
        page_number_int = int(page_number)
        if page_number_int < 1:
            page_number_int = 1
    except (TypeError, ValueError):
        page_number_int = 1
    try:
        tareas_paginated = paginator.page(page_number_int)
    except Exception as e:
        # Si la página es menor que 1, ya se fuerza a 1 antes
        # Si la página es mayor que el total, mostrar la última
        if hasattr(e, 'code') or 'no contiene resultados' in str(e) or 'EmptyPage' in str(type(e)):
            tareas_paginated = paginator.page(paginator.num_pages)
        else:
            tareas_paginated = paginator.page(1)
    from django.contrib import messages
    # Ejemplo: messages.info(request, "Lista de tareas cargada correctamente.")
    return render(request, "tareas_lista.html", {"tareas_paginated": tareas_paginated})



from rest_framework import viewsets, permissions
from rest_framework.decorators import action

def es_admin(user):
    return user.is_authenticated and user.is_staff


class EsAdminPermiso(permissions.BasePermission):
    def has_permission(self, request, view):
        # Solo admin (grupo 'admin' o is_staff) puede crear, editar, borrar, aprobar
        if hasattr(view, 'action') and view.action in ["create", "update", "partial_update", "destroy", "aprobar"]:
            return request.user and (request.user.is_staff or request.user.groups.filter(name='admin').exists())
        return True


from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Miembro, Tarea, Categoria, Evento
from django.db import models
from .serializers import MiembroSerializer, TareaSerializer, CategoriaSerializer, EventoSerializer

# ViewSet para Categoría (solo admin puede modificar)
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminPermiso]

# ViewSet para Evento (admin puede crear/editar, miembros solo lectura)
class EventoViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Devuelve todos los eventos para depuración, sin filtros restrictivos
        return Evento.objects.select_related("tarea", "miembro").all()
    serializer_class = EventoSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [permissions.IsAuthenticated(), EsAdminPermiso()]
        if self.action == "partial_update":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def partial_update(self, request, *args, **kwargs):
        evento = self.get_object()
        usuario = request.user
        es_admin = usuario.is_staff
        if not es_admin:
            # Solo puede mover sus propios eventos
            if not hasattr(usuario, 'miembro') or evento.miembro_id != usuario.miembro.id:
                raise PermissionDenied("Solo puedes mover tus propios eventos")
            datos = request.data
            campos_permitidos = set(['inicio', 'fin', 'dia_vista'])
            if any(k not in campos_permitidos for k in datos.keys()):
                raise PermissionDenied("Solo puedes modificar las horas de la tarea")
            from django.utils.dateparse import parse_datetime
            nuevo_inicio = parse_datetime(datos.get('inicio')) if 'inicio' in datos else evento.inicio
            nuevo_fin = parse_datetime(datos.get('fin')) if 'fin' in datos else evento.fin
            # Permitir mover a cualquier tramo horario, pero no a otro día
            # Si el frontend envía 'dia_vista', usarlo como día destino
            dia_vista = None
            if 'dia_vista' in datos:
                try:
                    partes = [int(x) for x in datos['dia_vista'].split('-')]
                    dia_vista = date(partes[0], partes[1], partes[2])
                except Exception:
                    dia_vista = None
            if not dia_vista:
                dia_vista = evento.inicio.date()
            if nuevo_inicio.date() != dia_vista or nuevo_fin.date() != dia_vista:
                raise PermissionDenied("Solo puedes mover la tarea dentro del día seleccionado")
        # Permitir que admin actualice miembro_id y tarea_id
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            from rest_framework.response import Response
            from rest_framework import status
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def marcar(self, request, pk=None):
        try:
            evento = self.get_object()
            evento.estado = "realizada"
            evento.save(update_fields=["estado", "actualizado_en"])
            return Response({"status": "marcada"})
        except Exception as e:
            import traceback
            return Response({"error": str(e), "trace": traceback.format_exc()}, status=500)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, EsAdminPermiso])
    def aprobar(self, request, pk=None):
        evento = self.get_object()
        evento.estado = "aprobada"
        evento.save(update_fields=["estado", "actualizado_en"])
        return Response({"status": "aprobada"})
from django.db.models import Sum


def es_admin(user):
    return user.is_authenticated and user.is_staff


class EsAdminPermiso(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["create", "update", "partial_update", "destroy", "aprobar"]:
            return request.user and request.user.is_staff
        return True


class MiembroViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        instance = serializer.save()
        registrar_auditoria(self.request.user, 'crear', instance, 'Miembro')
    def perform_update(self, serializer):
        instance = serializer.save()
        registrar_auditoria(self.request.user, 'editar', instance, 'Miembro')
    def perform_destroy(self, instance):
        registrar_auditoria(self.request.user, 'eliminar', instance, 'Miembro')
        instance.delete()
    queryset = Miembro.objects.filter(usuario__isnull=False, usuario__is_staff=False)
    serializer_class = MiembroSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminPermiso]


class TareaViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        instance = serializer.save(creado_por=self.request.user)
        registrar_auditoria(self.request.user, 'crear', instance, 'Tarea')
        self.generar_eventos_recurrentes(instance, self.request.data)
    queryset = Tarea.objects.select_related("categoria").all()
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminPermiso]

    def perform_create(self, serializer):
        instance = serializer.save(creado_por=self.request.user)
        registrar_auditoria(self.request.user, 'crear', instance, 'Tarea')
        self.generar_eventos_recurrentes(instance, self.request.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        self.generar_eventos_recurrentes(instance, self.request.data)

    def generar_eventos_recurrentes(self, tarea, data):
        # Solo si la tarea tiene recurrencia activa
        from datetime import timedelta, datetime, date, time
        from django.utils import timezone
        from .models import Evento, Miembro
        tipo = tarea.recurrencia_tipo
        if tipo == 'none':
            return
        meses = int(data.get('recurrencia_meses', 3))
        fecha_inicio = tarea.recurrencia_fecha_inicio or timezone.localdate()
        fecha_fin = tarea.recurrencia_fecha_fin
        if not fecha_fin:
            # Calcular fecha fin según meses
            y, m = fecha_inicio.year, fecha_inicio.month
            m += meses
            y += (m - 1) // 12
            m = ((m - 1) % 12) + 1
            try:
                fecha_fin = date(y, m, fecha_inicio.day)
            except:
                # Si el día no existe (ej: 31 de febrero), usar último día del mes
                import calendar
                last_day = calendar.monthrange(y, m)[1]
                fecha_fin = date(y, m, last_day)
        # Eliminar eventos futuros de esta tarea antes de regenerar
        Evento.objects.filter(tarea=tarea, inicio__gte=timezone.now()).delete()
        miembros = Miembro.objects.filter(usuario__isnull=False, usuario__is_staff=False)
        # Por ahora asignar a todos los miembros (puedes ajustar lógica)
        # Generar eventos según tipo de recurrencia
        actual = fecha_inicio
        while actual <= fecha_fin:
            if tipo == 'diaria':
                dias = [int(d) for d in (tarea.recurrencia_dias or '').split(',') if d != '']
                if actual.weekday() in dias:
                    for m in miembros:
                        self.crear_evento(tarea, m, actual)
            elif tipo == 'semanal':
                dias = [int(d) for d in (tarea.recurrencia_dias or '').split(',') if d != '']
                if actual.weekday() in dias:
                    for m in miembros:
                        self.crear_evento(tarea, m, actual)
            elif tipo == 'mensual':
                if tarea.recurrencia_dia_mes and actual.day == tarea.recurrencia_dia_mes:
                    for m in miembros:
                        self.crear_evento(tarea, m, actual)
            elif tipo == 'anual':
                if tarea.recurrencia_dia_mes and tarea.recurrencia_mes:
                    if actual.day == tarea.recurrencia_dia_mes and actual.month == tarea.recurrencia_mes:
                        for m in miembros:
                            self.crear_evento(tarea, m, actual)
            actual += timedelta(days=1)

    def crear_evento(self, tarea, miembro, fecha):
        from datetime import datetime, time
        from django.utils import timezone
        # Por defecto, evento de 1h a las 9:00
        inicio = timezone.make_aware(datetime.combine(fecha, time(9, 0)))
        fin = inicio + timedelta(minutes=tarea.tiempo_estimado or 60)
        from .models import Evento
        Evento.objects.create(tarea=tarea, miembro=miembro, inicio=inicio, fin=fin, estado='pendiente', creado_por=tarea.creado_por)

    def partial_update(self, request, *args, **kwargs):
        tarea = self.get_object()
        usuario = request.user
        es_admin = usuario.is_staff
        if not es_admin:
            # Solo puede editar sus propias tareas (vinculadas a su miembro)
            if not hasattr(usuario, 'miembro') or tarea.miembro_id != usuario.miembro.id:
                raise PermissionDenied("Solo puedes editar tus propias tareas")
            datos = request.data
            campos_permitidos = set(['inicio', 'fin', 'dia_vista'])
            if any(k not in campos_permitidos for k in datos.keys()):
                raise PermissionDenied("Solo puedes modificar las horas de la tarea")
            from django.utils.dateparse import parse_datetime
            nuevo_inicio = parse_datetime(datos.get('inicio')) if 'inicio' in datos else tarea.inicio
            nuevo_fin = parse_datetime(datos.get('fin')) if 'fin' in datos else tarea.fin
            # Permitir mover a cualquier tramo horario, pero no a otro día
            # Si el frontend envía 'dia_vista', usarlo como día destino
            dia_vista = None
            if 'dia_vista' in datos:
                try:
                    partes = [int(x) for x in datos['dia_vista'].split('-')]
                    dia_vista = date(partes[0], partes[1], partes[2])
                except Exception:
                    dia_vista = None
            if not dia_vista:
                dia_vista = tarea.inicio.date()
            if nuevo_inicio.date() != dia_vista or nuevo_fin.date() != dia_vista:
                raise PermissionDenied("Solo puedes mover la tarea dentro del día seleccionado")
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def marcar(self, request, pk=None):
        try:
            evento = self.get_object()
            # Miembro (usuario no admin) marca como realizada
            evento.estado = "realizada"
            evento.save(update_fields=["estado", "actualizado_en"])
            return Response({"status": "marcada"})
        except Exception as e:
            import traceback
            return Response({"error": str(e), "trace": traceback.format_exc()}, status=500)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, EsAdminPermiso])
    def aprobar(self, request, pk=None):
        tarea = self.get_object()
        tarea.estado = "aprobada"
        tarea.save(update_fields=["estado", "actualizado_en"])
        return Response({"status": "aprobada"})


    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def marcar(self, request, pk=None):
        try:
            evento = self.get_object()
            evento.estado = "realizada"
            evento.save(update_fields=["estado", "actualizado_en"])
            return Response({"status": "marcada"})
        except Exception as e:
            import traceback
            return Response({"error": str(e), "trace": traceback.format_exc()}, status=500)


def calendario_context(request, vista):
    # Variables base
    # Permitir navegar entre meses en la vista mensual
    from datetime import datetime as dt
    hoy = timezone.localdate()
    # --- Definir variables base ---
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    indices = list(range(7))
    miembros_qs = Miembro.objects.filter(usuario__isnull=False, usuario__is_staff=False)
    miembros = list(miembros_qs)
    miembros_json = [
        {"id": m.id, "nombre": m.nombre} for m in miembros
    ]
    colores = {m.id: m.color_hex for m in miembros}
    miembro_actual = None
    miembros_filtrados = [v for v in request.GET.getlist('miembros') if v]
    solo_mis_tareas = request.GET.get('solo_mis_tareas') == '1'
    if solo_mis_tareas and not request.user.is_staff and hasattr(request.user, 'miembro'):
        miembros_filtrados = [str(request.user.miembro.id)]
    miembros_seleccionados = miembros_filtrados if miembros_filtrados else []

    # --- Fechas y rangos ---
    from datetime import datetime as dt
    hoy = timezone.localdate()
    if vista == "mensual":
        mes = request.GET.get('mes')
        anio = request.GET.get('anio')
        try:
            if mes and anio:
                hoy = hoy.replace(year=int(anio), month=int(mes), day=1)
        except Exception:
            pass
    lunes = hoy - timedelta(days=hoy.weekday())
    domingo = lunes + timedelta(days=6)
    if vista == "diaria":
        fecha_str = request.GET.get('fecha')
        if fecha_str:
            try:
                dia_actual = dt.strptime(fecha_str, "%Y-%m-%d").date()
            except Exception:
                dia_actual = hoy
        else:
            dia_actual = hoy
        inicio_rango = dia_actual
        fin_rango = dia_actual
        if not request.user.is_staff and hasattr(request.user, 'miembro'):
            miembro_actual = request.user.miembro
            miembros = [m for m in miembros if m.id != miembro_actual.id]
            miembros = [miembro_actual] + miembros
    elif vista == "mensual":
        inicio_rango = hoy.replace(day=1)
        _, last_day = calendar.monthrange(hoy.year, hoy.month)
        fin_rango = hoy.replace(day=last_day)
        dia_actual = None
    else:
        inicio_rango = lunes
        fin_rango = domingo
        dia_actual = None

    # --- Eventos ---
    start_dt = timezone.make_aware(datetime.combine(inicio_rango, time.min))
    end_dt = timezone.make_aware(datetime.combine(fin_rango, time.max))
    eventos_qs = Evento.objects.filter(inicio__gte=start_dt, inicio__lte=end_dt)
    if miembros_filtrados:
        eventos_qs = eventos_qs.filter(miembro_id__in=miembros_filtrados)
    eventos = eventos_qs.select_related("miembro", "tarea")
    eventos_data = [
        {
            "id": e.id,
            "tarea": e.tarea.nombre,
            "tarea_id": e.tarea.id,
            "icono": e.tarea.icono,
            "color": e.miembro.color_hex,
            "miembro": e.miembro.nombre,
            "miembro_id": e.miembro.id,
            "miembro_icono": e.miembro.icono if hasattr(e.miembro, 'icono') else '',
            "miembro_nombre": e.miembro.nombre if hasattr(e.miembro, 'nombre') else '',
            "inicio": e.inicio,
            "fin": e.fin,
            "estado": e.estado,
            "puntuacion": getattr(e.tarea, 'puntuacion', 1),
        }
        for e in eventos
    ]

    meses_es = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    mes_nombre = meses_es[hoy.month - 1]
    year = hoy.year
    horas = [f"{h:02d}:00" for h in range(7, 23)]
    week_cols = []
    for i in range(7):
        dia = dias[i]
        fecha = lunes + timedelta(days=i)
        week_cols.append({
            "dia": dia,
            "label": fecha.strftime('%d/%m'),
            "iso": fecha.isoformat(),
        })

    # --- week_dates y weeks_dates ---
    week_dates = []
    weeks_dates = []
    if vista == "semanal":
        week_dates = [ (lunes + timedelta(days=i)).isoformat()[:10] for i in range(7) ]
    if vista == "mensual":
        cal = calendar.Calendar(firstweekday=0)
        calendar.setfirstweekday(calendar.MONDAY)
        weeks = calendar.monthcalendar(hoy.year, hoy.month)
        for week in weeks:
            week_dates_row = []
            for d in week:
                if d == 0:
                    week_dates_row.append(None)
                else:
                    week_dates_row.append(date(hoy.year, hoy.month, d))
            weeks_dates.append(week_dates_row)

    # --- Retorno único ---
    return {
        "dias": dias,
        "indices": indices,
        "miembros": miembros,
        "miembros_json": miembros_json,
        "colores": colores,
        "eventos_data": eventos_data,
        "hoy_iso": hoy.isoformat(),
        "is_admin": request.user.is_staff,
        "miembro_actual": miembro_actual if vista == "diaria" and not request.user.is_staff and hasattr(request.user, 'miembro') else None,
        "dia_actual": dia_actual if vista == "diaria" else None,
        "mes_nombre": mes_nombre,
        "year": year,
        "lunes": lunes,
        "domingo": domingo,
        "miembros_seleccionados": miembros_seleccionados,
        "vista": vista,
        "colores": colores,
        "miembros_json": miembros_json,
        "solo_mis_tareas": solo_mis_tareas,
        "horas": horas,
        "week_cols": week_cols,
        "week_dates": week_dates,
        "weeks_dates": weeks_dates,
    }



@user_passes_test(es_admin)
@login_required
@user_passes_test(es_admin)
def admin_tareas(request):
    from django.core.paginator import Paginator
    miembros = Miembro.objects.filter(usuario__isnull=False, usuario__is_staff=False)
    categorias = Categoria.objects.all()
    tareas = Tarea.objects.all().select_related('categoria')
    categoria_f = request.GET.get('categoria')
    tag_f = request.GET.get('tag')
    texto_f = request.GET.get('texto')
    if categoria_f:
        tareas = tareas.filter(categoria_id=categoria_f)
    if tag_f:
        tareas = tareas.filter(tag__icontains=tag_f)
    if texto_f:
        tareas = tareas.filter(
            models.Q(nombre__icontains=texto_f) |
            models.Q(descripcion__icontains=texto_f)
        )
    total_tareas = tareas.count()
    paginator = Paginator(tareas, 12)
    page_number = request.GET.get('page')
    tareas_paginated = paginator.get_page(page_number)
    hoy = timezone.localdate()
    meses_es = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    mes_nombre = meses_es[hoy.month - 1]
    mes_numero = hoy.month
    year = hoy.year
    return render(request, "admin_tareas.html", {
        "miembros": miembros,
        "categorias": categorias,
        "tareas_paginated": tareas_paginated,
        "total_tareas": total_tareas,
        "mes_nombre": mes_nombre,
        "mes_numero": mes_numero,
        "year": year
    })
from django.shortcuts import render

def politica_privacidad(request):
    return render(request, "privacidad.html")


@login_required
def request_data_export(request):
    """Permite a un usuario autenticado solicitar la exportación de sus datos personales.

    Para la demo, devolvemos JSON con los datos principales y registramos la acción en AuditLog.
    En producción, esto debería generar un paquete preparado para entrega (ZIP con datos) y
    control de acceso adicional.
    """
    from .models import AuditLog, Miembro
    user = request.user
    miembro = None
    try:
        miembro = user.miembro
    except Exception:
        miembro = None

    data = {
        'username': user.username,
        'email': getattr(user, 'email', ''),
        'miembro': {'id': miembro.id, 'nombre': miembro.nombre} if miembro else None,
    }
    # Registrar auditoría
    try:
        AuditLog.objects.create(action='export', user=user, details=data)
    except Exception:
        pass
    from django.http import JsonResponse
    return JsonResponse({'ok': True, 'data': data})


@login_required
def request_account_deletion(request):
    """Solicita la eliminación de la cuenta del usuario (proceso manual/automatizable).

    Mecanismo: marca una entrada de AuditLog con action='deletion_requested'.
    El borrado efectivo puede requerir verificación por el responsable (para cumplir
    adecuadamente RGPD/LOPDGDD y preservar evidencias legales durante el periodo
    requerido).
    """
    from .models import AuditLog
    user = request.user
    reason = request.POST.get('reason', '') if request.method == 'POST' else ''
    try:
        AuditLog.objects.create(action='deletion_requested', user=user, details={'reason': reason})
    except Exception:
        pass
    from django.shortcuts import redirect
    from django.contrib import messages
    messages.info(request, 'Solicitud de eliminación registrada. Un administrador la procesará.')
    return redirect('home')


