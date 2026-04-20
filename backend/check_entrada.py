import os
os.environ["RENDER"] = "1"
import psycopg2
import config

conn = psycopg2.connect(config.DATABASE_URL)
cur = conn.cursor()

cur.execute("SELECT id, preference_id, estado, usada, transferida FROM entradas WHERE preference_id = 'GA-Y6VR7DFSMA'")
row = cur.fetchone()
if row:
    print(f"ID: {row[0]}, Codigo: {row[1]}, Estado: {row[2]}, Usada: {row[3]}, Transferida: {row[4]}")
else:
    print("Entrada no encontrada")

conn.close()