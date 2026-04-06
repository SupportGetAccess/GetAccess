import requests

# Registro
data = {'email': 'guilles10@yahoo.com.ar', 'nombre': 'Willy', 'apellido': 'Test', 'password': 'Test1234!'}
r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=data, timeout=20)
print(f'Registro: {r.status_code}')
print(r.text)
