import os
import requests

api_key = 'os.environ.get("BREVO_API_KEY")'
codigo = '322603'

html = """<!DOCTYPE html>
<html><body style="margin:0; font-family:Segoe UI; background:#0a0a1a;">
<table width="100%" style="background:#0a0a1a;padding:40px;"><tr><td align="center">
<table width="600" style="background:#12122a;border-radius:20px;">
<tr><td style="background:linear-gradient(135deg,#6366f1,#ec4899);padding:30px;text-align:center;">
<h1 style="color:white;margin:0;">ACCESS ON</h1></td></tr>
<tr><td style="padding:40px;">
<h2 style="color:#f8fafc;">¡Bienvenido Willy!</h2>
<p style="color:#94a3b8;">Tu código de verificación:</p>
<div style="background:rgba(99,102,241,0.1);border:2px solid #6366f1;border-radius:12px;padding:20px;text-align:center;">
<span style="color:#6366f1;font-size:14px;">CÓDIGO</span><br><br>
<span style="color:#f8fafc;font-size:36px;font-weight:800;letter-spacing:8px;">""" + codigo + """</span>
</div></td></tr></table></td></tr></table></body></html>"""

r = requests.post('https://api.brevo.com/v3/smtp/email', 
    json={'sender':{'name':'Access ON','email':'aantoniaa1982@gmail.com'},
          'to':[{'email':'guilles10@yahoo.com.ar'}],
          'subject':'Código de verificación - Access ON',
          'htmlContent':html},
    headers={'api-key':api_key,'Content-Type':'application/json'}, timeout=20)
print(f'Status: {r.status_code}')
print(r.text[:300])
