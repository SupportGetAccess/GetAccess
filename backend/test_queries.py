import os
import psycopg2
import traceback
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Test 1: ventas total
print("=== Test 1: ventas total ===")
try:
    cur.execute("SELECT COUNT(*) as cnt, COALESCE(SUM(total), 0 as total, COALESCE(SUM(cantidad), 0) as cnt_total FROM entradas WHERE estado = 'pagada'")
    print("Result:", cur.fetchone())
except Exception as e:
    print("Error:", e)
    traceback.print_exc()

# Test 2: entradas join eventos
print("\n=== Test 2: entradas join eventos ===")
try:
    cur.execute("SELECT e.id, e.nombre, e.creado_por FROM eventos e ORDER BY e.id LIMIT 5")
    print("Eventos:", cur.fetchall())
except Exception as e:
    print("Error:", e)

# Test 3: verificar columna
print("\n=== Test 3: verificar columna creado_por ===")
try:
    cur.execute("SELECT id, nombre, creado_por FROM eventos WHERE creado_por IS NOT NULL LIMIT 5")
    print("Con creador:", cur.fetchall())
except Exception as e:
    print("Error:", e)

conn.close()