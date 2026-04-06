import requests
import sqlite3

# Eliminar usuario si existe
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
conn.execute("DELETE FROM usuarios WHERE email='guilles10@yahoo.com.ar'")
conn.commit()
conn.close()

# Hacer registro
data = {'email': 'guilles10@yahoo.com.ar', 'nombre': 'Willy', 'apellido': 'de Q', 'password': 'Test1234!'}
r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=data, timeout=20)
print(f'Registro: {r.status_code}')
print(r.text[:300])
