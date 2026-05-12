import psycopg2

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

try:
    cur.execute('ALTER TABLE entradas ADD COLUMN IF NOT EXISTS payment_order_id TEXT')
    conn.commit()
    print('Columna payment_order_id agregada correctamente')
except Exception as e:
    print(f'Error: {e}')
    conn.rollback()

cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'entradas' AND column_name = 'payment_order_id'")
if cur.fetchone():
    print('Verificado: columna existe en la tabla entradas')
else:
    print('ERROR: columna no encontrada')

conn.close()