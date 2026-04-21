import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Cambiar ID: 2 -> 1 y 4 -> 2
# Primero verificar dependencias
print("=== Verificando tablas relacionadas ===")

# entradas
cur.execute("SELECT COUNT(*) FROM entradas WHERE usuario_id = 2")
print(f"entradas usuario_id=2: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM entradas WHERE usuario_id = 4")
print(f"entradas usuario_id=4: {cur.fetchone()[0]}")

# eventos (creado_por)
cur.execute("SELECT COUNT(*) FROM eventos WHERE creado_por = 2")
print(f"eventos creado_por=2: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM eventos WHERE creado_por = 4")
print(f"eventos creado_por=4: {cur.fetchone()[0]}")

# solicitud_organizer
cur.execute("SELECT COUNT(*) FROM solicitud_organizer WHERE usuario_id = 2")
print(f"solicitud_organizer usuario_id=2: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM solicitud_organizer WHERE usuario_id = 4")
print(f"solicitud_organizer usuario_id=4: {cur.fetchone()[0]}")

# password_reset
cur.execute("SELECT COUNT(*) FROM password_reset WHERE email IN ('guilles10@yahoo.com.ar', 'aantoniaa1982@gmail.com')")
print(f"password_reset: {cur.fetchone()[0]}")

print("\n=== Cambiando IDs ===")

# Necesitamos secuencia temporal para evitar conflictos
# Primero cambia 2 a temporal 999
cur.execute("UPDATE usuarios SET id = 999 WHERE id = 2")
print("ID 2 -> 999")

# Cambia 4 a 2
cur.execute("UPDATE usuarios SET id = 2 WHERE id = 4")
print("ID 4 -> 2")

# Cambia 999 a 1
cur.execute("UPDATE usuarios SET id = 1 WHERE id = 999")
print("ID 999 -> 1")

conn.commit()

# Verificar
print("\n=== Resultado ===")
cur.execute("SELECT id, email, rol FROM usuarios ORDER BY id")
for row in cur.fetchall():
    print(row)

conn.close()