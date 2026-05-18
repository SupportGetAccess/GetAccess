import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Ver rol de usuario
cur.execute("SELECT id, email, rol FROM usuarios WHERE email = 'aantoniaa1982@gmail.com'")
print("Usuario:", cur.fetchone())

# Ver solicitud
cur.execute("SELECT id, estado, created_at FROM solicitud_organizer WHERE usuario_id = 4")
print("Solicitud:", cur.fetchone())

conn.close()