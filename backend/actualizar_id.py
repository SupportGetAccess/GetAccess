import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()
cur.execute("UPDATE eventos SET id = 9 WHERE id = 12")
conn.commit()
print('ID actualizado de 12 a 9')
cur.execute('SELECT id, nombre FROM eventos ORDER BY id')
for row in cur.fetchall():
    print(row)
conn.close()