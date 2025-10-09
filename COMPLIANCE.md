RGPD / LOPDGDD / ISO 27701 — Checklist mínimo para la demo

Este documento resume medidas y recomendaciones para que este proyecto cumpla con requisitos básicos de protección de datos personales y un marco de privacidad conforme a ISO 27701.

1) Gobernanza y responsabilidades (ISO 27701)
- Designar un responsable del tratamiento (persona física o rol). Añadir contacto en `templates/privacy.html`.
- Mantener registros de tratamiento (qué datos se recogen, finalidad, base legal, tiempo de conservación).

2) Base legal y derechos (RGPD / LOPDGDD)
- Mostrar aviso de privacidad claro (ya existe `templates/privacy.html`).
- Permitir ejercicio de derechos (proveer correo admin@example.com por defecto; en producción usar canal autenticado y verificado).

3) Minimización y consentimiento
- Solo recoger datos estrictamente necesarios. Para la demo, se recogen: username, password, eventos/tareas.
- Cookies: mostrar banner y guardar consentimiento (se añade `templates/cookie_banner.html`).

4) Seguridad técnica y organizativa
- Forzar HTTPS en producción (`SECURE_SSL_REDIRECT=True`).
- Cookies seguras: `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`.
- HSTS: configurar `SECURE_HSTS_SECONDS` > 0 en producción.
- Logs: limitar retención y no guardar contraseñas en texto plano.
- Control de accesos: no crear administradores de forma automática con contraseñas públicas.

5) Gestión de proveedores y transferencias
- Si se usan servicios en la nube (Render, bases de datos), documentar proveedores y acuerdos de tratamiento (DPA) si se procesan datos personales.

6) Auditoría y evidencias
- Mantener cambios de configuración en repositorio (sin secretos), y registrar quién publica cambios en producción.
- Ejecutar `python manage.py check --deploy` y aplicar recomendaciones.

7) Política de retención y eliminación
- Documentar tiempos de retención de datos y procedimientos de borrado.

8) Certificaciones y alcance de ISO 27701
- ISO 27701 requiere controles organizativos (PIMS) además de técnicos; para una demo se pueden documentar prácticas y mostrar evidencias básicas (privacidad policy, registros de tratamiento, DPA).

Recomendaciones prácticas inmediatas
- No subir `db.sqlite3` que contenga datos reales; limpiar antes de publicar.
- Usar variables de entorno en Render para SECRET_KEY, DEBUG y DATABASE_URL; no almacenar secretos en el repo.
- Añadir un endpoint/administración para que un usuario autenticado pueda solicitar la eliminación de su cuenta (respuesta automatizada o aviso al responsable).

Actualización (2025-10-09): acciones aplicadas en este repositorio
- `templates/privacy.html` actualizado con texto claro y contacto por defecto `privacy@example.org` (reemplazar en producción).
- `templates/cookie_banner.html` incluido y configurado para que las cookies analíticas solo se carguen con consentimiento.
- `tareas.models.AuditLog` existe y se usa para registrar solicitudes de exportación y eliminación.
- Añadido `DATA_PROCESSING.md` con un registro simplificado de actividades de tratamiento.
- Añadido comando de administración `manage.py process_requests` para listar y procesar solicitudes pendientes (no ejecuta borrados automáticos por defecto).

Acciones recomendadas pendientes (prioridad alta antes de producción)
- Revisar y firmar un DPA con el proveedor de hosting (Render u otro) antes de publicar datos reales.
- Eliminar o sanear cualquier backup o `db.sqlite3` que contenga datos reales en los archivos de distribución/zip.
- Definir política concreta de retención (los tiempos en este documento son sugeridos y deben revisarse legalmente).
- Si se habilita la función de enviar correos automáticos de verificación, implementar verificación por correo y medidas anti-abuso.


Notas para despliegue en Render (capa gratuita)
- La capa gratuita de Render proporciona entornos para demos pero puede implicar backups automáticos y logs gestionados por el proveedor; antes de subir datos reales asegúrate de: 
	- Revisar si Render mantiene backups persistentes (en la capa gratuita pueden existir snapshots temporales). 
	- No subir `db.sqlite3` con datos reales; usar DATABASE_URL apuntando a un servicio Postgres con DPA firmado.
	- Establecer variables de entorno en el panel de Render: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, `DATABASE_URL`.
	- Configurar `ALLOWED_HOSTS` y HSTS en `hogar/settings.py` para producción.

Comando de anonimización (operación administrativa)
- Se ha añadido `manage.py anonymize_requests` para procesar solicitudes de eliminación registradas en `AuditLog`.
- Flags principales: `--ids`, `--all-completed`, `--dry-run`, `--yes`, `--delete-events`, `--output-json`, `--admin-id`.
- El comando por defecto realiza pseudonimización (anonimiza usuario y desvincula miembros) y registra `AuditLog(action='deletion_executed')`.

Contacto para privacidad en demo
- correo de contacto (placeholder): privacy@example.org

Notas legales rápidas
- Para este proyecto, dado que no se tratan DNI, apellidos ni identificadores civiles, el riesgo es bajo. No obstante, los derechos ARCO/LOS (acceso, rectificación, supresión, portabilidad, limitación, oposición) siguen aplicando y deben tramitarse y documentarse.


Si quieres, implemento:
- Un endpoint `/privacy/request-deletion/` que permita a un usuario autenticado solicitar la eliminación de sus datos (genera ticket en logs o envía correo al admin).
- Cambios en `settings.py` para habilitar CSP (Content Security Policy) básico.
- Un `security.md` con pasos de hardening y comprobaciones (será útil para entrevistas y documentación).

