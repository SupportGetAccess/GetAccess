import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Ver rol de usuario
cur.execute("SELECT id, email, rol FROM usuarios WHERE email = 'aantoniaa1982@gmail.com'")
print("Usuario:", cur.fetchone())

# Ver solicitud
cur.execute("SELECT id, estado, created_at FROM solicitud_organizer WHERE usuario_id = 4")
print("Solicitud:", cur.fetchone())

conn.close()