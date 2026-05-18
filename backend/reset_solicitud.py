import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Eliminar solicitudes anteriores del usuario 4
cur.execute("DELETE FROM solicitud_organizer WHERE usuario_id = 4")
conn.commit()
print("Solicitudes anteriores eliminadas")

# Verificar estado actual del usuario
cur.execute("SELECT id, email, rol FROM usuarios WHERE id = 4")
print("Usuario actual:", cur.fetchone())

print("\nAhora el usuario puede solicitar ser organizador nuevamente desde el Perfil")

conn.close()