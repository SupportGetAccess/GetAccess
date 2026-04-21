import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

print("=== SOLICITUD ORGanizer ===\n")
cur.execute("SELECT * FROM solicitud_organizer ORDER BY id")
column_names = [desc[0] for desc in cur.description]
print("Columnas:", column_names)
print()

for row in cur.fetchall():
    print(f"ID: {row[0]}")
    print(f"  usuario_id: {row[1]}")
    print(f"  estado: {row[2]}")
    print(f"  motivo_rechazo: {row[3]}")
    print(f"  created_at: {row[4]}")
    print()

conn.close()