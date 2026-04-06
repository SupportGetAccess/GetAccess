import requests
import json
import sqlite3

# Eliminar usuario
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
conn.execute("DELETE FROM usuarios WHERE email='guilles10@yahoo.com.ar'")
conn.commit()
conn.close()

# Simular lo que hace el frontend
form = {'email': 'guilles10@yahoo.com.ar', 'nombre': 'Willy', 'apellido': 'Test', 'password': 'Test1234!'}

headers = {'Content-Type': 'application/json'}
r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=form, headers=headers, timeout=30)

print(f'Status: {r.status_code}')
print(f'Response: {r.text}')
