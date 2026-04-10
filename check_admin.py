import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
cur = conn.execute("SELECT email, nombre, rol FROM usuarios WHERE rol='admin'")
print(list(cur))