import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Eliminar usuario admin@getaccess.com
cur.execute("DELETE FROM usuarios WHERE email = 'admin@getaccess.com'")
conn.commit()
print("Usuario admin@getaccess.com eliminado")

# Verificar
cur.execute("SELECT id, email, rol FROM usuarios WHERE rol = 'admin'")
print("\nAdmins restantes:")
for row in cur.fetchall():
    print(row)

conn.close()