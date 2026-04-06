import requests

api_key = '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'

# Test a Gmail
r = requests.post('https://api.brevo.com/v3/smtp/email', 
    json={'sender':{'name':'Access ON','email':'aantoniaa1982@gmail.com'},
          'to':[{'email':'aantoniaa1982@gmail.com'}],
          'subject':'Test a Gmail',
          'textContent':'Test'},
    headers={'api-key':api_key,'Content-Type':'application/json'}, timeout=20)
print(f'Gmail: {r.status_code}')
print(r.text[:100])
