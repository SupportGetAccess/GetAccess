import requests

api_key = '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'

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
