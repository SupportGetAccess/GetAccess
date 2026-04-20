import os
os.environ["RENDER"] = "1"
import requests
import config

url = f"{config.PRODUCTION_URL}/api/validar-entrada"

# Login con admin
login = requests.post(f"{config.PRODUCTION_URL}/api/auth/login", json={"email": "admin@getaccess.com", "password": "admin123"})
print(f"Login: {login.status_code} - {login.text[:200]}")

if login.status_code == 200:
    token = login.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    response = requests.post(url, json={"codigo": "GA-Y6VR7DFSMA", "evento_id": 9}, headers=headers)
    print(f"Validar: {response.status_code}")
    print(f"Response: {response.text}")