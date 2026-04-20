import os
os.environ["RENDER"] = "1"
import psycopg2
import random
import string
import config

conn = psycopg2.connect(config.DATABASE_URL)
cur = conn.cursor()

cur.execute("SELECT id FROM entradas WHERE preference_id LIKE 'GA-0%' OR preference_id LIKE 'GA-1%'")
entradas = cur.fetchall()
print(f"Entradas con formato viejo: {len(entradas)}")

for row in entradas:
    entrada_id = row[0]
    nuevo_codigo = f"GA-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
    cur.execute("UPDATE entradas SET preference_id = %s WHERE id = %s", (nuevo_codigo, entrada_id))
    print(f"  {entrada_id} -> {nuevo_codigo}")

conn.commit()
conn.close()
print("\nCodigos actualizados")