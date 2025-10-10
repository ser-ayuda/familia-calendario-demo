# Familia Calendario — Demo pública

Una pequeña aplicación web para coordinar tareas y eventos del hogar. Esta carpeta contiene la versión pública y sanitizada pensada para mostrar en un portafolio.

Live demo
 - https://familia-calendario-demo.onrender.com/gestion/ (credenciales demo: `demo` / `demo`)

TL;DR
- Stack: Python, Django 5.2.x, SQLite (dev) / Postgres (prod), Render deployment
- Características: gestión de miembros, tareas recurrentes, calendario de eventos, API REST y utilidades para exportar/anacular datos (RGPD-aware)

Quick start (local)

1. Crea y activa el entorno virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Instala dependencias e inicializa la base de datos:

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data   # crea datos demo
python manage.py runserver
```

3. Abre `http://127.0.0.1:8000/` y entra con `demo` / `demo`.

Privacidad y cumplimiento

Esta rama está preparada para portafolio: backups, logs y datos sensibles han sido movidos a `removed_for_portfolio/` y `db.sqlite3` no está trackeado en Git. Consulta `COMPLIANCE.md` para detalles sobre las tareas de saneamiento realizadas.

Contribuciones y licencia

Si quieres reutilizar o mejorar el proyecto, revisa la `LICENSE` (MIT) incluida en el repositorio.

Más documentación

Consulta `README_demo.md` para instrucciones detalladas de arranque (scripts PowerShell incluidos), `README_PORTFOLIO.md` para la narrativa del portafolio y `COMPLIANCE.md` para la checklist de privacidad.
