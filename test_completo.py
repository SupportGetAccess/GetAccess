import os
import requests
import sqlite3
import json

# Eliminar usuario
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
conn.execute("DELETE FROM usuarios WHERE email='guilles10@yahoo.com.ar'")
conn.commit()
conn.close()

# Registro
data = {'email': 'guilles10@yahoo.com.ar', 'nombre': 'Willy', 'apellido': 'Test', 'password': 'Test1234!'}
r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=data, timeout=30)
print(f'Registro: {r.status_code}')
print(r.text)

# Verificar
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
c = conn.cursor()
c.execute("SELECT email, nombre, codigo_verificacion FROM usuarios WHERE email='guilles10@yahoo.com.ar'")
print(f'Usuario: {c.fetchone()}')
conn.close()

# Ahora enviar email directamente
import requests

api_key = 'os.environ.get("BREVO_API_KEY")'
codigo = '999999'

html = f"""<!DOCTYPE html><html><body style="background:#0a0a1a;color:#fff;padding:40px;text-align:center;">
<h1>ACCESS ON</h1>
<h2>Código: {codigo}</h2>
</body></html>"""

r = requests.post('https://api.brevo.com/v3/smtp/email', 
    json={'sender':{'name':'Access ON','email':'aantoniaa1982@gmail.com'},
          'to':[{'email':'guilles10@yahoo.com.ar'}],
          'subject':'Test',
          'htmlContent':html},
    headers={'api-key':api_key,'Content-Type':'application/json'}, timeout=20)
print(f'Email directo: {r.status_code}')
