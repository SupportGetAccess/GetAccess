import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Corregir rol de usuario - estaba rechazado pero tiene rol organizer
cur.execute("UPDATE usuarios SET rol = 'usuario' WHERE email = 'aantoniaa1982@gmail.com'")
conn.commit()
print("Usuario corregido a 'usuario'")

# Verificar
cur.execute("SELECT id, email, rol FROM usuarios WHERE email = 'aantoniaa1982@gmail.com'")
print("Ahora:", cur.fetchone())

conn.close()