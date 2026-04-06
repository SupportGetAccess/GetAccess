import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tablas:", [r[0] for r in cur.fetchall()])
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transferencias'")
print("Tabla transferencias:", cur.fetchone())
conn.close()
