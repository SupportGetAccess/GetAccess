import requests

api_key = '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'
codigo = '578169'

html = f"""<!DOCTYPE html><html><body style="background:#0a0a1a;color:#fff;padding:40px;font-family:Segoe UI;text-align:center;">
<h1 style="background:linear-gradient(135deg,#6366f1,#ec4899);padding:20px;border-radius:10px;">ACCESS ON</h1>
<h2>¡Bienvenido Willy!</h2>
<p>Tu código de verificación:</p>
<div style="background:rgba(99,102,241,0.2);border:2px solid #6366f1;padding:20px;border-radius:10px;display:inline-block;">
<span style="font-size:40px;font-weight:bold;letter-spacing:10px;">{codigo}</span>
</div>
</body></html>"""

r = requests.post('https://api.brevo.com/v3/smtp/email', 
    json={'sender':{'name':'Access ON','email':'aantoniaa1982@gmail.com'},
          'to':[{'email':'guilles10@yahoo.com.ar'}],
          'subject':'Código de verificación - Access ON',
          'htmlContent':html},
    headers={'api-key':api_key,'Content-Type':'application/json'}, timeout=20)
print(f'Email: {r.status_code}')
