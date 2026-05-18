import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Ver admin
cur.execute("SELECT id, email, nombre, rol FROM usuarios WHERE rol = 'admin'")
print("Admin:", cur.fetchall())

# Ver solicitudes recientes
cur.execute("SELECT id, usuario_id, estado, created_at FROM solicitud_organizer ORDER BY created_at DESC LIMIT 5")
print("\nSolicitudes:", cur.fetchall())

conn.close()