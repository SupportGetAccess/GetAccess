import sqlite3
import bcrypt

password = 'Test123!'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print('Hash:', hashed)

conn = sqlite3.connect('access_on.db')
conn.execute('DELETE FROM usuarios WHERE email = "testuser@test.com"')
conn.execute('INSERT INTO usuarios (email, nombre, apellido, password, verificado) VALUES (?, ?, ?, ?, ?)',
    ('testuser@test.com', 'Test', 'User', hashed, 1))
conn.commit()

cursor = conn.execute('SELECT email, verificado FROM usuarios WHERE email = "testuser@test.com"')
print('Usuario creado:', cursor.fetchone())

conn.close()
