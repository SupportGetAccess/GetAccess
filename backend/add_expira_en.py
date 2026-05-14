import psycopg2

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
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