import os
os.environ["RENDER"] = "1"
import psycopg2
import config

conn = psycopg2.connect(config.DATABASE_URL)
cur = conn.cursor()

cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'entradas' ORDER BY ordinal_position")
print("Columnas de entradas:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'usuarios' ORDER BY ordinal_position")
print("\nColumnas de usuarios:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()