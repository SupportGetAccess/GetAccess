import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')

# Ver entradas sin código
cur = conn.execute('SELECT id, preference_id, estado, usuario_id FROM entradas WHERE preference_id IS NULL OR preference_id = ""')
sin_codigo = cur.fetchall()
print(f"Entradas sin código encontradas: {len(sin_codigo)}")
for e in sin_codigo:
    print(f"  ID: {e[0]}, Estado: {e[2]}, Usuario: {e[3]}")

# Eliminar
if sin_codigo:
    ids = [e[0] for e in sin_codigo]
    conn.execute(f'DELETE FROM entradas WHERE id IN ({",".join("?"*len(ids))})', ids)
    conn.commit()
    print(f"\nEliminadas {len(ids)} entradas sin código")

conn.close()
