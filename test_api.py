import requests

api_key = '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'

print("Enviando email...")

url = 'https://api.brevo.com/v3/smtp/email'
headers = {'api-key': api_key, 'Content-Type': 'application/json'}

# Usar el email del usuario como sender
data = {
    'sender': {'name': 'Access ON', 'email': 'aantoniaa1982@gmail.com'},
    'to': [{'email': 'guilles10@yahoo.com.ar'}],
    'subject': 'Test Access ON',
    'textContent': 'Test email'
}

try:
    r = requests.post(url, json=data, headers=headers, timeout=30)
    print(f'Status: {r.status_code}')
    print(f'Response: {r.text}')
except Exception as e:
    print(f'Error: {e}')
