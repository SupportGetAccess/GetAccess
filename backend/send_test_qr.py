import qrcode
import base64
from io import BytesIO
import requests
import os

codigo = "GA-000012-001"

qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(codigo)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

buffer = BytesIO()
img.save(buffer, format="PNG")
img_base64 = base64.b64encode(buffer.getvalue()).decode()

print(f"Codigo QR: {codigo}")
print(f"Imagen base64 (primeros 100 chars): {img_base64[:100]}...")

email_html = f"""
<h2 style="color: #1f2937; text-align: center;">Codigo QR de Prueba</h2>
<p style="text-align: center;">Escanea este codigo con el scanner QR:</p>
<div style="text-align: center; margin: 20px 0;">
    <img src="data:image/png;base64,{img_base64}" alt="QR" style="width: 200px; height: 200px;">
</div>
<p style="text-align: center; font-size: 24px; font-weight: bold; color: #6366f1;">{codigo}</p>
<p style="text-align: center; color: #6b7280;">Evento: Festival de Musica 2026</p>
"""

html_content = f"""
<!DOCTYPE html>
<html>
<head></head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
        <div style="text-align: center; margin-bottom: 25px; padding-bottom: 20px; border-bottom: 2px solid #e5e7eb;">
            <h1 style="color: #6366f1; font-size: 28px; margin: 0; font-weight: bold;">Get Access - Scanner QR</h1>
        </div>
        {email_html}
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 25px 0;">
        <p style="color: #9ca3af; font-size: 12px; text-align: center;">Enviado automaticamente para pruebas</p>
    </div>
</body>
</html>
"""

brevo_api_key = os.environ.get("BREVO_API_KEY", "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")
brevo_sender_email = os.environ.get("BREVO_SENDER_EMAIL", "support.getaccess@gmail.com")
brevo_sender_name = "Get Access"

data = {
    "sender": {"name": brevo_sender_name, "email": brevo_sender_email},
    "to": [{"email": "guilles10@yahoo.com.ar"}],
    "subject": "Codigo QR de Prueba - Get Access Scanner",
    "htmlContent": html_content
}

try:
    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=data,
        headers={"api-key": brevo_api_key, "Content-Type": "application/json"},
        timeout=30
    )
    print(f"Email enviado! Status: {response.status_code}")
    if response.status_code == 201:
        print("Revisa tu casilla de guilles10@yahoo.com.ar")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error enviando email: {e}")
