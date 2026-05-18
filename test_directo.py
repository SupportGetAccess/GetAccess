import os
import requests

# Simular lo que hace la función
email = "guilles10@yahoo.com.ar"
codigo = "123456"
nombre = "Willy"

BREVO_API_KEY = "os.environ.get("BREVO_API_KEY")"
BREVO_SENDER_EMAIL = "aantoniaa1982@gmail.com"
BREVO_SENDER_NAME = "Access ON"

url = "https://api.brevo.com/v3/smtp/email"
headers = {
    "api-key": BREVO_API_KEY,
    "Content-Type": "application/json"
}

nombre_display = nombre if nombre else "Usuario"

html_content = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; background: #0a0a1a;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background: #0a0a1a; padding: 40px 20px;">
        <tr><td align="center">
            <table width="600" cellpadding="0" cellspacing="0" style="background: #12122a; border-radius: 20px; overflow: hidden;">
                <tr><td style="background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%); padding: 30px; text-align: center;">
                    <h1 style="margin: 0; color: white; font-size: 32px; font-weight: 800;">ACCESS ON</h1>
                    <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.8); font-size: 14px;">Tu puerta a los mejores eventos</p>
                </td></tr>
                <tr><td style="padding: 40px 30px;">
                    <h2 style="margin: 0 0 20px 0; color: #f8fafc; font-size: 24px; font-weight: 600;">Bienvenido """ + nombre_display + """!</h2>
                    <p style="margin: 0 0 30px 0; color: #94a3b8; font-size: 16px;">Gracias por registrarte en Access ON. Tu codigo de verificacion:</p>
                    <div style="background:rgba(99,102,241,0.1);border:2px solid #6366f1;border-radius:12px;padding:20px;text-align:center;">
                        <span style="color:#6366f1;font-size:14px;font-weight:600;">CODIGO</span><br><br>
                        <span style="color:#f8fafc;font-size:36px;font-weight:800;letter-spacing:8px;">""" + codigo + """</span>
                    </div>
                </td></tr>
                <tr><td style="background:#0a0a1a;padding:25px;text-align:center;">
                    <p style="margin:0;color:#64748b;font-size:12px;">2026 Access ON</p>
                </td></tr>
            </table>
        </td></tr>
    </table>
</body>
</html>"""

data = {
    "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
    "to": [{"email": email}],
    "subject": "Codigo de verificacion - Access ON",
    "htmlContent": html_content
}

print("Enviando...")
r = requests.post(url, json=data, headers=headers, timeout=30)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:100]}")
