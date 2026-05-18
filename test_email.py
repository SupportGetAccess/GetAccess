import os
import requests

api_key = 'os.environ.get("BREVO_API_KEY")'

html = """<!DOCTYPE html><html><body style="background:#0a0a1a;color:#fff;padding:40px;font-family:Segoe UI;text-align:center;">
<h1>ACCESS ON</h1>
<h2>Codigo: 842379</h2>
</body></html>"""

r = requests.post('https://api.brevo.com/v3/smtp/email', 
    json={'sender':{'name':'Access ON','email':'aantoniaa1982@gmail.com'},
          'to':[{'email':'guilles10@yahoo.com.ar'}],
          'subject':'Test',
          'htmlContent':html},
    headers={'api-key':api_key,'Content-Type':'application/json'}, timeout=20)
print(f'Email: {r.status_code}')
print(r.text[:100])
