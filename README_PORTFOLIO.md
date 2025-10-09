# Calendario Familiar — Preparado para Portafolio

Este documento resume el estado del proyecto, los cambios realizados para la versión demo pública y las instrucciones rápidas para presentar el proyecto en una entrevista o cartera.

## Estado actual (resumen)
- Proyecto Django funcional (Django 5.2.7) con base de datos SQLite (`db.sqlite3`).
- Virtualenv en `.venv` (Python 3.13.x).
- Se han eliminado/neutralizado cuidadosamente las funciones `reto(s)` para el demo público:
  - Plantillas relacionadas con retos movidas a `templates/reto-backup/`.
  - Cambios de código no destructivos y backups `.reto.bak` creados para archivos editados.
  - Migraciones reconciliadas con la base de datos (uso de `--fake` cuando procedía).
- Demo data creada (usuario `demo` / `demo` si `scripts/create_demo.py` está activo).

## Limpieza realizada (acción reciente)

- Fecha: 2025-10-08
- Se han identificado y archivado los artefactos de respaldo (principalmente las carpetas `backup_import_*/` y plantillas de `retos`) usando `scripts/clean_demo_artifacts.ps1`.
- Resultado: los archivos encontrados se movieron a `backup_for_portfolio/` y se creó el archivo `backup_for_portfolio.zip` en la raíz del repositorio: `C:\Users\j\familia_calendario_public\backup_for_portfolio.zip`.
- Notas: durante la operación el script produjo varias advertencias indicando que algunos archivos listados ya no existían (probablemente fueron eliminados/limpiados en pasos previos). El proceso terminó creando el ZIP correctamente.

Se han añadido además los siguientes cambios para facilitar el empaquetado final del portafolio:

- `.gitignore` (excluye `backup_import_*`, `backup_for_portfolio*`, bytecode y `.venv`).
- `scripts/package_portfolio.ps1` — script que genera un ZIP limpio del árbol actual (usa `git archive` y excluye backups detectados).


## Qué se limpió / neutralizó
- Todas las referencias en plantillas activas a la funcionalidad de `retos` se movieron a `templates/reto-backup/`.
- Se eliminaron bloques problemáticos en `tareas/models.py` que provocaban errores con la DB; se generó la migración correspondiente y se aplicó con cuidado.
- Se restauraron accidentalmente modificados en `.venv` desde backups cuando fue necesario.

## Archivos añadidos para demo/portafolio
- `scripts/start_demo.ps1` — arranca demo (migrations + demo data + server, registra PID y logs).
- `scripts/stop_demo.ps1` — para el demo (lee `.server_pid`, mata procesos o busca listeners por puerto).
- `scripts/runserver_foreground.ps1` — arranque sencillo en primer plano (activa venv + runserver).
- `scripts/start_server_only.ps1` — (útil) arranca solo el servidor en nueva ventana.
- `scripts/inspect_db_columns.py` — helper para inspeccionar tablas SQLite.
- `templates/registration/login.html` — shim para evitar TemplateDoesNotExist.
- `README_demo.md` — instrucciones rápidas de demo.
- `README_PORTFOLIO.md` — este archivo (estado e instrucciones para presentar).
- `C:\Users\j\start_familia_calendario.*` — lanzadores para arrancar el proyecto desde cualquier sitio (opcional).

## Recomendaciones antes de mostrar en público
1. Revise `db.sqlite3` para asegurarse de que no contiene datos sensibles.
2. Elimine cualquier archivo de backup que no quiera publicar (`backup_import_*` si contiene datos privados).
3. Revisa `templates/reto-backup/` y decide si moverlo fuera del repo (si prefieres no mostrar código deshabilitado).
4. Actualiza `hogar/settings.py` para configurar `ALLOWED_HOSTS` y `SECRET_KEY` diferente si vas a subir a un repositorio público.
5. Ejecuta `python manage.py check --deploy` para ver advertencias de seguridad antes de exponer el proyecto.

## Cómo presentar (guion de demostración)
- Mostrar la página principal y la UI (abre `http://127.0.0.1:8000`).
- Iniciar sesión con `demo/demo` y navegar a `/miembros/`, `/tareas/`, `/calendario/`.
- Explicar la decisión de neutralizar `retos` para la demo y mostrar `templates/reto-backup/` como evidencia de preservación no destructiva.
- Hablar brevemente sobre la estrategia de migraciones (uso de `--fake` para reconciliar con la DB existente) y por qué fue necesaria.

## Comandos útiles
- Arrancar demo (migrations + demo data + server):
```powershell
.\scripts\start_demo.ps1 -Port 8000 -Force
```
- Parar demo:
```powershell
.\scripts\stop_demo.ps1 -Port 8000 -Force
```
- Arrancar servidor (foreground):
```powershell
.\scripts\runserver_foreground.ps1
```
- Lanzador global (si lo configuraste):
```powershell
start_familia_calendario.bat
# o
powershell -NoProfile -Command "& 'C:/Users/j/start_familia_calendario.ps1'"
```

## Siguientes pasos opcionales (mejoras para portafolio)
- Añadir un `Dockerfile` + `docker-compose` minimal para que reclutadores puedan levantar el demo sin tocar Python local.
- Añadir pruebas E2E (por ejemplo con Playwright) que hagan login y verifiquen rutas clave para usar como evidencia técnica.
- Extraer el demo en un repositorio público separado que contenga solo lo necesario (migraciones, templates, scripts) y no los backups o datos privados.

---

Si quieres, puedo:
- crear un `clean_demo_artifacts` script que archive (zip/move) carpetas de backup y deje solo los ficheros necesarios para el portafolio;
- generar un `Dockerfile` y `docker-compose.yml` mínimo para el demo;
- preparar un `demo_walkthrough.md` listo para presentar en una entrevista.

Dime cuál de esos quieres que haga ahora.
