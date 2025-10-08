# Imprimir esquema de tablas relevantes
import sqlite3
from pathlib import Path
DB = Path(__file__).resolve().parent.parent / 'db.sqlite3'
con = sqlite3.connect(str(DB))
cur = con.cursor()
for tbl in ('tareas_categoria','tareas_tarea','tareas_miembro'):
    print('TABLE', tbl)
    try:
        cur.execute(f"PRAGMA table_info('{tbl}')")
        rows = cur.fetchall()
        for r in rows:
            print('  ', r)
    except Exception as e:
        print('  ERROR', e)
    print()
con.close()
