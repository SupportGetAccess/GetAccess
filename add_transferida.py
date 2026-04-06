import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
cur = conn.execute("PRAGMA table_info(entradas)")
cols = [c[1] for c in cur.fetchall()]
if 'transferida' not in cols:
    conn.execute("ALTER TABLE entradas ADD COLUMN transferida INTEGER DEFAULT 0")
    conn.commit()
    print("Columna 'transferida' agregada")
else:
    print("Columna ya existe")
conn.close()
