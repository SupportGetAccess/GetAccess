import requests

print("=== SIMULANDO REGISTRO DESDE FRONTEND ===")

# Simular los datos del formulario
form = {
    'email': 'guilles10@yahoo.com.ar',
    'nombre': 'Willy',
    'apellido': 'Test',
    'password': 'Test1234!'
}

# Simular headers del frontend
headers = {
    'Content-Type': 'application/json'
}

# Enviar registro
print(f"Enviando a: http://127.0.0.1:8000/api/auth/registro")
print(f"Datos: {form}")

r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=form, headers=headers, timeout=30)

print(f"\nRespuesta:")
print(f"Status: {r.status_code}")
print(f"Body: {r.text}")

# Verificar en BD
import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
c = conn.cursor()
c.execute("SELECT email, nombre, codigo_verificacion FROM usuarios WHERE email='guilles10@yahoo.com.ar'")
result = c.fetchone()
print(f"\nUsuario en BD: {result}")
conn.close()
