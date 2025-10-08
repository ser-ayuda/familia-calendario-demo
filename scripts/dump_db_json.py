# Script para extraer tablas relevantes desde db.sqlite3 y volcar JSON
import sqlite3, json
from pathlib import Path
DB = Path(__file__).resolve().parent.parent / 'db.sqlite3'
con = sqlite3.connect(str(DB))
con.row_factory = sqlite3.Row
cur = con.cursor()
out = {}
for tbl, cols in [
    ('auth_user', ['id','username','email','is_superuser','is_staff'] ),
    ('tareas_miembro', ['id','nombre','usuario_id','color_hex','icono'] ),
    ('tareas_categoria', ['id','nombre','descripcion','icono'] ),
    ('tareas_tarea', ['id','nombre','descripcion','categoria_id','puntuacion','tag','icono','premio'] ),
    ('tareas_evento', ['id','tarea_id','miembro_id','inicio','fin','estado'] ),
]:
    try:
        cur.execute('select %s from %s' % (','.join(cols), tbl))
        rows = [dict(r) for r in cur.fetchall()]
        out[tbl] = rows
    except Exception as e:
        out[tbl] = f'ERROR: {e}'
print(json.dumps(out, default=str, ensure_ascii=False, indent=2))
con.close()
