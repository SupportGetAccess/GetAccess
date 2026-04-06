import sqlite3
import bcrypt

conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
cur = conn.execute("SELECT password FROM usuarios WHERE email = 'aantoniaa1982@gmail.com'")
stored = cur.fetchone()
print("Stored hash:", stored[0] if stored else "No found")

# Test password
if stored:
    test = bcrypt.checkpw(b'guille123', stored[0].encode('utf-8'))
    print("Password 'guille123' matches:", test)
