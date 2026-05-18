import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
import uvicorn
import requests
import random
import string

app = FastAPI()

BREVO_API_KEY = "os.environ.get("BREVO_API_KEY")"
BREVO_SENDER_EMAIL = "a535a5001@smtp-brevo.com"
BREVO_SENDER_NAME = "Access ON"

class UserRegister(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str
    password: str

@app.post("/api/test/send-email")
def send_test_email(email: str):
    try:
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": email}],
            "subject": "Test Email",
            "htmlContent": "<h1>Test</h1><p>Email working</p>"
        }
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 201:
            return {"success": True, "message": "Email sent"}
        else:
            return {"success": False, "error": f"Status: {response.status_code}, Response: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)