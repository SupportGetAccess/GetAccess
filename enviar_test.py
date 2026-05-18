import os
import requests

api_key = 'os.environ.get("BREVO_API_KEY")'
codigo = '500969'

html = f"""<!DOCTYPE html>
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
                    <h2 style="margin: 0 0 20px 0; color: #f8fafc; font-size: 24px; font-weight: 600;">¡Bienvenido Willy!</h2>
                    <p style="margin: 0 0 30px 0; color: #94a3b8; font-size: 16px; line-height: 1.6;">Gracias por registrarte en Access ON. Para completar tu registro, ingresa el siguiente código de verificación:</p>
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr><td align="center" style="padding: 20px; background: rgba(99, 102, 241, 0.1); border-radius: 12px; border: 2px solid #6366f1;">
                            <span style="color: #6366f1; font-size: 14px; font-weight: 600; letter-spacing: 2px;">CÓDIGO DE VERIFICACIÓN</span>
                            <br><br>
                            <span style="color: #f8fafc; font-size: 36px; font-weight: 800; letter-spacing: 8px;">{codigo}</span>
                        </td></tr>
                    </table>
                    <p style="margin: 30px 0 0 0; color: #64748b; font-size: 14px;">Este código vence en 24 horas.</p>
                </td></tr>
                <tr><td style="background: #0a0a1a; padding: 25px 30px; text-align: center;">
                    <p style="margin: 0; color: #64748b; font-size: 12px;">© 2026 Access ON</p>
                </td></tr>
            </table>
        </td></tr>
    </table>
</body>
</html>"""

r = requests.post('https://api.brevo.com/v3/smtp/email', 
    json={'sender':{'name':'Access ON','email':'aantoniaa1982@gmail.com'},
          'to':[{'email':'guilles10@yahoo.com.ar'}],
          'subject':'Código de verificación - Access ON',
          'htmlContent':html},
    headers={'api-key':api_key,'Content-Type':'application/json'}, timeout=20)
print(f'Status: {r.status_code}')
print(r.text[:200])
