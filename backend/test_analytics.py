import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Test queries que usa analytics
user_id = 1  # admin

print("=== Test 1: ventas total ===")
cur.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas WHERE estado = 'pagada'")
print(cur.fetchone())

print("\n=== Test 2: validaciones ===")
cur.execute("SELECT COUNT(*) FROM validaciones")
print(cur.fetchone())

print("\n=== Test 3: por categoria ===")
cur.execute("""
    SELECT COALESCE(eventos.categoria, 'sin_categoria') as cat, COUNT(*) as cantidad
    FROM entradas
    JOIN eventos ON entradas.evento_id = eventos.id
    WHERE entradas.estado = 'pagada'
    GROUP BY cat
""")
print(cur.fetchall())

print("\n=== Test 4: top eventos ===")
cur.execute("SELECT id, nombre, vendidos FROM eventos WHERE vendidos > 0 ORDER BY vendidos DESC LIMIT 5")
for r in cur.fetchall():
    print(r)

print("\n=== Test 5: ventas por dia (PostgreSQL) ===")
cur.execute("""
    SELECT DATE(creada_en)::date as fecha, SUM(cantidad) as cantidad
    FROM entradas
    WHERE estado = 'pagada' AND creada_en >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY fecha
    ORDER BY fecha DESC
    LIMIT 5
""")
print(cur.fetchall())

conn.close()