import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Corregir rol de usuario - estaba rechazado pero tiene rol organizer
cur.execute("UPDATE usuarios SET rol = 'usuario' WHERE email = 'aantoniaa1982@gmail.com'")
conn.commit()
print("Usuario corregido a 'usuario'")

# Verificar
cur.execute("SELECT id, email, rol FROM usuarios WHERE email = 'aantoniaa1982@gmail.com'")
print("Ahora:", cur.fetchone())

conn.close()