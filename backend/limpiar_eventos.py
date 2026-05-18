import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()
cur.execute("DELETE FROM eventos WHERE nombre = 'Evento Prueba'")
conn.commit()
print('Eventos duplicados eliminados')
cur.execute('SELECT id, nombre FROM eventos ORDER BY id')
for row in cur.fetchall():
    print(row)
conn.close()