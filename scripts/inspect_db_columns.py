import sqlite3, json
c=sqlite3.connect('db.sqlite3')
cur=c.cursor()
cur.execute('PRAGMA table_info("tareas_aviso")')
rows=cur.fetchall()
print(json.dumps(rows, ensure_ascii=False, indent=2))
