import sqlite3
import bcrypt

# Nueva contraseña hasheada
new_password = "guille123"
hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
conn.execute("UPDATE usuarios SET password = ? WHERE email = 'aantoniaa1982@gmail.com'", (hashed.decode('utf-8'),))
conn.commit()
print("Password reseteada para aantoniaa1982@gmail.com")
