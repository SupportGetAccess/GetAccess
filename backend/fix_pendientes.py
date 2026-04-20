import os
os.environ["RENDER"] = "1"
import psycopg2
import config

conn = psycopg2.connect(config.DATABASE_URL)
cur = conn.cursor()

cur.execute("UPDATE entradas SET preference_id = NULL WHERE estado = 'pendiente'")
print(f"Entradas pendientes actualizadas: {cur.rowcount}")

conn.commit()
conn.close()
print("Listo")