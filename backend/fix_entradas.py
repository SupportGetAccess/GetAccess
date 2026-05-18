import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Las entradas con usuario_id=4 ahora son del usuario 2 (antonia)
cur.execute("UPDATE entradas SET usuario_id = 2 WHERE usuario_id = 4")
print("Entradas actualizadas: 4 -> 2")

conn.commit()

print("\n=== Verificacion ===")
cur.execute("SELECT id, usuario_id, evento_id FROM entradas ORDER BY id")
for row in cur.fetchall():
    print(row)

conn.close()