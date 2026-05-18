import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Ver admins verificados
cur.execute("SELECT id, email, rol, verificado FROM usuarios WHERE rol = 'admin'")
print("Admins:")
for row in cur.fetchall():
    print(row)

conn.close()