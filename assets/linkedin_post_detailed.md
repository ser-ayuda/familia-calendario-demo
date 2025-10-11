## LinkedIn — Post detallado y ficha técnica para "Familia Calendario" (español)

Versión larga (para publicar en LinkedIn o artículo corto):

He lanzado una demo pública de "Familia Calendario": una pequeña app Django para planificar tareas y eventos compartidos en el hogar. La demo está desplegada en Render (PAAS) y el código fuente es open-source en GitHub: https://github.com/ser-ayuda/familia-calendario-demo

Qué puedes probar
- Acceso a la interfaz de gestión: https://familia-calendario-demo.onrender.com/gestion/  (usuario demo/demo)
- Descargar el paquete de portafolio: Release -> `portfolio_minimal.zip` (fixtures anonimizados y capturas). No incluye datos personales.

Ficha técnica
- Stack: Python 3.13, Django 5.2.7, Django REST Framework
- Frontend: HTML templating Django + vanilla JS (con capturas automatizadas con Playwright)
- Persistencia: SQLite (desarrollo) / Postgres (producción)
- Testing: pytest/Django test suite + acciones automatizadas para capturas
- Dependencias: gunicorn, whitenoise, dj-database-url, psycopg2-binary, djangorestframework

Despliegue en Render (pasos generales)
1. Crear un servicio tipo "Web Service" en Render y conectar el repo GitHub.
2. Configurar variables de entorno en el panel de Render:
   - DJANGO_SECRET_KEY: una clave larga y segura
   - DJANGO_DEBUG=false
   - DATABASE_URL: postgres://user:pass@host:5432/dbname (si usas Postgres)
3. Usar el `Dockerfile` o el build automático de Render. Si usas Docker, Render construirá la imagen con el `Dockerfile` incluido.
4. Ejecutar migraciones en la command-run (o usar entrypoint que haga `python manage.py migrate`).
5. (Opcional) Configurar el dominio personalizado, HTTPS y políticas HSTS.

Checklist para ponerlo en la nube (resumen de seguridad y buenas prácticas)
- Nunca subir `DJANGO_SECRET_KEY` ni `DATABASE_URL` al repositorio.
- Asegurar `DEBUG=false` en producción.
- Habilitar `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE` y `CSRF_COOKIE_SECURE`.
- Usar un servicio Postgres gestionado para producción (con backups y DPA si tratas datos de terceros).
- Revisar y sanear cualquier backup que contenga datos reales antes de compartir el repo o ZIP.

Entorno de desarrollo (para contribuir o probar localmente)
1. Clona el repo y crea la virtualenv:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
2. Aplicar migraciones y cargar fixtures anonimizados:
```powershell
python manage.py migrate
python manage.py loaddata fixtures/contenttypes.json fixtures/auth.json fixtures/tareas.json
```
3. Iniciar el servidor:
```powershell
python manage.py runserver
```

Puntos destacables a añadir al post de LinkedIn (para buena impresión)
- Resaltar la arquitectura: stack ligero, contenedores y despliegue en PAAS (Render).
- Mencionar pruebas y automatización: tests unitarios y script de screenshots con Playwright para generar assets visuales.
- Cumplimiento/Privacidad: fixtures anonimizados y checklist COMPLIANCE.md para mostrar responsabilidad en manejo de datos.
- Mostrar enlaces: demo en Render + repo GitHub + Release con ZIP preparado.

Call to action (CTA)
- "Si quieres que te enseñe este proyecto en 15 minutos, escríbeme y lo desplegamos juntos." 

Hashtags sugeridos
#Django #Python #WebDev #DevOps #Render #Portfolio #OpenSource

Versión corta (para tweet/preview en LinkedIn):

Familia Calendario — demo pública desplegada en Render. Código y guía de despliegue en GitHub. Prueba: https://familia-calendario-demo.onrender.com/gestion/ (demo/demo)
