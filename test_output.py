import requests
import traceback
import sys

form = {'email': 'guilles10@yahoo.ar', 'nombre': 'Willy', 'apellido': 'Test', 'password': 'MiPassword123!'}

# Capturar todo el output
import io
from contextlib import redirectstdout, redirectstderr

output = io.StringIO()

with redirectstdout(output), redirectstderr(output):
    r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=form, timeout=60)

print(f'Status: {r.status_code}')
print(f'Respuesta: {r.json()}')
print(f'\nLogs del servidor (stdout):')
print(output.getvalue())
