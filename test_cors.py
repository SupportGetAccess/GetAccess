import requests
h = {'Origin': 'http://localhost:3000'}
r = requests.get('http://localhost:8000/api/entradas/', headers=h)
print('CORS:', r.headers.get('Access-Control-Allow-Origin'))
