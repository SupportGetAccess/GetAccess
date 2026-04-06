import requests

print("=== INICIANDO TEST ===")

# Registro
data = {'email': 'guilles10@yahoo.com.ar', 'nombre': 'Willy', 'apellido': 'Test', 'password': 'Test1234!'}
print(f"Enviando registro a: http://127.0.0.1:8000/api/auth/registro")
print(f"Datos: {data}")

r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=data, timeout=30)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")

# Verificar en BD
import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
c = conn.cursor()
c.execute("SELECT email, nombre, codigo_verificacion FROM usuarios WHERE email='guilles10@yahoo.com.ar'")
result = c.fetchone()
print(f"Usuario en BD: {result}")
conn.close()
