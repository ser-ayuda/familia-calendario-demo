import shutil, datetime, os, sqlite3
from pathlib import Path

DB = Path('db.sqlite3')
if not DB.exists():
    print('ERROR: db.sqlite3 not found')
    raise SystemExit(1)

now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
bak = Path(f'db.sqlite3.bak_{now}')
shutil.copy(str(DB), str(bak))
size = bak.stat().st_size
print('BACKUP_CREATED', str(bak), f'{size} bytes')

# Open and run integrity check
try:
    con = sqlite3.connect(str(bak))
    cur = con.cursor()
    cur.execute('PRAGMA integrity_check;')
    res = cur.fetchone()
    integrity = res[0] if res else 'NO RESULT'
    print('INTEGRITY_CHECK', integrity)

    tables = ['tareas_miembro','tareas_tarea','tareas_evento','auth_user']
    for t in tables:
        try:
            cur.execute(f'SELECT count(*) FROM {t};')
            c = cur.fetchone()[0]
        except Exception as e:
            c = f'ERROR: {e}'
        print('COUNT', t, c)
    con.close()
except Exception as e:
    print('ERROR checking backup:', e)
    raise
