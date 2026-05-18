import os
import requests

api_key = 'os.environ.get("BREVO_API_KEY")'

url = 'https://api.brevo.com/v3/smtp/email'
headers = {'api-key': api_key, 'Content-Type': 'application/json'}
data = {
    'sender': {'name': 'Access ON', 'email': 'aantoniaa1982@gmail.com'},
    'to': [{'email': 'guilles10@yahoo.com.ar'}],
    'subject': 'Test directo',
    'textContent': 'Test directo'
}

r = requests.post(url, json=data, headers=headers, timeout=20)
print(f'Status: {r.status_code}')
print(f'Response: {r.text}')
