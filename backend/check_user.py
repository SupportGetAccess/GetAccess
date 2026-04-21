import sqlite3
conn = sqlite3.connect(r'C:\Users\guill\eventos_tickets_full\backend\access_on.db')

# Ver solicitudes pendientes del usuario 8
cur = conn.execute("SELECT * FROM solicitud_organizer WHERE usuario_id = 8")
print("Solicitudes pendientes:", cur.fetchall())

# Eliminar solicitudes pendientes
conn.execute("DELETE FROM solicitud_organizer WHERE usuario_id = 8 AND estado = 'pendiente'")
conn.commit()
print("Solicitudes eliminadas")

# Verificar
cur = conn.execute("SELECT * FROM solicitud_organizer WHERE usuario_id = 8")
print("Solicitudes restantes:", cur.fetchall())
conn.close()