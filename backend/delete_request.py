import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))

cur = conn.cursor()

# Ver solicitudes pendientes del usuario 8
# Ver solicitudes pendientes del usuario (ID 4)
cur.execute("SELECT * FROM solicitud_organizer WHERE usuario_id = 4")
print("Solicitudes pendientes:", cur.fetchall())

# Eliminar solicitudes pendientes
cur.execute("DELETE FROM solicitud_organizer WHERE usuario_id = 4 AND estado = 'pendiente'")
conn.commit()
print("Solicitudes pendientes eliminadas")

# Verificar
cur.execute("SELECT * FROM solicitud_organizer WHERE usuario_id = 4")
print("Restantes:", cur.fetchall())

conn.close()