import requests
h = {'Origin': 'http://localhost:3000', 'Authorization': 'Bearer fake'}
r = requests.get('http://localhost:8000/api/transferencias/pendientes', headers=h)
print('Status:', r.status_code)
print('CORS:', r.headers.get('Access-Control-Allow-Origin'))
