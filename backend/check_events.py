import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Ver eventos creados por usuario 2
print("=== Eventos creados por usuario ID 2 ===")
cur.execute("SELECT id, nombre, creado_por FROM eventos WHERE creado_por = 2")
for r in cur.fetchall():
    print(r)

# Ver entradas de eventos creados por usuario 2
print("\n=== Entradas de eventos del usuario 2 ===")
cur.execute("""
    SELECT en.id, en.evento_id, en.usuario_id, en.cantidad, en.total, e.nombre
    FROM entradas en
    JOIN eventos e ON en.evento_id = e.id
    WHERE e.creado_por = 2 AND en.estado = 'pagada'
""")
for r in cur.fetchall():
    print(r)

# Ver rol actual del usuario
print("\n=== Rol del usuario ===")
cur.execute("SELECT id, email, rol FROM usuarios WHERE id = 2")
print(cur.fetchone())

conn.close()