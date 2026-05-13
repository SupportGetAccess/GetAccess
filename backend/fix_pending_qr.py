import psycopg2

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

print("=== Estado antes ===")
cur.execute("SELECT COUNT(*) FROM entradas WHERE estado = 'pendiente'")
print(f"Entradas pendientes: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM entradas WHERE preference_id LIKE 'QR-%' AND estado = 'pendiente' AND payment_order_id IS NULL")
print(f"Con QR en preference_id pero sin payment_order_id: {cur.fetchone()[0]}")

print("\n=== Corrigiendo ===")
cur.execute("""
    UPDATE entradas
    SET payment_order_id = preference_id
    WHERE preference_id LIKE 'QR-%'
    AND estado = 'pendiente'
    AND payment_order_id IS NULL
""")
conn.commit()
print(f"Entradas actualizadas: {cur.rowcount}")

print("\n=== Estado después ===")
cur.execute("SELECT COUNT(*) FROM entradas WHERE estado = 'pendiente'")
print(f"Entradas pendientes restantes: {cur.fetchone()[0]}")

conn.close()
print("\n✅ Proceso completado")