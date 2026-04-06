import sqlite3
import bcrypt

password = 'Test123!'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print('Password:', password)
print('Hash:', hashed)

conn = sqlite3.connect('access_on.db')
conn.execute('DELETE FROM usuarios WHERE email LIKE "%guilles10%"')
conn.execute('INSERT INTO usuarios (email, nombre, apellido, password, verificado) VALUES (?, ?, ?, ?, ?)',
    ('guilles10@yahoo.com', 'Willy', 'Test', hashed, 1))
conn.commit()
conn.close()
print('Usuario creado!')
