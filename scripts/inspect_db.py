import sqlite3, os
db = r'c:/Users/j/familia_calendario_public/db.sqlite3'
print('DB exists' if os.path.exists(db) else 'DB missing')
if os.path.exists(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','index') ORDER BY type, name")
    for name, typ in cur.fetchall():
        print(typ, name)
    con.close()
