import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Ver columnas de entradas
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'entradas' ORDER BY ordinal_position")
print("=== Columnas de entradas ===")
for row in cur.fetchall():
    print(row[0])

conn.close()