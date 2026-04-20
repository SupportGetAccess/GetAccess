import os
os.environ["RENDER"] = "1"
import psycopg2
import bcrypt
import config

conn = psycopg2.connect(config.DATABASE_URL)
cur = conn.cursor()

cur.execute("SELECT email, password FROM usuarios WHERE email = 'aantoniaa1982@gmail.com'")
row = cur.fetchone()
print(f"Email: {row[0]}")
print(f"Hash stored: {row[1][:60]}...")

# Probar la password
test_pass = "guille123"
result = bcrypt.checkpw(test_pass.encode(), row[1].encode())
print(f"Password match: {result}")

conn.close()