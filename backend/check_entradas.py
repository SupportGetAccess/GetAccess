import os
os.environ["RENDER"] = "1"
import psycopg2
import config

conn = psycopg2.connect(config.DATABASE_URL)
cur = conn.cursor()

cur.execute("SELECT id, evento_id, usuario_id, cantidad, total, estado, preference_id FROM entradas ORDER BY id DESC LIMIT 5")
print("Ultimas entradas:")
for row in cur.fetchall():
    print(row)

conn.close()