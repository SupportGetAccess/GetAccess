import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
cur = conn.cursor()
# Buscar en todas las tablas
cur.execute("SELECT id, evento_id, usuario_id, cantidad, estado, preference_id FROM entradas")
print("Todas las entradas:")
for e in cur.fetchall():
    if e[5] and "Y6VR7DFSMA" in str(e[5]):
        print(e)