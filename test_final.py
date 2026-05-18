import os
import requests
import sqlite3

# Eliminar usuario
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
conn.execute("DELETE FROM usuarios WHERE email='guilles10@yahoo.com.ar'")
conn.commit()
conn.close()

# Registro
form = {'email': 'guilles10@yahoo.com.ar', 'nombre': 'Willy', 'apellido': 'Test', 'password': 'Test1234!'}
r = requests.post('http://127.0.0.1:8000/api/auth/registro', json=form, timeout=30)
print(f'Registro: {r.status_code}')

# Verificar código
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
c = conn.cursor()
c.execute("SELECT codigo_verificacion FROM usuarios WHERE email='guilles10@yahoo.com.ar'")
codigo = c.fetchone()[0]
print(f'Código: {codigo}')
conn.close()

# Enviar email directo
import requests as req
api_key = 'os.environ.get("BREVO_API_KEY")'

html = f"""<!DOCTYPE html><html><body style="background:#0a0a1a;color:#fff;padding:40px;text-align:center;font-family:Segoe UI;">
<h1 style="background:linear-gradient(135deg,#6366f1,#ec4899);padding:20px;border-radius:10px;">ACCESS ON</h1>
<h2>¡Bienvenido Willy!</h2>
<p>Tu código de verificación:</p>
<div style="background:rgba(99,102,241,0.2);border:2px solid #6366f1;padding:20px;border-radius:10px;display:inline-block;">
<span style="font-size:40px;font-weight:bold;letter-spacing:10px;">{codigo}</span>
</div>
</body></html>"""

r = req.post('https://api.brevo.com/v3/smtp/email', 
    json={'sender':{'name':'Access ON','email':'aantoniaa1982@gmail.com'},
          'to':[{'email':'guilles10@yahoo.com.ar'}],
          'subject':'Código de verificación - Access ON',
          'htmlContent':html},
    headers={'api-key':api_key,'Content-Type':'application/json'}, timeout=20)
print(f'Email enviado: {r.status_code}')
