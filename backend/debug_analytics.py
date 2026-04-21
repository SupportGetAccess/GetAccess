import psycopg2
import traceback
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Verificar columna
print("=== Columnas de eventos ===")
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'eventos'")
cols = cur.fetchall()
for c in cols:
    print(c[0])

# Verificar si hay eventos con creado_por
print("\n=== Eventos con creador ===")
cur.execute("SELECT id, nombre, creado_por FROM eventos WHERE creado_por IS NOT NULL LIMIT 5")
print(cur.fetchall())

# Verificar si hay entradas
print("\n=== Entradas pagadas ===")
cur.execute("SELECT COUNT(*) FROM entradas WHERE estado = 'pagada'")
print("Total:", cur.fetchone())

# Test query analytics
print("\n=== Test query analytics ===")
user_id = 4  # aantoniaa1982@gmail.com
try:
    cur.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas JOIN eventos ON entradas.evento_id = eventos.id WHERE entradas.estado = 'pagada' AND eventos.creado_por = %s", (user_id,))
    print("Result:", cur.fetchone())
except Exception as e:
    print("Error:", e)

conn.close()