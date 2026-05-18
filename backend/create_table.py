import os
import psycopg2

conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
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