
from django.db import models

# Modelo para avisos administrativos
class Aviso(models.Model):
    NIVEL_CHOICES = [
        ("INFO", "Info"),
        ("WARNING", "Advertencia"),
        ("ERROR", "Error"),
        ("CRITICAL", "Crítico"),
    ]
    mensaje = models.TextField()
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES, default="INFO")
    creado_en = models.DateTimeField(auto_now_add=True)
    visto = models.BooleanField(default=False)
    usuario = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='avisos')

    def __str__(self):
        return f"[{self.nivel}] {self.mensaje[:40]}{'...' if len(self.mensaje)>40 else ''}"



class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Miembro(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    color_hex = models.CharField(max_length=7, default="#888888")
    icono = models.CharField(max_length=20, default="", blank=True)
    usuario = models.OneToOneField('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='miembro')
# RETO_REMOVED:     saldo = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text="Saldo acumulado en euros por retos")
# RETO_REMOVED:     puntos = models.PositiveIntegerField(default=0, help_text="Puntos acumulados por retos")

    def __str__(self) -> str:
        return self.nombre


class Tarea(models.Model):
    RECURRENCIA_CHOICES = [
        ('none', 'Sin repetición'),
        ('diaria', 'Diaria'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ]
    recurrencia_tipo = models.CharField(max_length=10, choices=RECURRENCIA_CHOICES, default='none')
    # Días de la semana para diaria/semanal (0=Lunes, 6=Domingo)
    recurrencia_dias = models.CharField(max_length=20, blank=True, help_text="Días de la semana separados por coma (ej: 0,2,4)")
    # Día del mes para mensual/anual
    recurrencia_dia_mes = models.PositiveIntegerField(null=True, blank=True, help_text="Día del mes (1-31)")
    # Mes para anual
    recurrencia_mes = models.PositiveIntegerField(null=True, blank=True, help_text="Mes (1-12, solo anual)")
    # Rango de fechas para la recurrencia
    recurrencia_fecha_inicio = models.DateField(null=True, blank=True, help_text="Fecha de inicio de la recurrencia")
    recurrencia_fecha_fin = models.DateField(null=True, blank=True, help_text="Fecha de fin de la recurrencia")
    premio = models.DecimalField(max_digits=6, decimal_places=2, default=0.10, help_text="Premio en euros (ejemplo: 0.20)")
    tiempo_estimado = models.PositiveIntegerField(default=30, help_text="Tiempo estimado en minutos")
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('realizada', 'Realizada por miembro'),
        ('aprobada', 'Aprobada por administrador'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=20, default="", blank=True)
    categoria = models.ForeignKey('Categoria', null=True, blank=True, on_delete=models.SET_NULL, related_name='tareas')
    tag = models.CharField(max_length=50, blank=True)
    puntuacion = models.PositiveIntegerField(default=1)

    creado_por = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='tareas_creadas')

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='eventos')
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='eventos')
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=Tarea.ESTADO_CHOICES, default='pendiente')
    creado_por = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='eventos_creados')
    actualizado_en = models.DateTimeField(auto_now=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['inicio']

    def __str__(self):
        return f"{self.tarea.nombre} - {self.miembro.nombre} ({self.inicio:%Y-%m-%d %H:%M})"

    @property
    def duracion_minutos(self) -> int:
        return int((self.fin - self.inicio).total_seconds() // 60)


class AuditLog(models.Model):
    """Registro de auditoría simple para acciones relacionadas con identidades y datos personales.

    Esto ayuda a cumplir con requisitos de trazabilidad (quién ha solicitado/ejecutado
    la eliminación de datos, exportaciones, cambios de permisos, etc.).
    """
    ACTION_CHOICES = [
        ('export', 'Export Data'),
        ('deletion_requested', 'Deletion Requested'),
        ('deletion_executed', 'Deletion Executed'),
        ('user_created', 'User Created'),
        ('permission_change', 'Permission Change'),
    ]
    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_logs')
    target_type = models.CharField(max_length=64, blank=True)
    target_id = models.CharField(max_length=64, blank=True)
    details = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_action_display()} - {self.user} - {self.created_at:%Y-%m-%d %H:%M}"

