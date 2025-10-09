Registro simplificado de actividades de tratamiento — Familia Calendario (demo)

Fecha: 2025-10-09

1. Responsable
- Proyecto: Familia Calendario (demo)
- Contacto placeholder: privacy@example.org

2. Actividades de tratamiento (resumen)
- Autenticación de usuarios: datos tratados: username, password(hasheada). Finalidad: permitir acceso.
- Gestión de tareas y eventos: datos tratados: nombre de la tarea, descripción, horario, miembro asociado (nombre). Finalidad: prestación del servicio.
- Auditoría de solicitudes de privacidad: datos tratados: identificador de usuario (id interno), acción solicitada, timestamps. Finalidad: trazabilidad y cumplimiento legal.

3. Categorías de interesados
- Usuarios registrados en la demo.

4. Conservación
- Datos de cuenta y tareas: mientras exista la cuenta o hasta eliminación por solicitud.
- Registros de auditoría y solicitudes de privacidad: 5 años por defecto.

5. Destinatarios / encargados
- Proveedor de hosting (Render u otro): debe existir DPA antes de producción.

6. Medidas técnicas y organizativas
- HTTPS/TLS en despliegue.
- Cookies seguras y CSRF protector.
- No incluir secretos en el repositorio.

7. Procedimiento para solicitudes
- Usuario autenticado puede solicitar exportación o eliminación a través de los endpoints disponibles.
- La solicitud queda registrada en `tareas.AuditLog` con action `deletion_requested` o `export`.
- Un administrador revisa la solicitud y la procesa manualmente dentro de 1 mes. La acción de procesamiento (exportación / anonimización) debe registrarse en `AuditLog` con action `deletion_executed` o `export`.

Notas: este registro es simplificado y se recomienda revisar con asesoría legal antes de producción.

Comando administrativo para anonimización
- Existe el comando `manage.py anonymize_requests` que permite al admin procesar las solicitudes registradas en `AuditLog`.
- Ejemplos:
	- Simular para ids: `python manage.py anonymize_requests --ids 12 --dry-run`
	- Procesar y anonimizar: `python manage.py anonymize_requests --ids 12 13 --yes --output-json report.json`
	- Procesar todas las solicitudes: `python manage.py anonymize_requests --all-completed --yes`

El comando crea `AuditLog(action='deletion_executed')` para cada solicitud procesada y en caso de fallo `AuditLog(action='deletion_failed')`.
