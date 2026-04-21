import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')

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