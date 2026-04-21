import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Las entradas con usuario_id=4 ahora son del usuario 2 (antonia)
cur.execute("UPDATE entradas SET usuario_id = 2 WHERE usuario_id = 4")
print("Entradas actualizadas: 4 -> 2")

conn.commit()

print("\n=== Verificacion ===")
cur.execute("SELECT id, usuario_id, evento_id FROM entradas ORDER BY id")
for row in cur.fetchall():
    print(row)

conn.close()