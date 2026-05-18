import os
import psycopg2

conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

# Verificar si existe la columna
cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name = 'entradas' AND column_name = 'expira_en'
""")
if cur.fetchone():
    print('Columna expira_en ya existe')
else:
    # Agregar columna
    cur.execute('ALTER TABLE entradas ADD COLUMN expira_en TIMESTAMP')
    conn.commit()
    print('Columna expira_en agregada correctamente')

cur.close()
conn.close()