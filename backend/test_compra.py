import os
os.environ["RENDER"] = "1"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
import random
import requests
import config

conn = psycopg2.connect(config.DATABASE_URL)
conn.autocommit = True
cur = conn.cursor(cursor_factory=RealDictCursor)

cur.execute("SELECT id, email, nombre, apellido FROM usuarios WHERE email = %s", ('aantoniaa1982@gmail.com',))
user = cur.fetchone()
if not user:
    print("Usuario no encontrado")
    exit()

usuario_id = user['id']
print(f"Usuario: {user['nombre']} {user['apellido']} ({user['email']})")

cur.execute("SELECT id, nombre, fecha, lugar, precio FROM eventos WHERE id = 9")
evento = cur.fetchone()
print(f"Evento: {evento['nombre']} - ${evento['precio']}")

codigo = f"GA-{random.randint(100000, 999999)}"
print(f"Codigo: {codigo}")

cur.execute('''INSERT INTO entradas (evento_id, usuario_id, cantidad, total, estado, preference_id, creada_en, usada, transferida)
               VALUES (%s, %s, %s, %s, %s, %s, NOW(), 0, 0) RETURNING id''',
            (evento['id'], usuario_id, 1, evento['precio'], 'pagada', codigo))
entrada_id = cur.fetchone()['id']
print(f"Entrada creada ID: {entrada_id}")

import datetime

QUICKCHART_URL = "https://quickchart.io/qr"
qr_url = f"{QUICKCHART_URL}?size=300x300&text={codigo}"

fecha = evento['fecha']
fecha_formateada = str(fecha)
try:
    fecha_dt = datetime.datetime.strptime(str(fecha).split('.')[0], "%Y-%m-%d %H:%M:%S")
    fecha_formateada = fecha_dt.strftime("%d de %B de %Y - %H:%M")
except:
    try:
        fecha_dt = datetime.datetime.strptime(str(fecha), "%Y-%m-%d")
        fecha_formateada = fecha_dt.strftime("%d de %B de %Y")
    except:
        pass

email_content = f"""
<h2 style="color: #1f2937; text-align: center; margin-bottom: 15px;">¡Hola {user['nombre']} {user['apellido']}!</h2>
<p style="color: #4b5563; font-size: 16px; line-height: 1.6; text-align: center;">
    Tu entrada para <strong>{evento['nombre']}</strong>
</p>
<div style="text-align: center; margin: 25px 0;">
    <p style="color: #6366f1; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 15px 0;">Escaneá este código en la entrada</p>
    <div style="background-color: #ffffff; display: inline-block; padding: 15px; border-radius: 12px; border: 2px solid #6366f1;">
        <img src="{qr_url}" alt="Código QR" style="width: 180px; height: 180px; display: block;">
    </div>
    <p style="color: #6366f1; font-size: 22px; font-weight: bold; margin: 15px 0 0 0; letter-spacing: 3px;">{codigo}</p>
</div>
<div style="background-color: #f3f4f6; border-radius: 8px; padding: 20px; margin: 25px 0;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                <strong style="color: #4b5563;">📅 Fecha:</strong>
            </td>
            <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                {fecha_formateada}
            </td>
        </tr>
        <tr>
            <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                <strong style="color: #4b5563;">📍 Lugar:</strong>
            </td>
            <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                {evento['lugar']}
            </td>
        </tr>
        <tr>
            <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                <strong style="color: #4b5563;">🎟️ Entradas:</strong>
            </td>
            <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                1 entrada
            </td>
        </tr>
        <tr>
            <td style="padding: 10px 0;">
                <strong style="color: #4b5563;">💵 Total:</strong>
            </td>
            <td style="padding: 10px 0; text-align: right; color: #10b981; font-weight: 800; font-size: 18px;">
                ${evento['precio']:,.2f}
            </td>
        </tr>
    </table>
</div>
<div style="text-align: center; padding: 12px; background-color: #dcfce7; border-radius: 8px; margin: 20px 0;">
    <p style="color: #166534; margin: 0; font-weight: 700; font-size: 16px;">✅ PAGADA</p>
</div>
<p style="color: #6b7280; font-size: 14px; text-align: center;">
    Presentá el código QR en la entrada del evento o mostrá este email en tu celular.
</p>
"""

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
        <div style="text-align: center; margin-bottom: 25px; padding-bottom: 20px; border-bottom: 2px solid #e5e7eb;">
            <h1 style="color: #6366f1; font-size: 28px; margin: 0; font-weight: bold;">🎫 Get Access</h1>
        </div>
        {email_content}
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 25px 0;">
        <p style="color: #9ca3af; font-size: 12px; text-align: center;">© 2026 Get Access - Todos los derechos reservados</p>
    </div>
</body>
</html>"""

payload = {
    "sender": {"name": config.BREVO_SENDER_NAME, "email": config.BREVO_SENDER_EMAIL},
    "to": [{"email": user['email'], "name": user['nombre']}],
    "subject": f"🎫 Tu entrada para {evento['nombre']} - Get Access",
    "htmlContent": html_content
}

print("\nEnviando email...")
response = requests.post(config.BREVO_API_URL, json=payload, headers={"api-key": config.BREVO_API_KEY, "Content-Type": "application/json"})
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

cur.close()
conn.close()

print(f"\nTicket enviado a {user['email']}")