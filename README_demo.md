# Demo: arranque rápido

Este repositorio incluye scripts auxiliares para arrancar y parar rápidamente una copia demo del proyecto.

## Documentación ampliada — guía paso a paso

Esta sección recoge instrucciones detalladas para reproducir la demo localmente, alternativas con fixtures, verificación rápida y una checklist para preparar el repositorio antes de publicarlo en un perfil (LinkedIn/GitHub). Es intencionalmente exhaustiva para que puedas compartir el enlace con confianza.

### Requisitos mínimos
- Windows PowerShell (pwsh)
- Python 3.11+ (probado con 3.13)
- Git (para clonar el repo o actualizar)

### Opción A — arranque rápido (scripts PowerShell)

1. Desde la raíz del repositorio ejecuta:

```powershell
.\scripts\start_demo.ps1 -Port 8000 -Force
```

2. El script hace lo siguiente (resumen): crea `.venv` si hace falta, instala dependencias, aplica migraciones y ejecuta `scripts/create_demo.py` (idempotente). Abre una nueva ventana con el servidor y guarda el PID en `.server_pid`.

3. Para detener:

```powershell
.\scripts\stop_demo.ps1 -Port 8000 -Force
```

### Opción B — reproducir demo a partir de fixtures (sin `db.sqlite3`)

1. Crear y activar virtualenv (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Instalar dependencias y aplicar migraciones:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
```

3. Cargar fixtures en el orden correcto:

```powershell
.venv\Scripts\python.exe manage.py loaddata fixtures/contenttypes.json fixtures/auth.json fixtures/tareas.json
```

4. Ejecutar servidor:

```powershell
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

5. Accede con las credenciales demo:

- Usuario: `demo`
- Contraseña: `demo`

Nota: `fixtures/auth.json` ha sido sanitizado — la mayoría de cuentas tienen contraseña reemplazada por `"!"` para evitar exponer hashes; la cuenta `demo` mantiene una contraseña válida (`demo`) para facilitar pruebas.

### Verificaciones y pruebas locales
- Ver PID guardado: `Get-Content .server_pid`
- Comprobar que el servidor responde: `Invoke-WebRequest http://127.0.0.1:8000 -UseBasicParsing`
- Probar rutas clave: `/tareas/`, `/calendario/`, `/demo/`, `/gestion/`.
- Iniciar sesión con `demo/demo` y abrir `/gestion/` para comprobar las vistas de administración.

### Troubleshooting rápido
- Si `loaddata` falla por codificación en Windows, asegúrate de ejecutar con `.venv\Scripts\python.exe` y que los ficheros JSON estén en UTF-8. Los fixtures incluidos ya lo están.
- Si `start_demo.ps1` no abre el servidor por conflicto de puerto, usa `-Force` para terminar el proceso que esté ocupando el puerto.
- Si ves errores 500, revisa `server_err.log` y el output en la ventana donde `start_demo.ps1` lanzó el servidor.

### Checklist antes de publicar a LinkedIn / portafolio
Marca cada punto si ya está completado:

- [x] `LICENSE` (MIT) incluido.
- [x] `COMPLIANCE.md` con la checklist de saneamiento.
- [x] Backups y logs removidos a `removed_for_portfolio/`.
- [x] `fixtures/` sanitizados (`auth.json` neutraliza contraseñas salvo `demo`).
- [x] `README_demo.md` y `README.md` explicativos y con instrucciones reproducibles.
- [x] `assets/social.png` y `assets/linkedin_post.md` para la publicación.
- [ ] (opcional) Reemplazar nombres de ejemplo en `fixtures/tareas.json` por identificadores anónimos (`member_1`, `member_2`) si prefieres no mostrar términos como `mamá`/`papá` en el repo.

Si quieres que haga la anonimización automática de `fixtures/tareas.json` (re-mapeo de usuarios y FK references preservadas), dímelo y lo hago; lo dejo desactivado por defecto porque los nombres actuales son claramente marcados como ejemplos en los READMEs.

### Publicación en LinkedIn — guía breve
- Usa `assets/social.png` (1200x627) y el texto en `assets/linkedin_post.md`.
- Antes de publicar: revisa que el repo público en GitHub apunte a la rama `main` que contiene los fixtures y la `README_demo.md` mejorada.
- En la publicación enlaza a la demo en Render (si estás publicando la demo en un host público) o al repo en GitHub si solo compartes el código.

Sugerencia: publica la entrada con una breve explicación técnica (stack, retos resueltos) y añade 2 capturas (home, calendario). Si quieres, puedo generar las capturas automáticamente y añadirlas a `demo_screenshots/`.

---

Si quieres que continúe y haga cualquiera de las tareas siguientes ahora, marca una opción:

1. Anonimizar nombres en `fixtures/tareas.json` (re-mapeo automático y actualización del fixture).
2. Generar capturas `demo_screenshots/` (login, calendario, tareas) y añadirlas al repo.
3. Preparar `portfolio_minimal.zip` sin `db.sqlite3` (solo migraciones + scripts/create_demo.py).

Dime cuál prefieres y lo hago.

### Artifact: portfolio_minimal.zip

He generado un artefacto local `portfolio_minimal.zip` (excluye `.venv`, `db.sqlite3`, y `removed_for_portfolio/`) que ahora incluye las capturas generadas en `demo_screenshots/` y los fixtures anonimizados. El archivo está en la raíz del repo pero está listado en `.gitignore` para evitar subir binarios accidentalmente al historial.

Cómo publicar el ZIP en GitHub (pasos manuales):

1. Ve a la página del repositorio en GitHub → "Releases" → "Draft a new release".
2. Subir `portfolio_minimal.zip` como asset del release.
3. Completa el título y descripción (usa `assets/linkedin_post.md` para la descripción sugerida) y publica el release.

Si quieres que cree el draft release y suba el ZIP por ti, puedo hacerlo pero necesitaré autorización (o lo subo usando la API con credenciales si me las facilitas). Si prefieres, lo dejo listo localmente y lo subes manualmente.


Requisitos
- Windows PowerShell (pwsh)
- Python + venv (el script crea `.venv` si falta)

Comandos principales

- Arrancar el servidor de desarrollo (mata procesos que ocupen el puerto si se usa `-Force`):

```powershell
.\scripts\start_demo.ps1 -Port 8000 -Force
```

- Parar el servidor (lee `.server_pid` o, con `-Force`, mata procesos que estén escuchando en el puerto):

```powershell
.\scripts\stop_demo.ps1 -Port 8000 -Force
```

¿Qué hace `start_demo.ps1`?
- Asegura que exista `.venv` y usa ` .venv\Scripts\python.exe`.
- Actualiza pip e instala `requirements.txt` si está presente.
- Ejecuta `migrate --noinput`.
- Ejecuta `scripts/create_demo.py` si existe para poblar datos de demo.
- Inicia `manage.py runserver 127.0.0.1:<Port>` usando el Python del venv, redirigiendo stdout/stderr a `server_stdout.log` / `server_err.log`.
- Escribe el PID del proceso en `.server_pid`.

Archivos relevantes
- `.server_pid` — PID del proceso Python que corre el servidor (si arrancó desde `start_demo.ps1`).
- `server_stdout.log`, `server_err.log` — logs del servidor.
- `templates/registration/login.html` — shim que reutiliza `templates/login.html` para la vista de login.

Credenciales demo
- Usuario: `demo` / `demo` (usuario de pruebas para la demo)

Notas y troubleshooting
- Si el script detecta que el puerto ya está en uso, por defecto no mata procesos para evitar pérdida de datos; usa `-Force` para forzar cierre.
- Revisa `server_err.log` si ves errores 500 en el sitio.
- Si quieres usar la plantilla `registration/login.html` exacta del proyecto original, cópiala a `templates/registration/login.html` (actualmente hay un shim que incluye `templates/login.html`).

Contacto
- Si quieres que adapte los scripts (p. ej. `-NoBrowser`, arranque en 127.0.0.1 sólo, o logging adicional), dime qué prefieres y lo implemento.

Portafolio / preparación para mostrar
- Si vas a presentar este proyecto en un portafolio, hay un documento principal con recomendaciones y el estado final en `README_PORTFOLIO.md`.
# README - Demo (Familia Calendario)

## Objetivo

Este README explica cómo ejecutar la versión de demo/portafolio del proyecto "familia_calendario_public".
Es una copia ligera del proyecto original (basado en `C:\Users\j\familia_calendario`) preparada para mostrar en CV o entrevistas.

## Resumen de la demo

- Aplicación Django con vistas públicas (inicio, tareas, calendario, miembros, demo).
- Plantillas mínimas añadidas para que la demo funcione sin errores (por ejemplo `base.html`, `tareas_lista.html`, `calendario.html`, `admin_miembros.html`).
- `scripts/start_demo.ps1` — prepara venv, aplica migraciones, crea datos demo y abre el servidor en una nueva ventana; guarda PID en `.server_pid`.
- `scripts/stop_demo.ps1` — detiene el proceso registrado en `.server_pid`.
-- `scripts/create_demo.py` — crea datos demo y un usuario de pruebas `demo`.

## Requisitos (local)

- Windows PowerShell (pwsh.exe recomendado)
- Python 3.11+ (probado con 3.13)
- Git (opcional)

## Archivos importantes

- `manage.py` — entrada Django (ya configurada).
- `hogar/settings.py` — settings del proyecto (DEBUG=True por defecto en demo).
- `templates/` — plantillas usadas por la demo (se añadieron las mínimas necesarias).
- `scripts/start_demo.ps1` — preparar y arrancar demo en otra ventana.
- `scripts/stop_demo.ps1` — detener demo.
- `scripts/create_demo.py` — crear datos demo.

## Credenciales demo

- Usuario: `demo`
- Contraseña: `demo`

> Nota: no uses estas credenciales en producción; son sólo para la demo local.

## Cómo ejecutar (PowerShell)

Abre PowerShell en la raíz del repositorio (`C:\Users\j\familia_calendario_public`) y ejecuta:

1) Iniciar demo (abre una nueva ventana y espera a que el servidor esté listo):

```powershell
.\scripts\start_demo.ps1
```

El script hará:
- crear/usar `.venv` (si no existe), instalar dependencias (si `requirements.txt` está presente), ejecutar `makemigrations/migrate` y `scripts/create_demo.py`.
- abrir una nueva ventana PowerShell y ejecutar `python manage.py runserver 127.0.0.1:8000` usando el Python de la venv.
- esperará hasta que el puerto esté listo y guardará el PID en `.server_pid`.
- intentará abrir el navegador en `http://127.0.0.1:8000/`.

2) Verificar desde la ventana actual:

```powershell
# ver PID guardado
Get-Content .server_pid

# comprobar listener en el puerto 8000
netstat -a -n -o | Select-String ":8000"

# comprobación HTTP rápida
Invoke-WebRequest http://127.0.0.1:8000 -UseBasicParsing
Invoke-WebRequest http://127.0.0.1:8000/tareas/ -UseBasicParsing
Invoke-WebRequest http://127.0.0.1:8000/calendario/ -UseBasicParsing
Invoke-WebRequest http://127.0.0.1:8000/demo/ -UseBasicParsing
```

3) Parar el demo:

```powershell
.\scripts\stop_demo.ps1
```

Si la ventana donde se lanzó el servidor muestra un error, revisa esa ventana: `start_demo.ps1` abre la ventana y el output del servidor aparecerá allí.

## Notas técnicas / seguridad

- `DEBUG` está activado para facilitar debug en local (no usar en producción).
- La API (`/api/`) está protegida por defecto (DRF `IsAuthenticated`). Si quieres mostrar la API pública en el demo, edita `hogar/settings.py` y ajusta `REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']` a `['rest_framework.permissions.AllowAny']` (solo para demo).
 - El script `scripts/create_demo.py` crea datos demo y el usuario de pruebas `demo`.

## Plantillas y cambios realizados

Para que la demo funcione sin depender de plantillas privadas del repositorio original, se añadieron plantillas mínimas:
- `templates/base.html` (layout mínimo con nav y bloques `title`/`content`).
- `templates/tareas_lista.html` (lista de tareas con paginación).
- `templates/calendario.html` (vista calendario demo).
- `templates/admin_miembros.html` (vista miembros/avisos demo).
- `templates/registration/login.html` (login mínimo).

## Comprobaciones rápidas

Puedes correr estos pasos para verificar que el demo está listo:

```powershell
.\scripts\start_demo.ps1
# una vez listo
Invoke-WebRequest http://127.0.0.1:8000 -UseBasicParsing
Invoke-WebRequest http://127.0.0.1:8000/tareas/ -UseBasicParsing
Invoke-WebRequest http://127.0.0.1:8000/calendario/ -UseBasicParsing
```

## Siguientes pasos recomendados (para CV / portafolio)

- Añadir `demo_screenshots/` con 2-3 capturas (home, calendario, tareas).
- Documentar arquitectura breve: modelos clave y endpoints API (README técnico adicional).
- Si quieres exponer la API en el demo, puedo añadir un endpoint público limitado o tokens demo.

Si quieres que haga alguno de estos pasos ahora (añadir screenshots, publicar API demo, o crear README técnico con endpoints y ejemplos curl/python), dime cuál y lo hago.

## Limpieza para portafolio

He preparado una versión reducida lista para subir a servicios como Render. Para mantener el repositorio ligero y evitar subir datos de desarrollo, moví los backups y logs grandes a la carpeta `removed_for_portfolio/` en la raíz. Con esto el paquete minimal contiene sólo lo necesario para ejecutar la demo local o desplegarla en un host.

- Carpeta movida: `backup_import_*`, `backup_for_portfolio` -> `removed_for_portfolio/`
- Logs movidos: `server*.log`, `*.log.bak` -> `removed_for_portfolio/`

He creado además `portfolio_minimal.zip` en la raíz que contiene los archivos mínimos necesarios (manage.py, apps `hogar` y `tareas`, `templates/`, `static/`, `requirements.txt`, `db.sqlite3` si está presente, y scripts de arranque). Este archivo está listo para subir a Render o compartir como artefacto de portafolio.

Si prefieres que en lugar de `db.sqlite3` el paquete incluya sólo las migraciones y un `scripts/create_demo.py` idempotente, dímelo y lo recreo sin la base de datos.

Quick start local (Windows PowerShell)
1. Abre PowerShell en la raíz del repo.
2. Ejecuta el script de inicio rápido:

```powershell
.\scripts\quick_start.ps1
```

Esto creará (si es necesario) la virtualenv en `.venv`, instalará dependencias, aplicará migraciones, cargará los fixtures anonimizados y arrancará el servidor de desarrollo.

LinkedIn: he añadido `assets/linkedin_post_ready.md` con texto listo para pegar y `assets/social.png` para usar en la publicación.

## Despliegue rápido en Render

Instrucciones mínimas para desplegar en Render (servicio PaaS):

1) Subir el repo o `portfolio_minimal.zip` a un repositorio público (GitHub).
2) En Render, crear un nuevo "Web Service" apuntando a ese repo. Configura:
	 - Build command: `pip install -r requirements.txt`
	 - Start command: `./.venv/bin/python manage.py migrate --noinput && ./.venv/bin/python manage.py runserver 0.0.0.0:$PORT`
		 (en Windows/PowerShell la ruta de `.venv` será distinta; Render usa Linux por defecto, por eso las rutas anteriores.)
3) Si subes `db.sqlite3`, no hace falta correr `create_demo.py` en Render; de lo contrario habilita el script `scripts/create_demo.py` en el start command justo después de `migrate`.

Notas:
- Asegúrate de desactivar `DEBUG` y configurar variables de entorno sensibles para un despliegue público (SECRET_KEY, ALLOWED_HOSTS, base de datos si la migras a Postgres). Para demo de portafolio puedes mantener DEBUG=True si el acceso es privado.
- Si quieres, preparo el `render.yaml` (o `Dockerfile`) para que el despliegue en Render sea un clic.

Nota sobre los datos de ejemplo
-------------------------------
Los nombres de miembros incluidos en los fixtures (por ejemplo `mamá`, `papá`, `hijo_1`, `abuela`) son ejemplos ficticios usados únicamente para la demo y no representan a personas reales. Las credenciales reales y datos sensibles no están incluidos en esta copia para portfolio.

## Despliegue con Docker (local o en Render usando container)

He añadido un `Dockerfile` y dos `docker-compose` (uno con SQLite y otro con Postgres) para que puedas probar la demo en contenedores.

Construir y ejecutar (SQLite, rápido - bind al código para desarrollo):

```bash
docker compose build
docker compose up -d
```

Abrir en: http://localhost:8000

Para usar Postgres (persistencia):

```bash
docker compose -f docker-compose-postgres.yml build
docker compose -f docker-compose-postgres.yml up -d
```

Notas:
- El `Dockerfile` hace un `migrate`, intenta ejecutar `scripts/create_demo.py` y `collectstatic` durante la build (es un enfoque "best-effort" para demo). Si prefieres ejecutar estas tareas en runtime, puedo mover esos pasos al entrypoint.
- Render admite despliegue por contenedor: en la UI de Render crea un servicio tipo "Docker" apuntando al repo; Render construirá la imagen usando este `Dockerfile`. En ese caso configura variables de entorno (SECRET_KEY, DEBUG, DATABASE_URL) en la UI.

