import os
os.environ["SUPABASE_URI"] = "postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"

import sys
sys.path.insert(0, 'C:/Users/guill/eventos_tickets_full/backend')

from main import app, get_db, SECRET_KEY
from fastapi.testclient import TestClient
import jwt

# Crear token
token = jwt.encode({"sub": "1"}, SECRET_KEY, algorithm="ALGORITHM")

# Hacer request
client = TestClient(app)
response = client.get(
    "/api/analytics/todos",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")