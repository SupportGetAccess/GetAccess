import requests

form = {'email': 'guilles10@yahoo.com.ar', 'nombre': 'Willy', 'apellido': 'Test', 'password': 'MiPassword123!'}
r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=form, timeout=30)
print(f'Registro: {r.status_code}')
print(f'Respuesta: {r.json()}')
