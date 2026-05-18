import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

user_id = 2

print("=== Test 1: ventas total (organizer) ===")
cur.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas JOIN eventos ON entradas.evento_id = eventos.id WHERE entradas.estado = 'pagada' AND eventos.creado_por = %s", (user_id,))
print(cur.fetchone())

print("\n=== Test 2: Por categoria (organizer) ===")
cur.execute("""
    SELECT COALESCE(eventos.categoria, 'sin_categoria') as cat, COUNT(*) as cantidad
    FROM entradas
    JOIN eventos ON entradas.evento_id = eventos.id
    WHERE entradas.estado = 'pagada' AND eventos.creado_por = %s
    GROUP BY cat
""", (user_id,))
print(cur.fetchall())

print("\n=== Test 3: Top eventos (organizer) ===")
cur.execute("""
    SELECT e.id, e.nombre, e.vendidos, (e.vendidos * e.precio) as ingresos
    FROM eventos e
    WHERE e.vendidos > 0 AND e.creado_por = %s
    ORDER BY e.vendidos DESC
    LIMIT 10
""", (user_id,))
print(cur.fetchall())

print("\n=== Test 4: Validaciones (organizer) ===")
cur.execute("""
    SELECT COUNT(*) FROM validaciones v
    JOIN entradas e ON v.entrada_id = e.id
    JOIN eventos ev ON e.evento_id = ev.id
    WHERE ev.creado_por = %s
""", (user_id,))
print(cur.fetchone())

print("\n=== Test 5: Ventas por dia (organizer) ===")
cur.execute("""
    SELECT DATE(creada_en)::date as fecha, SUM(cantidad) as cantidad
    FROM entradas
    JOIN eventos ON entradas.evento_id = eventos.id
    WHERE entradas.estado = 'pagada' AND eventos.creado_por = %s AND creada_en >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY fecha
    ORDER BY fecha DESC
    LIMIT 14
""", (user_id,))
print(cur.fetchall())

conn.close()