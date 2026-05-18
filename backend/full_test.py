import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Test analytics completo
user_id = 2  # aantoniaa1982@gmail.com

print("=== 1. Obtener rol ===")
cur.execute("SELECT COALESCE(rol, 'usuario') FROM usuarios WHERE id = %s", (user_id,))
rol = cur.fetchone()
print(f"Rol: {rol[0]}")

print("\n=== 2. Ventas total - admin ===")
cur.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas WHERE estado = 'pagada'")
print(cur.fetchone())

print("\n=== 3. Ventas total - organizador ===")
cur.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas JOIN eventos ON entradas.evento_id = eventos.id WHERE entradas.estado = 'pagada' AND eventos.creado_por = %s", (user_id,))
print(cur.fetchone())

print("\n=== 4. Por categoría ===")
cur.execute("""
    SELECT COALESCE(eventos.categoria, 'sin_categoria') as cat, COUNT(*) as cantidad
    FROM entradas
    JOIN eventos ON Entradas.evento_id = eventos.id
    WHERE entradas.estado = 'pagada'
    GROUP BY cat
""")
print(cur.fetchall())

print("\n=== 5. Top eventos ===")
cur.execute("""
    SELECT e.id, e.nombre, e.vendidos, (e.vendidos * e.precio) as ingresos
    FROM eventos e
    WHERE e.vendidos > 0
    ORDER BY e.vendidos DESC
    LIMIT 5
""")
for r in cur.fetchall():
    print(r)

print("\n=== 6. Validaciones ===")
cur.execute("SELECT COUNT(*) FROM validaciones")
print(cur.fetchone())

print("\n=== 7. Ventas por día ===")
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