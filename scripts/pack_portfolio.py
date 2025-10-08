"""Crea portfolio_minimal.zip con solo los archivos indispensables para la demo/portafolio.
Lista de inclusión (relativa a la raíz del repo):
- manage.py
- hogar/** (todos los ficheros .py necesarios)
- tareas/** (módulo de la app)
- templates/**
- static/**
- requirements.txt
- README*.md
- scripts/start_demo.ps1, scripts/stop_demo.ps1, scripts/create_demo.py y otros scripts útiles
- db.sqlite3 (opcional, si existe)

El script ignora archivos de backup y logs.
"""
import zipfile
from pathlib import Path
import fnmatch

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'portfolio_minimal.zip'
INCLUDE = [
    'manage.py',
    'requirements.txt',
    'db.sqlite3',
    'hogar',
    'tareas',
    'templates',
    'static',
    'README.md',
    'README_demo.md',
    'README_PORTFOLIO.md',
    'scripts/start_demo.ps1',
    'scripts/stop_demo.ps1',
    'scripts/create_demo.py',
    'scripts/runserver_foreground.ps1',
]

# Helper to decide if a path should be included
def should_include(p: Path):
    # include if matches any include prefix
    rel = p.relative_to(ROOT).as_posix()
    for inc in INCLUDE:
        if rel == inc:
            return True
        if inc.endswith('/'):
            if rel.startswith(inc.rstrip('/')):
                return True
        else:
            # directory include
            if p.is_dir() and rel == inc:
                return True
            if rel.startswith(inc + '/'):
                return True
    return False

# Collect files
files = []
for p in ROOT.rglob('*'):
    # skip the removed_for_portfolio folder if it exists
    if 'removed_for_portfolio' in p.parts:
        continue
    if p.is_file():
        if should_include(p):
            files.append(p)

if not files:
    print('No files matched inclusion list. Adjust INCLUDE in the script.')
else:
    print(f'Adding {len(files)} files to {OUT.name}')
    with zipfile.ZipFile(OUT, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for f in files:
            arcname = f.relative_to(ROOT).as_posix()
            z.write(f, arcname)
    print('Created', OUT)
