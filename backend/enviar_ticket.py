import sqlite3
import qrcode
import requests
import os
import base64
import sys
from pathlib import Path

# Importar configuración centralizada
sys.path.insert(0, str(Path(__file__).parent))
try:
    import config
    BREVO_API_URL = config.BREVO_API_URL
    BREVO_API_KEY = config.BREVO_API_KEY
    BREVO_SENDER_EMAIL = config.BREVO_SENDER_EMAIL
    BREVO_SENDER_NAME = config.BREVO_SENDER_NAME
except ImportError:
    BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
    BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "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")
    BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL", "soporte@getaccess.com.ar")
    BREVO_SENDER_NAME = "Get Access"

conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
cur = conn.cursor()

# Query simple
cur.execute('''
    SELECT e.id, e.preference_id, e.cantidad, e.total, ev.nombre, ev.fecha, ev.lugar, u.email, u.nombre
    FROM entradas e
    JOIN eventos ev ON e.evento_id = ev.id
    JOIN usuarios u ON e.usuario_id = u.id
    WHERE e.id = 1
''')
row = cur.fetchone()

if row is None:
    print("No se encontró la entrada")
    exit(1)

print("Row:", row)

entrada_id = row[0]
codigo = row[1]
cantidad = row[2]
total = row[3]
evento = row[4]
fecha = row[5]
lugar = row[6]
email = row[7]
nombre = row[8]

print(f"Entrada ID: {entrada_id}")
print(f"Codigo: {codigo}")
print(f"Evento: {evento}")
print(f"Email: {email}")

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
url = BREVO_API_URL
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
