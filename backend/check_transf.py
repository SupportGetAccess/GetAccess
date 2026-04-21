import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Verificar transferencias
cur.execute("SELECT * FROM transferencias")
print("=== TRANSFERENCIAS ===")
for row in cur.fetchall():
    print(row)

print("\n=== RESUMEN DE REFERENCIAS ===")
print("""
TABLA                    | REFERENCIA
------------------------|------------------
entradas                 | usuario_id
solicitud_organizer     | usuario_id
transferencias         | usuario_origen, usuario_destino
password_reset         | (email - no es ID)
""")

conn.close()