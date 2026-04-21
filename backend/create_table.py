import psycopg2

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS solicitud_organizer (
        id SERIAL PRIMARY KEY,
        usuario_id INTEGER NOT NULL,
        estado TEXT DEFAULT 'pendiente',
        motivo_rechazo TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
print("Tabla creada!")

cur.close()
conn.close()