import requests
import sys
import io

# Capturar stdout
old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()

# Ejecutar registro
form = {'email': 'guilles10@yahoo.com.ar', 'nombre': 'Willy', 'apellido': 'Test', 'password': 'MiPassword123!'}
r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=form, timeout=30)

# Restaurar stdout
output = buffer.getvalue()
sys.stdout = old_stdout

print(f'Registro: {r.status_code}')
print(f'Respuesta: {r.json()}')
print(f'\nLogs del servidor:')
print(output)
