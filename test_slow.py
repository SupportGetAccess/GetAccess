import requests
import time

form = {'email': 'guilles10@yahoo.com.ar', 'nombre': 'Willy', 'apellido': 'Test', 'password': 'MiPassword123!'}
r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=form, timeout=60)
print(f'Status: {r.status_code}')
data = r.json()
print(f'Respuesta: {data}')
print(f'Email enviado: {data.get("email_enviado")}')
