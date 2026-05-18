import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Simular lo que hace el backend
# Usuario admin (user_id=1)
user_id = 1

print("=== Test 1: Obtener rol del usuario ===")
cur.execute("SELECT COALESCE(rol, 'usuario') FROM usuarios WHERE id = %s", (user_id,))
print(cur.fetchone())

print("\n=== Test 2: ventas total (admin) ===")
cur.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas WHERE estado = 'pagada'")
print(cur.fetchone())

print("\n=== Test 3: ventas total (organizer) ===")
cur.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas JOIN eventos ON entradas.evento_id = eventos.id WHERE entradas.estado = 'pagada' AND eventos.creado_por = %s", (user_id,))
print(cur.fetchone())

# Verificar la estructura de la tabla entradas
print("\n=== Entradas ===")
cur.execute("SELECT id, evento_id, usuario_id, cantidad, total, estado FROM entradas LIMIT 3")
for r in cur.fetchall():
    print(r)

# Verificar eventos
print("\n=== Eventos ===")
cur.execute("SELECT id, nombre, creado_por FROM eventos LIMIT 3")
for r in cur.fetchall():
    print(r)

conn.close()