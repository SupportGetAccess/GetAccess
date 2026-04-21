import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Test 1: Admin (user_id=1) - debe traer todo
print("=== Admin (user_id=1) ===")
cur.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas WHERE estado = 'pagada'")
print("Result:", cur.fetchone())

# Test 2: Usuario normal (user_id=4) - debe traer 0 porque no tiene eventos
print("\n=== Usuario normal (user_id=4) ===")
cur.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas JOIN eventos ON entradas.evento_id = eventos.id WHERE entradas.estado = 'pagada' AND eventos.creado_por = 4")
print("Result:", cur.fetchone())

# Verificar eventos propios del usuario 4
print("\n=== Eventos propios del usuario 4 ===")
cur.execute("SELECT id, nombre FROM eventos WHERE creado_por = 4")
print(cur.fetchall())

# Verificar entrada con evento propio del usuario 4
print("\n=== Entradas con eventos del usuario 4 ===")
cur.execute("SELECT e.id, e.nombre, en.id FROM entradas en JOIN eventos e ON en.evento_id = e.id WHERE e.creado_por = 4")
print(cur.fetchall())

conn.close()