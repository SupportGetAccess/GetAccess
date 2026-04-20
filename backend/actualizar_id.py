import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()
cur.execute("UPDATE eventos SET id = 9 WHERE id = 12")
conn.commit()
print('ID actualizado de 12 a 9')
cur.execute('SELECT id, nombre FROM eventos ORDER BY id')
for row in cur.fetchall():
    print(row)
conn.close()