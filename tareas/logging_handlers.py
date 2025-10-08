
import logging

class AvisoAdminHandler(logging.Handler):
    def emit(self, record):
        try:
            from tareas.models import Aviso
            from django.utils.timezone import now
            mensaje = self.format(record)
            nivel = record.levelname.upper()
            if nivel not in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
                nivel = "INFO"
            Aviso.objects.create(
                mensaje=mensaje,
                nivel=nivel,
                creado_en=now()
            )
        except Exception:
            pass  # Nunca fallar el logging por errores en avisos
