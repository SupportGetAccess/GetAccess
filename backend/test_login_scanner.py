import requests

url = "https://getaccess-d3um.onrender.com/api/auth/login"
data = {"email": "aantoniaa1982@gmail.com", "password": "guille123"}

res = requests.post(url, json=data, headers={"Content-Type": "application/json"})
print(f"Status: {res.status_code}")
print(f"Headers: {res.headers}")
print(f"Response: {res.text}")

# También probar con admin
data2 = {"email": "admin@getaccess.com", "password": "admin123"}
res2 = requests.post(url, json=data2)
print(f"\nAdmin - Status: {res2.status_code}")
print(f"Admin - Response: {res2.text}")