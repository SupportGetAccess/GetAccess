import sqlite3
import qrcode
import requests
import os
import base64
import uuid
import bcrypt

BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "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")
BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL", "support.getaccess@gmail.com")
BREVO_SENDER_NAME = "Get Access"

conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
cur = conn.cursor()

# Verificar si hay entradas
cur.execute('SELECT COUNT(*) FROM entradas')
count = cur.fetchone()[0]
print(f"Entradas actuales: {count}")

# Obtener o crear usuario
cur.execute("SELECT id FROM usuarios WHERE email = 'guilles10@yahoo.com.ar'")
user_row = cur.fetchone()
if user_row:
    usuario_id = user_row[0]
    print(f"Usuario existente ID: {usuario_id}")
else:
    password = 'guille123'
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cur.execute('INSERT INTO usuarios (email, password, nombre, apellido, verificado, rol) VALUES (?, ?, ?, ?, ?, ?)',
        ('guilles10@yahoo.com.ar', hashed, 'Guille', 'Apellido', 1, 'usuario'))
    usuario_id = cur.lastrowid
    print(f"Usuario creado ID: {usuario_id}")

# Obtener evento
cur.execute("SELECT id FROM eventos WHERE nombre LIKE '%Festival%'")
evento_id = cur.fetchone()[0]
print(f"Evento ID: {evento_id}")

# Generar código único
codigo = f'GA-{uuid.uuid4().hex[:12].upper()}'
print(f"Código: {codigo}")

# Crear entrada
cur.execute('''INSERT INTO entradas (evento_id, usuario_id, cantidad, total, estado, preference_id, payment_id, creado_en, usada)
               VALUES (?, ?, 1, 5000, 'pagada', ?, NULL, datetime('now'), 0)''', 
            (evento_id, usuario_id, codigo))
entrada_id = cur.lastrowid
print(f"Entrada creada ID: {entrada_id}")

conn.commit()

# Obtener datos para el email
cur.execute('''
    SELECT e.id, e.preference_id, e.cantidad, e.total, ev.nombre, ev.fecha, ev.lugar, u.email, u.nombre
    FROM entradas e
    JOIN eventos ev ON e.evento_id = ev.id
    JOIN usuarios u ON e.usuario_id = u.id
    WHERE e.id = ?
''', (entrada_id,))
row = cur.fetchone()

entrada_id = row[0]
codigo = row[1]
cantidad = row[2]
total = row[3]
evento = row[4]
fecha = row[5]
lugar = row[6]
email = row[7]
nombre = row[8]

print(f"\nDatos del ticket:")
print(f"  ID: {entrada_id}")
print(f"  Código: {codigo}")
print(f"  Evento: {evento}")
print(f"  Email: {email}")

# Generar QR
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(codigo)
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')

qr_path = 'C:/Users/guill/eventos_tickets_full/backend/ticket_qr.png'
img.save(qr_path)

with open(qr_path, 'rb') as f:
    qr_base64 = base64.b64encode(f.read()).decode('utf-8')

# Enviar email
url = "https://api.brevo.com/v3/smtp/email"
headers = {"api-key": BREVO_API_KEY, "Content-Type": "application/json"}

html_content = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #6366f1, #ec4899); padding: 30px; text-align: center;">
        <h1 style="color: white; margin: 0;">🎫 Get Access</h1>
    </div>
    <div style="padding: 30px; background: #f8fafc;">
        <h2 style="color: #1e293b;">¡Gracias por tu compra!</h2>
        <p>Tu entrada para <strong>{evento}</strong> está confirmada.</p>
        
        <div style="background: white; padding: 20px; border-radius: 12px; text-align: center; margin: 20px 0;">
            <img src="data:image/png;base64,{qr_base64}" alt="QR Code" style="width: 200px;">
            <p style="font-family: monospace; font-size: 18px; margin-top: 10px;"><strong>{codigo}</strong></p>
        </div>
        
        <div style="background: white; padding: 20px; border-radius: 12px;">
            <p><strong>📅 Fecha:</strong> {fecha}</p>
            <p><strong>📍 Lugar:</strong> {lugar}</p>
            <p><strong>🎫 Cantidad:</strong> {cantidad}</p>
            <p><strong>💰 Total:</strong> ${total}</p>
        </div>
        
        <p style="color: #64748b; font-size: 12px; margin-top: 20px;">
            Presenta este código QR en la entrada del evento.
        </p>
    </div>
</body>
</html>
"""

payload = {
    "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
    "to": [{"email": email, "name": nombre}],
    "subject": f"🎫 Tu entrada para {evento}",
    "htmlContent": html_content
}

print("\nEnviando email...")
response = requests.post(url, json=payload, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

if os.path.exists(qr_path):
    os.remove(qr_path)
conn.close()
print("\n¡Listo! Ticket enviado a guilles10@yahoo.com.ar")
