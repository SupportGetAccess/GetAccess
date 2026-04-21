import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Ver todos los usuarios
cur.execute("SELECT id, email, nombre, rol FROM usuarios ORDER BY id")
print("Todos los usuarios:")
for row in cur.fetchall():
    print(row)

# Ver cual es admin
cur.execute("SELECT email FROM usuarios WHERE rol = 'admin' ORDER BY id LIMIT 1")
admin = cur.fetchone()
print("\nAdmin actual:", admin[0] if admin else "NINGUNO")

conn.close()