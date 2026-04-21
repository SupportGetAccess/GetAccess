import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Ver admin
cur.execute("SELECT id, email, nombre, rol FROM usuarios WHERE rol = 'admin'")
print("Admin:", cur.fetchall())

# Ver solicitudes recientes
cur.execute("SELECT id, usuario_id, estado, created_at FROM solicitud_organizer ORDER BY created_at DESC LIMIT 5")
print("\nSolicitudes:", cur.fetchall())

conn.close()