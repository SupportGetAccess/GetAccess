import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()
cur.execute("DELETE FROM eventos WHERE nombre = 'Evento Prueba'")
conn.commit()
print('Eventos duplicados eliminados')
cur.execute('SELECT id, nombre FROM eventos ORDER BY id')
for row in cur.fetchall():
    print(row)
conn.close()