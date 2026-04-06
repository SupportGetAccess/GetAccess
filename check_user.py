import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
cur = conn.execute("SELECT id, email, nombre, verificado FROM usuarios WHERE email LIKE '%antoniaa%'")
print(cur.fetchall())
