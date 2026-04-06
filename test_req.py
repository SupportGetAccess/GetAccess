import requests

form = {'email': 'test@prueba.com', 'nombre': 'Test', 'apellido': 'User', 'password': 'Test1234!'}
r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=form, timeout=20)
print(f'Status: {r.status_code}')
print(f'Response: {r.text}')
