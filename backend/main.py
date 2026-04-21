from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from collections import defaultdict
from datetime import datetime, timedelta
import uvicorn
import sqlite3
import psycopg2
import bcrypt
from jose import jwt
import datetime
import requests
import random
import string
import hashlib
import hmac
import qrcode
import io
import base64
import os
from pathlib import Path

# Importar configuración centralizada
try:
    import config
    SECRET_KEY = config.SECRET_KEY
    ALGORITHM = config.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
    ALLOWED_ORIGINS = config.ALLOWED_ORIGINS
    BREVO_API_KEY = config.BREVO_API_KEY
    BREVO_SENDER_EMAIL = config.BREVO_SENDER_EMAIL
    BREVO_SENDER_NAME = config.BREVO_SENDER_NAME
    DATABASE_URL = config.DATABASE_URL
    RATE_LIMIT_WINDOW = config.RATE_LIMIT_WINDOW
    RATE_LIMIT_MAX = config.RATE_LIMIT_MAX
    PRODUCTION_URL = config.PRODUCTION_URL
    RENDER_URL = config.RENDER_URL
    DEV_URLS = config.DEV_URLS
    BREVO_API_URL = config.BREVO_API_URL
    MERCADOPAGO_API_URL = config.MERCADOPAGO_API_URL
    MERCADOPAGO_ACCESS_TOKEN = config.MERCADOPAGO_ACCESS_TOKEN
    QUICKCHART_URL = config.QUICKCHART_URL
    EMAIL_LOGO_URL = config.EMAIL_LOGO_URL
    DEFAULT_EVENT_IMAGES = config.DEFAULT_EVENT_IMAGES
    ADMIN_SECRET = config.ADMIN_SECRET
except ImportError:
    # Fallback si no existe config.py
    SECRET_KEY = os.environ.get("SECRET_KEY", "access_on_super_secret_key_2026_fallback")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000,https://192.168.1.40:3443").split(",")
    BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "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")
    BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL", "soporte@getaccess.com.ar")
    BREVO_SENDER_NAME = "Get Access"
    DATABASE_URL = "access_on.db"
    RATE_LIMIT_WINDOW = 60
    RATE_LIMIT_MAX = 100
    PRODUCTION_URL = "https://getaccess.com.ar"
    RENDER_URL = "https://getaccess-d3um.onrender.com"
    DEV_URLS = ["http://localhost:3000", "https://192.168.1.40:3443"]
    BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
    MERCADOPAGO_API_URL = "https://api.mercadopago.com"
    MERCADOPAGO_ACCESS_TOKEN = "APP_USR-2888302331727804-031609-eb4c51fc6c1654d701d4a5f3b24fbcd7-1921694"
    QUICKCHART_URL = "https://quickchart.io/qr"
    EMAIL_LOGO_URL = "https://getaccess.now.sh/logo.png"
    DEFAULT_EVENT_IMAGES = [
        "https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=800",
        "https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=800",
        "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800",
        "https://images.unsplash.com/photo-1527224857830-43a7acc85260?w=800",
        "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800",
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800",
        "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800",
        "https://images.unsplash.com/photo-1598387993441-a364f854c3e1?w=800",
    ]

# Rate Limiting - tabla en base de datos
RATE_LIMIT_WINDOW = 60  # segundos
RATE_LIMIT_MAX = 100    # max requests por ventana

# Logging de seguridad
import logging
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - SECURITY - %(message)s'))
security_logger.addHandler(handler)

def log_security(evento: str, detalles: str = ""):
    """Registrar eventos de seguridad"""
    security_logger.info(f"{evento}: {detalles}")

def get_client_ip(request: Request) -> str:
    """Obtener IP real del cliente"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

def registrar_visita(ip: str):
    """Registrar visita en la base de datos"""
    try:
        if "postgresql" in DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO visitas (ip, fecha, contador)
                VALUES (%s, CURRENT_DATE, 1)
                ON CONFLICT (ip, fecha) DO UPDATE SET contador = visitas.contador + 1
            """, (ip,))
            conn.commit()
            cur.close()
            conn.close()
        else:
            conn = sqlite3.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("SELECT contador FROM visitas WHERE ip = ? AND fecha = date('now')", (ip,))
            row = cur.fetchone()
            if row:
                conn.execute("UPDATE visitas SET contador = contador + 1 WHERE ip = ? AND fecha = date('now')", (ip,))
            else:
                conn.execute("INSERT INTO visitas (ip, fecha, contador) VALUES (?, date('now'), 1)", (ip,))
            conn.commit()
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Error registrando visita: {e}")

# Brute-force protection
BRUTE_FORCE_MAX = 5  # max intentos fallidos
BRUTE_FORCE_WINDOW = 300  # 5 minutos de bloqueo

def init_brute_force_table(db):
    """Inicializa la tabla de protección brute-force"""
    if is_postgres():
        db.execute("""
            CREATE TABLE IF NOT EXISTS brute_force_protection (
                email VARCHAR(255) PRIMARY KEY,
                intentos INTEGER DEFAULT 0,
                bloqueado_hasta TIMESTAMP,
                ultimo_intento TIMESTAMP
            )
        """)
    else:
        db.execute("""
            CREATE TABLE IF NOT EXISTS brute_force_protection (
                email TEXT PRIMARY KEY,
                intentos INTEGER DEFAULT 0,
                bloqueado_hasta TEXT,
                ultimo_intento TEXT
            )
        """)
    db.commit()

def check_brute_force(email: str, db, es_login: bool = True) -> tuple[bool, str]:
    """Verifica y maneja protección brute-force"""
    # Crear tabla si no existe
    try:
        if is_postgres():
            db.execute("""
                CREATE TABLE IF NOT EXISTS brute_force_protection (
                    email VARCHAR(255) PRIMARY KEY,
                    intentos INTEGER DEFAULT 0,
                    bloqueado_hasta TIMESTAMP,
                    ultimo_intento TIMESTAMP
                )
            """)
        else:
            db.execute("""
                CREATE TABLE IF NOT EXISTS brute_force_protection (
                    email TEXT PRIMARY KEY,
                    intentos INTEGER DEFAULT 0,
                    bloqueado_hasta TEXT,
                    ultimo_intento TEXT
                )
            """)
        db.commit()
    except:
        pass  # Tabla ya existe
    
    now = datetime.datetime.now()
    
    cursor = db.execute("SELECT intentos, bloqueado_hasta, ultimo_intento FROM brute_force_protection WHERE email = ?", (email,))
    row = cursor.fetchone()
    
    if row:
        intentos, bloqueado_hasta, ultimo_intento = row
        
        # Verificar si está bloqueado
        if bloqueado_hasta:
            if is_postgres():
                if isinstance(bloqueado_hasta, datetime.datetime) and bloqueado_hasta > now:
                    return False, f"Cuenta bloqueada. Intenta más tarde."
            else:
                if bloqueado_hasta and datetime.datetime.fromisoformat(bloqueado_hasta) > now:
                    return False, f"Cuenta bloqueada. Intenta más tarde."
        
        # Resetear intentos si pasó el tiempo de ventana
        if ultimo_intento:
            if is_postgres():
                if isinstance(ultimo_intento, datetime.datetime):
                    tiempo_pasado = (now - ultimo_intento).total_seconds()
                else:
                    tiempo_pasado = 300
            else:
                tiempo_pasado = (now - datetime.datetime.fromisoformat(ultimo_intento)).total_seconds() if ultimo_intento else 300
            
            if tiempo_pasado > BRUTE_FORCE_WINDOW:
                intentos = 0
    
    return True, ""

def record_brute_force_attempt(email: str, exitoso: bool, db):
    """Registrar intento de login"""
    now = datetime.datetime.now()
    
    cursor = db.execute("SELECT intentos FROM brute_force_protection WHERE email = ?", (email,))
    row = cursor.fetchone()
    
    if exitoso:
        # Login exitoso - resetear intentos
        if row:
            db.execute("DELETE FROM brute_force_protection WHERE email = ?", (email,))
    else:
        # Login fallido - incrementar contador
        intentos = (row[0] + 1) if row else 1
        
        if intentos >= BRUTE_FORCE_MAX:
            bloqueado_hasta = now + datetime.timedelta(minutes=15)
            if is_postgres():
                db.execute("""
                    INSERT INTO brute_force_protection (email, intentos, bloqueado_hasta, ultimo_intento)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (email) DO UPDATE SET intentos = EXCLUDED.intentos, bloqueado_hasta = EXCLUDED.bloqueado_hasta, ultimo_intento = EXCLUDED.ultimo_intento
                """, (email, intentos, bloqueado_hasta, now))
            else:
                db.execute("""
                    INSERT OR REPLACE INTO brute_force_protection (email, intentos, bloqueado_hasta, ultimo_intento)
                    VALUES (?, ?, ?, ?)
                """, (email, intentos, bloqueado_hasta.isoformat(), now.isoformat()))
            log_security("BRUTE_FORCE_BLOCKED", f"Email: {email}, Intentos: {intentos}")
        else:
            if is_postgres():
                db.execute("""
                    INSERT INTO brute_force_protection (email, intentos, ultimo_intento)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (email) DO UPDATE SET intentos = EXCLUDED.intentos, ultimo_intento = EXCLUDED.ultimo_intento
                """, (email, intentos, now))
            else:
                db.execute("""
                    INSERT OR REPLACE INTO brute_force_protection (email, intentos, ultimo_intento)
                    VALUES (?, ?, ?)
                """, (email, intentos, now.isoformat()))
            
            log_security("LOGIN_FAILED", f"Email: {email}, Intento: {intentos}")
    
    db.commit()

def init_rate_limit_table(db):
    """Inicializa la tabla de rate limiting"""
    if is_postgres():
        db.execute("""
            CREATE TABLE IF NOT EXISTS rate_limits (
                client_id VARCHAR(255) PRIMARY KEY,
                requests TIMESTAMP[],
                window_seconds INTEGER DEFAULT 60
            )
        """)
    else:
        db.execute("""
            CREATE TABLE IF NOT EXISTS rate_limits (
                client_id TEXT PRIMARY KEY,
                requests TEXT,
                window_seconds INTEGER DEFAULT 60
            )
        """)
    db.commit()

def check_rate_limit(client_id: str, db) -> bool:
    """Rate limiting con persistencia en base de datos"""
    # Crear tabla si no existe
    try:
        if is_postgres():
            db.execute("""
                CREATE TABLE IF NOT EXISTS rate_limits (
                    client_id VARCHAR(255) PRIMARY KEY,
                    requests TIMESTAMP[],
                    window_seconds INTEGER DEFAULT 60
                )
            """)
        else:
            db.execute("""
                CREATE TABLE IF NOT EXISTS rate_limits (
                    client_id TEXT PRIMARY KEY,
                    requests TEXT,
                    window_seconds INTEGER DEFAULT 60
                )
            """)
        db.commit()
    except:
        pass  # Tabla ya existe
    
    now = datetime.datetime.now()
    
    cursor = db.execute("SELECT requests, window_seconds FROM rate_limits WHERE client_id = ?", (client_id,))
    row = cursor.fetchone()
    
    window = RATE_LIMIT_WINDOW
    requests_times = []
    
    if row:
        window = row[1] or RATE_LIMIT_WINDOW
        req_str = row[0]
        if req_str:
            if is_postgres():
                requests_times = req_str if isinstance(req_str, list) else []
            else:
                requests_times = [datetime.datetime.fromisoformat(t) for t in req_str.split(',')] if req_str else []
    
    # Filtrar requests dentro de la ventana
    cutoff = now - datetime.timedelta(seconds=window)
    requests_times = [t for t in requests_times if t > cutoff]
    
    if len(requests_times) >= RATE_LIMIT_MAX:
        return False
    
    requests_times.append(now)
    
    # Guardar en BD
    if is_postgres():
        db.execute("""
            INSERT INTO rate_limits (client_id, requests, window_seconds)
            VALUES (%s, %s, %s)
            ON CONFLICT (client_id) DO UPDATE SET requests = EXCLUDED.requests, window_seconds = EXCLUDED.window_seconds
        """, (client_id, requests_times, window))
    else:
        req_str = ','.join([t.isoformat() for t in requests_times])
        db.execute("""
            INSERT OR REPLACE INTO rate_limits (client_id, requests, window_seconds)
            VALUES (?, ?, ?)
        """, (client_id, req_str, window))
    db.commit()
    
    return True

# MercadoPago Webhook Secret
MERCADO_PAGO_WEBHOOK_SECRET = os.environ.get("MERCADO_PAGO_WEBHOOK_SECRET", "access_on_webhook_secret_2026")

# Logo base64 para emails
LOGO_DATA = """data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImxvZ28iIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPjxzdG9wIHN0b3AtY29sb3I9IiM2MzY2ZjEiLz48c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiNlYzQ4OWEiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cmVjdCB4PSI1MCIgeT0iMjUiIHdpZHRoPSI4MCIgaGVpZ2h0PSI1NSIgcng9IjgiIGZpbGw9InVybCgjbG9nbykiLz48Y2lyY2xlIGN4PSIzMCIgY3k9IjUyIiByPSIyMCIgZmlsbD0iIzY4NjhGRiIvPjxjaXJjbGUgY3g9IjcwIiBjeT0iNTIiIHI9IjIwIiBmaWxsPSIjNjg2OEZGIi8+PHJlY3QgeD0iNDgiIHk9IjQ4IiB3aWR0aD0iMjQiIGhlaWdodD0iOCIgcng9IjIiIGZpbGw9IiM2ODY4RkYiLz48cmVjdCB4PSI0NSIgeT0iMTUiIHdpZHRoPSIzMCIgaGVpZ2h0PSIxNSIgcng9IjQiIGZpbGw9InVybCgjbG9nbykiLz48L3N2Zz4="""

EMAIL_HEADER = f"""
    <div style="text-align: center; margin-bottom: 25px; padding-bottom: 20px; border-bottom: 2px solid #e5e7eb;">
        <img src="{EMAIL_LOGO_URL}" alt="Get Access" style="width: 150px; height: auto;" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
        <div style="display: none; color: #6366f1; font-size: 28px; font-weight: bold;">🎫 Get Access</div>
    </div>
"""

def get_email_template(content: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
        <div style="text-align: center; margin-bottom: 25px; padding-bottom: 20px; border-bottom: 2px solid #e5e7eb;">
            <h1 style="color: #6366f1; font-size: 28px; margin: 0; font-weight: bold;">🎫 Get Access</h1>
        </div>
        {content}
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 25px 0;">
        <p style="color: #9ca3af; font-size: 12px; text-align: center;">© 2026 Get Access - Todos los derechos reservados</p>
    </div>
</body>
</html>"""

def get_db():
    """Devuelve conexión a la base de datos (SQLite local o PostgreSQL Supabase)"""
    if DATABASE_URL.startswith("postgresql"):
        # Producción: Supabase PostgreSQL - sin RealDictCursor para compatibilidad
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        try:
            yield DbWrapper(conn, is_postgres=True)
        finally:
            conn.close()
    else:
        # Desarrollo: SQLite local
        conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield DbWrapper(conn, is_postgres=False)
        finally:
            conn.close()

class DbWrapper:
    """Wrapper para compatibilidad entre SQLite y PostgreSQL"""
    def __init__(self, conn, is_postgres=False):
        self._conn = conn
        self._is_postgres = is_postgres
    
    @property
    def is_postgres(self):
        return self._is_postgres
    
    def execute(self, query, params=None):
        # Convertir ? a %s para PostgreSQL siempre
        if self._is_postgres and '?' in query:
            query = query.replace('?', '%s')
        
        if self._is_postgres:
            cur = self._conn.cursor()
            cur.execute(query, params or [])
            return CursorWrapper(cur, self._conn)
        else:
            return self._conn.execute(query, params or [])
    
    def commit(self):
        self._conn.commit()

class CursorWrapper:
    """Wrapper para el cursor de PostgreSQL - devuelve tuplas como SQLite"""
    def __init__(self, cursor, conn):
        self._cursor = cursor
        self._conn = conn
    
    @property
    def lastrowid(self):
        cur = self._conn.cursor()
        cur.execute("SELECT lastval()")
        result = cur.fetchone()
        return result[0] if result else None
    
    @property
    def rowcount(self):
        return self._cursor.rowcount
    
    def fetchall(self):
        return self._cursor.fetchall()
    
    def fetchone(self):
        return self._cursor.fetchone()
    
    def fetchmany(self, size=5):
        return self._cursor.fetchmany(size)

# Tipos de conexión compatibles
try:
    from sqlite3 import Connection as SqliteConnection
except:
    SqliteConnection = object

try:
    import psycopg2
    from psycopg2.extensions import connection as PsycopgConnection
except:
    PsycopgConnection = object

def is_postgres():
    return DATABASE_URL.startswith("postgresql")

def execute_query(db, query, params=None):
    """Ejecuta query de forma compatible con SQLite y PostgreSQL"""
    if db.is_postgres:
        cur = db._conn.cursor()
        cur.execute(query.replace('?', '%s') if '?' in query else query, params or [])
        return cur
    else:
        return db.execute(query, params or [])

def fetch_all(db, query, params=None):
    """Fetch all rows compatible with both SQLite and PostgreSQL"""
    if db.is_postgres:
        cur = db._conn.cursor()
        cur.execute(query.replace('?', '%s') if '?' in query else query, params or [])
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    else:
        cursor = db.execute(query, params or [])
        return cursor.fetchall()

def fetch_one(db, query, params=None):
    """Fetch one row compatible with both SQLite y PostgreSQL"""
    if db.is_postgres:
        cur = db._conn.cursor()
        cur.execute(query.replace('?', '%s') if '?' in query else query, params or [])
        row = cur.fetchone()
        return dict(row) if row else None
    else:
        cursor = db.execute(query, params or [])
        return cursor.fetchone()

def run_query(db, query, params=None):
    """Ejecuta query sin return (INSERT, UPDATE, DELETE)"""
    if db.is_postgres:
        cur = db._conn.cursor()
        cur.execute(query.replace('?', '%s') if '?' in query else query, params or [])
        db.commit()
    else:
        db.execute(query, params or [])
        db.commit()

def last_row_id(db):
    """Get last inserted ID"""
    if db.is_postgres:
        cur = db._conn.cursor()
        cur.execute("SELECT lastval()")
        result = cur.fetchone()
        return result[0] if result else None
    else:
        return db._conn.execute("SELECT last_insert_rowid()").fetchone()[0]

# Acceso directo a execute para compatibilidad
# Pero vamos a usarlo solo con las funciones helper

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def generar_codigo():
    return ''.join(random.choices(string.digits, k=6))

def enviar_codigo_verificacion(email: str, codigo: str, nombre: str = ""):
    """Send verification email using Brevo API"""
    try:
        nombre_display = nombre if nombre else "Usuario"
        content = f"""
        <h2 style="color: #1f2937; text-align: center; margin-bottom: 20px;">Bienvenido {nombre_display}!</h2>
        <p style="color: #4b5563; font-size: 16px; line-height: 1.6;">
            Gracias por registrarte en <strong>Get Access</strong>. Tu código de verificación es:
        </p>
        <div style="background-color: #f3f4f6; border: 2px solid #6366f1; border-radius: 8px; padding: 20px; text-align: center; margin: 25px 0;">
            <span style="font-size: 28px; font-weight: bold; color: #6366f1; letter-spacing: 8px;">{codigo}</span>
        </div>
        <p style="color: #6b7280; font-size: 14px; text-align: center;">
            Este código expirará en 24 horas.
        </p>
        <p style="color: #ef4444; font-size: 14px; text-align: center; background-color: #fef2f2; padding: 12px; border-radius: 8px; margin-top: 20px;">
            ⚠️ Si no solicitaste este registro, puedes ignorar este email.
        </p>
        """
        
        html_content = get_email_template(content)
        
        data = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": email}],
            "subject": "🎫 Código de verificación - Get Access",
            "htmlContent": html_content
        }
        
        response = requests.post(BREVO_API_URL, json=data, headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"}, timeout=30)
        print(f"Brevo API Response Status: {response.status_code}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def enviar_email(to_email: str, subject: str, html_content: str):
    """Send generic email using Brevo API"""
    try:
        data = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": to_email}],
            "subject": subject,
            "htmlContent": html_content
        }
        
        response = requests.post(BREVO_API_URL, json=data, headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"}, timeout=30)
        print(f"Brevo API Response Status: {response.status_code}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

app = FastAPI(title="Access ON API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    pass

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://getaccess.com.ar",
        "https://getaccess-d3um.onrender.com",
        "http://localhost:3000",
        "https://192.168.1.40:3443"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where the main.py is located (backend folder)
BACKEND_DIR = Path(__file__).parent
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"

# Serve static files (images)
IMAGES_DIR = FRONTEND_DIR / "images"
if IMAGES_DIR.exists():
    app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

# Debug: print the paths
print(f"DEBUG: BACKEND_DIR = {BACKEND_DIR}")
print(f"DEBUG: FRONTEND_DIR = {FRONTEND_DIR}")
print(f"DEBUG: FRONTEND_DIR exists = {FRONTEND_DIR.exists()}")
if FRONTEND_DIR.exists():
    print(f"DEBUG: index.html exists = {(FRONTEND_DIR / 'index.html').exists()}")

@app.get("/")
async def serve_index():
    print(f"DEBUG: Serving index from {FRONTEND_DIR / 'index.html'}")
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/test-api")
def test_api():
    return {"test": "ok", "message": "API is working"}

@app.get("/api/visitas/", tags=["visitas"])
async def get_estadisticas_visitas(
    request: Request,
    dias: int = 30
):
    """Obtener estadísticas de visitas"""
    ip = get_client_ip(request)
    registrar_visita(ip)
    
    try:
        if "postgresql" in DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("""
                SELECT fecha, SUM(contador) as total, COUNT(DISTINCT ip) as ips_unicas
                FROM visitas
                WHERE fecha >= CURRENT_DATE - INTERVAL '%s day'
                GROUP BY fecha
                ORDER BY fecha DESC
            """, (dias,))
            resultados = cur.fetchall()
            cur.execute("SELECT SUM(contador) as total, COUNT(DISTINCT ip) as ips_unicas FROM visitas WHERE fecha >= CURRENT_DATE - INTERVAL '%s day'", (dias,))
            total = cur.fetchone()
            cur.close()
            conn.close()
        else:
            conn = sqlite3.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(f"""
                SELECT fecha, SUM(contador) as total, COUNT(DISTINCT ip) as ips_unicas
                FROM visitas
                WHERE fecha >= date('now', '-{dias} day')
                GROUP BY fecha
                ORDER BY fecha DESC
            """)
            resultados = cur.fetchall()
            cur.execute(f"SELECT SUM(contador) as total, COUNT(DISTINCT ip) as ips_unicas FROM visitas WHERE fecha >= date('now', '-{dias} day')")
            total = cur.fetchone()
            cur.close()
            conn.close()
        
        return {
            "total_visitas": total[0] or 0,
            "ips_unicas": total[1] or 0,
            "dias": dias,
            "detalle": [{"fecha": str(r[0]), "visitas": r[1], "ips": r[2]} for r in resultados]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/visitas/ip/", tags=["visitas"])
async def get_visitas_por_ip(
    request: Request,
    dias: int = 30
):
    """Obtener visitas por IP"""
    ip = get_client_ip(request)
    registrar_visita(ip)
    
    try:
        if "postgresql" in DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("""
                SELECT ip, SUM(contador) as total_visitas, COUNT(DISTINCT fecha) as dias
                FROM visitas
                WHERE fecha >= CURRENT_DATE - INTERVAL '%s day'
                GROUP BY ip
                ORDER BY total_visitas DESC
                LIMIT 100
            """, (dias,))
            resultados = cur.fetchall()
            cur.close()
            conn.close()
        else:
            conn = sqlite3.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(f"""
                SELECT ip, SUM(contador) as total_visitas, COUNT(DISTINCT fecha) as dias
                FROM visitas
                WHERE fecha >= date('now', '-{dias} day')
                GROUP BY ip
                ORDER BY total_visitas DESC
                LIMIT 100
            """)
            resultados = cur.fetchall()
            cur.close()
            conn.close()
        
        return {"ip": [{"ip": r[0], "visitas": r[1], "dias": r[2]} for r in resultados]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/scanner.html")
async def serve_scanner():
    return FileResponse(FRONTEND_DIR / "scanner.html")

@app.get("/{file_path:path}.html")
async def serve_html_files(file_path: str):
    file_path_html = FRONTEND_DIR / f"{file_path}.html"
    if file_path_html.exists() and file_path_html.is_file():
        return FileResponse(file_path_html)
    return FileResponse(FRONTEND_DIR / "index.html")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    import traceback
    from starlette.responses import JSONResponse
    error_msg = str(exc)
    tb = traceback.format_exc()
    print(f"========== EXCEPTION ==========")
    print(f"Request URL: {request.url}")
    print(f"Error: {error_msg}")
    print(f"Traceback: {tb}")
    print(f"=================================")
    return JSONResponse(
        status_code=500,
        content={"detail": error_msg},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

security = HTTPBearer()

# Pydantic Models
class UsuarioCreate(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioResponse(BaseModel):
    id: int
    email: str
    nombre: str
    apellido: str
    verificado: bool
    rol: str = "usuario"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UsuarioResponse

def crear_token(user_id: int) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def es_admin(db, user_id: int) -> bool:
    cursor = db.execute("SELECT rol FROM usuarios WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] == "admin"

def es_organizer(db, user_id: int) -> bool:
    cursor = db.execute("SELECT rol FROM usuarios WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] == "organizer"

def validar_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    if not any(c.isupper() for c in password):
        return False, "La contraseña debe tener al menos una letra mayúscula"
    if not any(c.islower() for c in password):
        return False, "La contraseña debe tener al menos una letra minúscula"
    if not any(c.isdigit() for c in password):
        return False, "La contraseña debe tener al menos un número"
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in password):
        return False, "La contraseña debe tener al menos un carácter especial"
    return True, ""

@app.post("/api/auth/registro", response_model=dict)
def registro(usuario: UsuarioCreate, request: Request, db = Depends(get_db)):
    client_id = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_id, db):
        raise HTTPException(status_code=429, detail="Demasiadas solicitudes. Intenta más tarde.")
    
    log_security("REGISTRO_INITIATED", f"Email: {usuario.email}")
    
    # Check if user exists
    cursor = db.execute("SELECT id FROM usuarios WHERE email = ?", (usuario.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Validate password
    valida, mensaje = validar_password(usuario.password)
    if not valida:
        raise HTTPException(status_code=400, detail=mensaje)
    
    # Generate verification code
    codigo = generar_codigo()
    hashed_password = hash_password(usuario.password)
    
    # Insert user
    cursor = db.execute(
        """INSERT INTO usuarios (email, nombre, apellido, password, verificado, codigo_verificacion) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (usuario.email, usuario.nombre, usuario.apellido, hashed_password, 0, codigo)
    )
    db.commit()
    user_id = cursor.lastrowid
    
    print(f">>> USUARIO CREADO CON ID: {user_id}")
    print(f">>> CODIGO GENERADO: {codigo}")
    
    # Send verification email
    email_enviado = enviar_codigo_verificacion(usuario.email, codigo, usuario.nombre)
    print(f">>> EMAIL ENVIADO: {email_enviado}")
    
    if not email_enviado:
        # Rollback user creation since email failed
        db.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        db.commit()
        raise HTTPException(status_code=500, detail="Failed to send verification email")
    
    return {
        "message": "Registro exitoso. Verifica tu email.",
        "email": usuario.email,
        "codigo": codigo,
        "requires_verification": True
    }

@app.post("/api/auth/login", response_model=TokenResponse)
def login(credenciales: UsuarioLogin, request: Request, db = Depends(get_db)):
    client_id = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_id, db):
        raise HTTPException(status_code=429, detail="Demasiados intentos. Espera un momento.")
    
    # Verificar brute-force protection
    puede_login, mensaje = check_brute_force(credenciales.email, db)
    if not puede_login:
        log_security("BRUTE_FORCE_BLOCKED_ATTEMPT", f"Email: {credenciales.email}")
        raise HTTPException(status_code=429, detail=mensaje)
    
    cursor = db.execute(
        "SELECT id, email, nombre, apellido, password, verificado, COALESCE(rol, 'usuario') as rol FROM usuarios WHERE email = ?",
        (credenciales.email,)
    )
    row = cursor.fetchone()
    
    if not row:
        record_brute_force_attempt(credenciales.email, False, db)
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Manejar tanto dict (PostgreSQL) como tupla (SQLite)
    if isinstance(row, dict):
        user_id = row['id']
        email = row['email']
        nombre = row['nombre']
        apellido = row['apellido']
        hashed_password = row['password']
        verificado = row['verificado']
        rol = row['rol']
    else:
        user_id, email, nombre, apellido, hashed_password, verificado, rol = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
    
    if not verificado:
        raise HTTPException(status_code=403, detail="Debes verificar tu email primero")
    
    if not verify_password(credenciales.password, hashed_password):
        record_brute_force_attempt(credenciales.email, False, db)
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Login exitoso
    record_brute_force_attempt(credenciales.email, True, db)
    log_security("LOGIN_SUCCESS", f"Email: {email}, UserID: {user_id}")
    
    access_token = crear_token(user_id)
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UsuarioResponse(id=user_id, email=email, nombre=nombre, apellido=apellido, verificado=bool(verificado), rol=rol)
    )

@app.post("/api/auth/verificar", response_model=TokenResponse)
def verificar_email(datos: dict, db = Depends(get_db)):
    email = datos.get("email")
    codigo = datos.get("codigo")
    
    if not email or not codigo:
        raise HTTPException(status_code=400, detail="Email y código son requeridos")
    
    # Get user
    cursor = db.execute(
        "SELECT id, email, nombre, apellido, password, verificado, codigo_verificacion, COALESCE(rol, 'usuario') as rol FROM usuarios WHERE email = ?",
        (email,)
    )
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_id, email_db, nombre, apellido, hashed_password, verificado, codigo_db, rol = row
    
    if codigo != codigo_db:
        raise HTTPException(status_code=400, detail="Código incorrecto")
    
    # Update user as verified
    db.execute(
        "UPDATE usuarios SET verificado = 1, codigo_verificacion = NULL WHERE id = ?",
        (user_id,)
    )
    db.commit()
    
    access_token = crear_token(user_id)
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UsuarioResponse(id=user_id, email=email_db, nombre=nombre, apellido=apellido, verificado=True, rol=rol)
    )

@app.get("/api/auth/me", response_model=UsuarioResponse)
def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute(
        "SELECT id, email, nombre, apellido, verificado, COALESCE(rol, 'usuario') as rol FROM usuarios WHERE id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    id, email, nombre, apellido, verificado, rol = row
    return UsuarioResponse(id=id, email=email, nombre=nombre, apellido=apellido, verificado=bool(verificado), rol=rol)

class PerfilUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    password_actual: Optional[str] = None
    password_nuevo: Optional[str] = None

@app.put("/api/auth/perfil")
def actualizar_perfil(datos: PerfilUpdate, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute(
        "SELECT id, email, nombre, apellido, password, verificado FROM usuarios WHERE id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_id_db, email_actual, nombre_actual, apellido_actual, hashed_password, verificado = row
    
    if datos.email and datos.email != email_actual:
        cursor = db.execute("SELECT id FROM usuarios WHERE email = ? AND id != ?", (datos.email, user_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    if datos.password_nuevo:
        if not datos.password_actual:
            raise HTTPException(status_code=400, detail="Ingresa tu contraseña actual")
        
        if not verify_password(datos.password_actual, hashed_password):
            raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
        
        valida, mensaje = validar_password(datos.password_nuevo)
        if not valida:
            raise HTTPException(status_code=400, detail=mensaje)
        
        hashed_password = hash_password(datos.password_nuevo)
    
    nuevo_nombre = datos.nombre if datos.nombre else nombre_actual
    nuevo_apellido = datos.apellido if datos.apellido else apellido_actual
    nuevo_email = datos.email if datos.email else email_actual
    
    db.execute(
        "UPDATE usuarios SET email = ?, nombre = ?, apellido = ?, password = ? WHERE id = ?",
        (nuevo_email, nuevo_nombre, nuevo_apellido, hashed_password, user_id)
    )
    db.commit()
    
    return {"message": "Perfil actualizado correctamente", "email": nuevo_email, "nombre": nuevo_nombre, "apellido": nuevo_apellido}

@app.post("/api/auth/solicitar-organizer")
def solicitar_organizer(credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("SELECT id, rol FROM usuarios WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if row[1] == "admin":
        raise HTTPException(status_code=400, detail="Ya eres administrador")
    
    if row[1] == "organizer":
        raise HTTPException(status_code=400, detail="Ya eres organizador")
    
    # Verificar estado de solicitud - permitir si está rechazada o no hay solicitud
    cursor = db.execute("SELECT id, estado FROM solicitud_organizer WHERE usuario_id = ? ORDER BY created_at DESC LIMIT 1", (user_id,))
    sol_row = cursor.fetchone()
    
    if sol_row:
        sol_id = sol_row[0] if isinstance(sol_row, tuple) else sol_row["id"]
        sol_estado = sol_row[1] if isinstance(sol_row, tuple) else sol_row["estado"]
        
        if sol_estado == 'pendiente':
            raise HTTPException(status_code=400, detail="Ya tienes una solicitud pendiente")
        elif sol_estado == 'rechazado':
            # Actualizar solicitud rechazada a pendiente
            db.execute("UPDATE solicitud_organizer SET estado = 'pendiente', motivo_rechazo = NULL WHERE id = ?", (sol_id,))
            db.commit()
            # Enviar email al admin
            cursor = db.execute("SELECT email, nombre, apellido FROM usuarios WHERE id = ?", (user_id,))
            user_row = cursor.fetchone()
            if user_row:
                usuario_email = user_row[0] if isinstance(user_row, tuple) else user_row["email"]
                usuario_nombre = user_row[1] if isinstance(user_row, tuple) else user_row["nombre"]
                usuario_apellido = user_row[2] if isinstance(user_row, tuple) else user_row["apellido"]
                
                # Enviar email al admin
                admin_email = "guilles10@yahoo.com.ar"
                email_content = get_email_template(f"""
                    <h2 style="color: #1f2937; text-align: center;">📋 Nueva solicitud de organizador</h2>
                    <p style="color: #4b5563; font-size: 16px;">El usuario <strong>{usuario_nombre} {usuario_apellido}</strong> ({usuario_email}) ha solicitado ser organizador de eventos.</p>
                    <p style="color: #6b7280; font-size: 14px;">Esta es una nueva solicitud (la anterior fue rechazada).</p>
                """)
                enviar_email(
                    to_email=admin_email,
                    subject="📋 Nueva solicitud de organizador - Get Access",
                    html_content=email_content
                )
            return {"message": "Solicitud reenviada correctamente. Un administrador revisará tu solicitud."}
    
    # No tiene solicitud - crear nueva
    db.execute(
        "INSERT INTO solicitud_organizer (usuario_id, estado) VALUES (?, 'pendiente')",
        (user_id,)
    )
    db.commit()
    
    # Obtener datos del usuario para enviar email al admin
    cursor = db.execute("SELECT email, nombre, apellido FROM usuarios WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    if user_row:
        usuario_email = user_row[0] if isinstance(user_row, tuple) else user_row["email"]
        usuario_nombre = user_row[1] if isinstance(user_row, tuple) else user_row["nombre"]
        usuario_apellido = user_row[2] if isinstance(user_row, tuple) else user_row["apellido"]
        
        # Enviar email al admin
        admin_email = "guilles10@yahoo.com.ar"
        email_content = get_email_template(f"""
            <h2 style="color: #1f2937; text-align: center;">📋 Nueva solicitud de organizador</h2>
            <p style="color: #4b5563; font-size: 16px;">El usuario <strong>{usuario_nombre} {usuario_apellido}</strong> ({usuario_email}) ha solicitado ser organizador de eventos.</p>
            <p style="color: #6b7280; font-size: 14px;">Revisa la solicitud en el panel de administración.</p>
        """)
        enviar_email(
            to_email=admin_email,
            subject="📋 Nueva solicitud de organizador - Get Access",
            html_content=email_content
        )
    
    return {"message": "Solicitud enviada correctamente. Un administrador revisará tu solicitud."}

@app.get("/api/auth/mi-estado")
def mi_estado(credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("SELECT id, email, nombre, apellido, verificado, COALESCE(rol, 'usuario') as rol FROM usuarios WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if isinstance(row, dict):
        return {
            "id": row["id"],
            "email": row["email"],
            "nombre": row["nombre"],
            "apellido": row["apellido"],
            "verificado": row["verificado"],
            "rol": row["rol"]
        }
    else:
        return {
            "id": row[0],
            "email": row[1],
            "nombre": row[2],
            "apellido": row[3],
            "verificado": row[4],
            "rol": row[5]
        }

@app.get("/api/auth/mi-solicitud-organizer")
def mi_solicitud_organizer(credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("""
        SELECT id, estado, motivo_rechazo, created_at 
        FROM solicitud_organizer 
        WHERE usuario_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    
    if not row:
        return {"hay_solicitud": False, "estado": None}
    
    if isinstance(row, dict):
        return {
            "hay_solicitud": True,
            "estado": row["estado"],
            "motivo_rechazo": row["motivo_rechazo"],
            "created_at": str(row["created_at"])
        }
    else:
        return {
            "hay_solicitud": True,
            "estado": row[1],
            "motivo_rechazo": row[2],
            "created_at": str(row[3])
        }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# === EVENTOS ===

class EventoCreate(BaseModel):
    nombre: str
    descripcion: str
    fecha: str
    lugar: str
    precio: float
    capacidad: int
    imagen: Optional[str] = None
    categoria: Optional[str] = None

class EventoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    fecha: str
    lugar: str
    precio: float
    disponibles: int

@app.get("/api/eventos/")
def listar_eventos(categoria: str = None, busqueda: str = None, mis_eventos: bool = False, db = Depends(get_db), credentials = None):
    try:
        # Si mis_eventos=true, obtener solo los eventos del organizador actual
        user_id = None
        if mis_eventos and credentials:
            try:
                payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = int(payload.get("sub"))
            except:
                pass  # Si no tiene token, devolver todos
        
        query = "SELECT id, nombre, descripcion, fecha, lugar, precio, capacidad, vendidos, COALESCE(imagen, '') as imagen, COALESCE(categoria, '') as categoria FROM eventos WHERE 1=1"
        params = []
        
        # Si es para mis eventos, filtrar por creado_por
        if user_id:
            query += " AND creado_por = ?"
            params.append(user_id)
        
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if busqueda:
            busqueda_lower = busqueda.lower()
            query += " AND (LOWER(nombre) LIKE ? OR LOWER(descripcion) LIKE ? OR LOWER(lugar) LIKE ?)"
            params.extend([f"%{busqueda_lower}%", f"%{busqueda_lower}%", f"%{busqueda_lower}%"])
        query += " ORDER BY fecha"
        
        cursor = db.execute(query, params)
        rows = cursor.fetchall()
        
        # Manejar tanto dict (PostgreSQL) como tupla (SQLite)
        return [
            {
                "id": r["id"] if isinstance(r, dict) else r[0],
                "nombre": r["nombre"] if isinstance(r, dict) else r[1],
                "descripcion": r["descripcion"] if isinstance(r, dict) else r[2],
                "fecha": r["fecha"] if isinstance(r, dict) else r[3],
                "lugar": r["lugar"] if isinstance(r, dict) else r[4],
                "precio": r["precio"] if isinstance(r, dict) else r[5],
                "disponibles": (r["capacidad"] if isinstance(r, dict) else r[6]) - (r["vendidos"] if isinstance(r, dict) else r[7]),
                "imagen": r["imagen"] if isinstance(r, dict) else r[8],
                "categoria": r["categoria"] if isinstance(r, dict) else r[9],
                "capacidad": r["capacidad"] if isinstance(r, dict) else r[6],
                "vendidos": r["vendidos"] if isinstance(r, dict) else r[7]
            }
            for r in rows
        ]
    except Exception as e:
        print(f">>> ERROR listar_eventos: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/eventos/categorias")
def listar_categorias(db = Depends(get_db)):
    cursor = db.execute("SELECT DISTINCT categoria FROM eventos WHERE categoria IS NOT NULL AND categoria != ''")
    rows = cursor.fetchall()
    # rows puede ser dict (PostgreSQL) o tuple (SQLite)
    return [r['categoria'] if isinstance(r, dict) else r[0] for r in rows]

@app.get("/api/eventos/{evento_id}")
def obtener_evento(evento_id: int, db = Depends(get_db)):
    cursor = db.execute("SELECT id, nombre, descripcion, fecha, lugar, precio, capacidad, vendidos, COALESCE(imagen, '') as imagen, COALESCE(categoria, '') as categoria FROM eventos WHERE id = ?", (evento_id,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    cursor_img = db.execute("SELECT id, url, orden FROM evento_imagenes WHERE evento_id = ? ORDER BY orden, id", (evento_id,))
    imagenes = [{"id": r[0], "url": r[1], "orden": r[2]} for r in cursor_img.fetchall()]
    
    return {
        "id": row[0], "nombre": row[1], "descripcion": row[2], "fecha": row[3], "lugar": row[4],
        "precio": row[5], "capacidad": row[6], "vendidos": row[7], "imagen": row[8], "categoria": row[9],
        "disponibles": row[6] - row[7], "imagenes": imagenes
    }

class ImagenCreate(BaseModel):
    url: str
    orden: int = 0

@app.post("/api/eventos/{evento_id}/imagenes")
def agregar_imagen(evento_id: int, imagen: ImagenCreate, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if not es_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Solo administradores pueden agregar imágenes")
    
    cursor = db.execute("SELECT id FROM eventos WHERE id = ?", (evento_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    cursor = db.execute("INSERT INTO evento_imagenes (evento_id, url, orden) VALUES (?, ?, ?)", (evento_id, imagen.url, imagen.orden))
    db.commit()
    
    return {"id": cursor.lastrowid, "url": imagen.url, "orden": imagen.orden}

@app.delete("/api/eventos/{evento_id}/imagenes/{imagen_id}")
def eliminar_imagen(evento_id: int, imagen_id: int, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if not es_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar imágenes")
    
    cursor = db.execute("DELETE FROM evento_imagenes WHERE id = ? AND evento_id = ?", (imagen_id, evento_id))
    db.commit()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    return {"message": "Imagen eliminada"}

@app.post("/api/eventos/")
def crear_evento(evento: EventoCreate, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Verificar rol - admin o organizer pueden crear
    cursor = db.execute("SELECT COALESCE(rol, 'usuario') FROM usuarios WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    user_rol = user_row[0] if isinstance(user_row, tuple) else user_row.get('rol', 'usuario')
    
    if user_rol not in ['admin', 'organizer']:
        raise HTTPException(status_code=403, detail="Solo administradores y organizadores pueden crear eventos")
    
    evento_fecha_str = evento.fecha.replace('Z', '')
    if '+' in evento_fecha_str:
        evento_fecha_str = evento_fecha_str.split('+')[0]
    evento_fecha = datetime.datetime.fromisoformat(evento_fecha_str)
    if evento_fecha < datetime.datetime.now():
        raise HTTPException(status_code=400, detail="La fecha ingresada no debe ser anterior a la fecha actual")
    
    cursor = db.execute(
        "INSERT INTO eventos (nombre, descripcion, fecha, lugar, precio, capacidad, vendidos, imagen, categoria, creado_por) VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?)",
        (evento.nombre, evento.descripcion, evento.fecha + " 20:00:00", evento.lugar, evento.precio, evento.capacidad, evento.imagen, evento.categoria, user_id)
    )
    db.commit()
    print(f">>> EVENTO CREADO: {evento.nombre}, ID: {cursor.lastrowid}, Fecha: {evento.fecha}")
    fecha_formateada = evento.fecha + " 20:00:00"
    return {"id": cursor.lastrowid, "nombre": evento.nombre, "descripcion": evento.descripcion, "fecha": fecha_formateada, "lugar": evento.lugar, "precio": evento.precio, "capacidad": evento.capacidad, "imagen": evento.imagen, "categoria": evento.categoria}

class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha: Optional[str] = None
    lugar: Optional[str] = None
    precio: Optional[float] = None
    capacidad: Optional[int] = None
    imagen: Optional[str] = None
    categoria: Optional[str] = None

@app.put("/api/eventos/{evento_id}")
def actualizar_evento(evento_id: int, evento: EventoUpdate, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if not es_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Solo administradores pueden editar eventos")
    
    cursor = db.execute("SELECT id FROM eventos WHERE id = ?", (evento_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    if evento.fecha is not None:
        evento_fecha_str = evento.fecha.replace('Z', '')
        if '+' in evento_fecha_str:
            evento_fecha_str = evento_fecha_str.split('+')[0]
        evento_fecha = datetime.datetime.fromisoformat(evento_fecha_str)
        if evento_fecha < datetime.datetime.now():
            raise HTTPException(status_code=400, detail="La fecha ingresada no debe ser anterior a la fecha actual")
    
    updates = []
    params = []
    if evento.nombre is not None:
        updates.append("nombre = ?")
        params.append(evento.nombre)
    if evento.descripcion is not None:
        updates.append("descripcion = ?")
        params.append(evento.descripcion)
    if evento.fecha is not None:
        updates.append("fecha = ?")
        params.append(evento.fecha)
    if evento.lugar is not None:
        updates.append("lugar = ?")
        params.append(evento.lugar)
    if evento.precio is not None:
        updates.append("precio = ?")
        params.append(evento.precio)
    if evento.capacidad is not None:
        updates.append("capacidad = ?")
        params.append(evento.capacidad)
    if evento.imagen is not None:
        updates.append("imagen = ?")
        params.append(evento.imagen)
    if evento.categoria is not None:
        updates.append("categoria = ?")
        params.append(evento.categoria)
    
    if not updates:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    params.append(evento_id)
    db.execute(f"UPDATE eventos SET {', '.join(updates)} WHERE id = ?", params)
    db.commit()
    
    cursor = db.execute("SELECT id, nombre, descripcion, fecha, lugar, precio, capacidad, vendidos, COALESCE(imagen, '') as imagen, COALESCE(categoria, '') as categoria FROM eventos WHERE id = ?", (evento_id,))
    row = cursor.fetchone()
    
    return {
        "id": row[0], "nombre": row[1], "descripcion": row[2], "fecha": row[3], "lugar": row[4],
        "precio": row[5], "capacidad": row[6], "vendidos": row[7], "imagen": row[8], "categoria": row[9],
        "disponibles": row[6] - row[7]
    }

@app.delete("/api/eventos/{evento_id}")
def eliminar_evento(evento_id: int, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if not es_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar eventos")
    
    cursor = db.execute("SELECT id, nombre FROM eventos WHERE id = ?", (evento_id,))
    evento = cursor.fetchone()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    db.execute("DELETE FROM evento_imagenes WHERE evento_id = ?", (evento_id,))
    db.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
    db.commit()
    
    return {"message": f"Evento '{evento[1]}' eliminado correctamente"}

# === ENTRADAS ===

class EntradaCreate(BaseModel):
    evento_id: int
    cantidad: int

class EntradaResponse(BaseModel):
    id: int
    evento_id: int
    usuario_id: int
    cantidad: int
    total: float
    estado: str

@app.get("/api/entradas/")
def listar_entradas(credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    request_id = str(random.randint(1000, 9999))
    print(f">>> [{request_id}] Entradas endpoint called")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        print(f">>> [{request_id}] User ID: {user_id}")
    except Exception as e:
        print(f">>> [{request_id}] Token error: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")
    
    try:
        cursor = db.execute("""
            SELECT e.id, e.evento_id, e.usuario_id, e.cantidad, e.total, e.estado, e.preference_id,
                   ev.nombre, ev.fecha, ev.lugar
            FROM entradas e
            JOIN eventos ev ON e.evento_id = ev.id
            WHERE e.usuario_id = ? AND e.estado = 'pagada' AND (e.transferida IS NULL OR e.transferida = 0)
            ORDER BY e.id DESC
        """, (user_id,))
        rows = cursor.fetchall()
        print(f">>> [{request_id}] Entradas found: {len(rows)}")
        return [
            {
                "id": r[0], "evento_id": r[1], "usuario_id": r[2], "cantidad": r[3],
                "total": r[4], "estado": r[5], "codigo": r[6],
                "evento": {"nombre": r[7], "fecha": r[8], "lugar": r[9]}
            }
            for r in rows
        ]
    except Exception as e:
        print(f">>> [{request_id}] Error listar_entradas: {e}")
        return []

@app.get("/api/entradas/buscar")
def buscar_entradas(q: str, db = Depends(get_db)):
    cursor = db.execute("""
        SELECT e.id, e.evento_id, e.usuario_id, e.cantidad, e.total, e.estado, e.preference_id,
               ev.nombre, ev.fecha, ev.lugar, u.email, u.nombre, u.apellido
        FROM entradas e
        JOIN eventos ev ON e.evento_id = ev.id
        JOIN usuarios u ON e.usuario_id = u.id
        WHERE u.email = ? AND (e.transferida IS NULL OR e.transferida = 0)
        ORDER BY e.id DESC
    """, (q,))
    rows = cursor.fetchall()
    
    if not rows:
        raise HTTPException(status_code=404, detail="No se encontraron entradas con ese email")
    
    return [
        {
            "id": r[0], "evento_id": r[1], "cantidad": r[3],
            "total": r[4], "estado": r[5],
            "evento": {"nombre": r[7], "fecha": r[8], "lugar": r[9]},
            "email": r[10], "nombre": r[11], "apellido": r[12]
        }
        for r in rows
    ]

@app.post("/api/entradas/")
def crear_entrada(entrada: EntradaCreate, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    print(f">>> CREAR ENTRADA: evento_id={entrada.evento_id}, cantidad={entrada.cantidad}")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        print(f">>> USER_ID: {user_id}")
    except Exception as e:
        print(f">>> ERROR TOKEN: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("SELECT id, precio, capacidad, vendidos FROM eventos WHERE id = ?", (entrada.evento_id,))
    evento = cursor.fetchone()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    print(f">>> EVENTO: {evento}")
    
    disponibles = evento[2] - evento[3]
    if disponibles < entrada.cantidad:
        raise HTTPException(status_code=400, detail="No hay suficientes entradas disponibles")
    
    total = evento[1] * entrada.cantidad
    print(f">>> TOTAL: {total}")
    
    cursor = db.execute(
        "INSERT INTO entradas (evento_id, usuario_id, cantidad, total, estado, preference_id, usada, transferida) VALUES (?, ?, ?, ?, ?, NULL, 0, 0)",
        (entrada.evento_id, user_id, entrada.cantidad, total, "pendiente")
    )
    db.commit()
    try:
        entrada_id = cursor.lastrowid
        print(f">>> ENTRADA_ID: {entrada_id}")
    except Exception as e:
        print(f">>> ERROR LASTROWID: {e}")
        entrada_id = random.randint(100000, 999999)
    
    db.execute("UPDATE eventos SET vendidos = vendidos + ? WHERE id = ?", (entrada.cantidad, entrada.evento_id))
    db.commit()
    
    return {"id": entrada_id, "evento_id": entrada.evento_id, "usuario_id": user_id, "cantidad": entrada.cantidad, "total": total, "estado": "pendiente", "codigo": None}

# === TRANSFERENCIA DE ENTRADAS ===
import secrets

class TransferenciaRequest(BaseModel):
    email_destino: EmailStr

@app.post("/api/entradas/{entrada_id}/transferir")
def transferir_entrada(entrada_id: int, req: TransferenciaRequest, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("SELECT usuario_id, estado, preference_id FROM entradas WHERE id = ?", (entrada_id,))
    entrada = cursor.fetchone()
    
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    
    if entrada[0] != user_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta entrada")
    
    if entrada[1] != "pagada":
        raise HTTPException(status_code=400, detail="Solo se pueden transferir entradas pagadas")
    
    cursor = db.execute("SELECT transferida FROM entradas WHERE id = ?", (entrada_id,))
    if cursor.fetchone()[0] == 1:
        raise HTTPException(status_code=400, detail="Esta entrada ya está en transferencia")
    
    token_transferencia = secrets.token_urlsafe(32)
    
    db.execute("UPDATE entradas SET transferida = 1 WHERE id = ?", (entrada_id,))
    
    db.execute("""INSERT INTO transferencias (entrada_id, usuario_origen, usuario_destino, token, estado, created_at) 
                  VALUES (?, ?, ?, ?, 'pendiente', datetime('now'))""",
               (entrada_id, user_id, req.email_destino, token_transferencia))
    db.commit()
    
    url_aceptar = f"{req.email_destino.split('@')[0]}"
    cursor = db.execute("SELECT id FROM transferencias WHERE token = ?", (token_transferencia,))
    transfer_id = cursor.fetchone()[0]
    
    cursor = db.execute("SELECT nombre, fecha FROM eventos e JOIN entradas en ON en.evento_id = e.id WHERE en.id = ?", (entrada_id,))
    evento = cursor.fetchone()
    
    html_content = f"""
        <h2 style="color: #1e293b;">🎫 Transferencia de Entrada</h2>
        <p>Hola, te han transferido una entrada para el evento:</p>
        <div style="background: #f8fafc; padding: 20px; border-radius: 12px; margin: 20px 0;">
            <p><strong>🎪 Evento:</strong> {evento[0] if evento else 'Evento'}</p>
            <p><strong>📅 Fecha:</strong> {evento[1] if evento else 'Fecha por confirmar'}</p>
            <p><strong>🎫 Código:</strong> {entrada[2]}</p>
        </div>
        <p>Para aceptar la transferencia, ingresa a Get Access e introduce este código:</p>
        <div style="background: #6366f1; color: white; padding: 15px; text-align: center; border-radius: 8px; font-size: 20px; font-family: monospace;">
            {token_transferencia}
        </div>
        <p style="color: #64748b; font-size: 12px; margin-top: 20px;">
            Si no solicitaste esta transferencia, ignora este email.
        </p>
    """
    
    requests.post(BREVO_API_URL, json={
        "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
        "to": [{"email": req.email_destino, "name": req.email_destino.split('@')[0]}],
        "subject": f"🎫 Te han transferido una entrada - {evento[0] if evento else 'Get Access'}",
        "htmlContent": get_email_template(html_content)
    }, headers={"api-key": BREVO_API_KEY}, timeout=10)
    
    return {"mensaje": "Transferencia iniciada. Se envió un email al destinatario.", "token": token_transferencia}

@app.post("/api/entradas/aceptar-transferencia")
def aceptar_transferencia(token: str, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token_auth = credentials.credentials
    try:
        payload = jwt.decode(token_auth, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("SELECT id, entrada_id, usuario_destino, estado FROM transferencias WHERE token = ?", (token,))
    transfer = cursor.fetchone()
    
    if not transfer:
        raise HTTPException(status_code=404, detail="Token de transferencia inválido")
    
    if transfer[3] != "pendiente":
        raise HTTPException(status_code=400, detail="Esta transferencia ya fue procesada")
    
    cursor = db.execute("SELECT email FROM usuarios WHERE id = ?", (user_id,))
    user_email = cursor.fetchone()[0]
    
    if transfer[2] != user_email:
        raise HTTPException(status_code=403, detail="Esta transferencia no es para ti")
    
    db.execute("UPDATE entradas SET usuario_id = ?, transferida = 0 WHERE id = ?", (user_id, transfer[1]))
    db.execute("UPDATE transferencias SET estado = 'completada', accepted_at = datetime('now') WHERE id = ?", (transfer[0],))
    db.commit()
    
    return {"mensaje": "¡Transferencia aceptada! La entrada ahora es tuya."}

import time
import random

@app.get("/api/transferencias/pendientes")
def get_transferencias_pendientes(credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    request_id = str(random.randint(1000, 9999))
    print(f">>> [{request_id}] Transferencias endpoint called")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        print(f">>> [{request_id}] User ID: {user_id}")
    except Exception as e:
        print(f">>> [{request_id}] Token error: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")
    
    try:
        cursor = db.execute("SELECT email FROM usuarios WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if not result:
            print(f">>> [{request_id}] No user found")
            return []
        user_email = result[0]
        print(f">>> [{request_id}] User email: {user_email}")
        
        cursor = db.execute("""
            SELECT t.id, t.entrada_id, t.token, t.estado, t.created_at,
                   e.preference_id, ev.nombre, ev.fecha, ev.lugar
            FROM transferencias t
            JOIN entradas e ON t.entrada_id = e.id
            JOIN eventos ev ON e.evento_id = ev.id
            WHERE t.usuario_destino = %s AND t.estado = 'pendiente'
            ORDER BY t.created_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        print(f">>> [{request_id}] Rows found: {len(rows)}")
        
        return [
            {
                "id": r['id'] if isinstance(r, dict) else r[0], 
                "entrada_id": r['entrada_id'] if isinstance(r, dict) else r[1], 
                "token": r['token'] if isinstance(r, dict) else r[2], 
                "estado": r['estado'] if isinstance(r, dict) else r[3], 
                "fecha": r['created_at'] if isinstance(r, dict) else r[4],
                "codigo": r['preference_id'] if isinstance(r, dict) else r[5], 
                "evento": r['nombre'] if isinstance(r, dict) else r[6], 
                "fecha_evento": r['fecha'] if isinstance(r, dict) else r[7], 
                "lugar": r['lugar'] if isinstance(r, dict) else r[8]
            }
            for r in rows
        ]
    except Exception as e:
        print(f">>> [{request_id}] DB ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/entradas/{entrada_id}/transferencias")
def get_transferencias(entrada_id: int, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("SELECT usuario_id FROM entradas WHERE id = ?", (entrada_id,))
    entrada = cursor.fetchone()
    
    if not entrada or entrada[0] != user_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta entrada")
    
    cursor = db.execute("""
        SELECT id, usuario_origen, usuario_destino, token, estado, created_at 
        FROM transferencias WHERE entrada_id = ? ORDER BY created_at DESC
    """, (entrada_id,))
    rows = cursor.fetchall()
    
    return [{"id": r[0], "origen": r[1], "destino": r[2], "token": r[3], "estado": r[4], "fecha": r[5]} for r in rows]

# === PAGOS (MercadoPago) ===

MERCADO_PAGO_ACCESS_TOKEN = os.environ.get("MERCADO_PAGO_ACCESS_TOKEN", "APP_USR-2888302331727804-031609-eb4c51fc6c1654d701d4a5f3b24fbcd7-1921694")

@app.post("/api/pagos/webhook")
async def webhook_mercadopago(request: Request, db = Depends(get_db)):
    try:
        client_ip = request.client.host if request.client else "unknown"
        body_json = await request.json()
        print(f">>> WEBHOOK RECIBIDO desde {client_ip}: {body_json}")
        
        topic = body_json.get("type")
        if topic == "payment":
            payment_id = body_json.get("data", {}).get("id")
            
            if payment_id:
                response = requests.get(
                    f"{MERCADOPAGO_API_URL}/v1/payments/{payment_id}",
                    headers={"Authorization": f"Bearer {MERCADO_PAGO_ACCESS_TOKEN}"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    payment_data = response.json()
                    status_mp = payment_data.get("status")
                    external_ref = payment_data.get("external_reference")
                    
                    print(f">>> Payment ID: {payment_id}, Status: {status_mp}, Ref: {external_ref}")
                    
                    if external_ref and status_mp == "approved":
                        entrada_ids = [int(x.strip()) for x in str(external_ref).split(',') if x.strip().isdigit()]
                        for ext_id in entrada_ids:
                            cursor_check = db.execute("SELECT id, estado, preference_id FROM entradas WHERE id = ?", (ext_id,))
                            entrada = cursor_check.fetchone()
                            if entrada and entrada[1] != "pagada":
                                db.execute("UPDATE entradas SET estado = 'pagada', usada = 0 WHERE id = ?", (ext_id,))
                                db.commit()
                                print(f">>> Entrada {ext_id} marcada como pagada")
                                
                                cursor = db.execute("""
                                    SELECT u.email, u.nombre, u.apellido, ev.nombre, ev.fecha, ev.lugar, e.cantidad, e.total, e.preference_id
                                    FROM entradas e
                                    JOIN usuarios u ON e.usuario_id = u.id
                                    JOIN eventos ev ON e.evento_id = ev.id
                                    WHERE e.id = ?
                                """, (ext_id,))
                                row = cursor.fetchone()
                                if row:
                                    import string
                                    if not row[8]:
                                        codigo = f"GA-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
                                        db.execute("UPDATE entradas SET preference_id = ? WHERE id = ?", (codigo, ext_id))
                                        db.commit()
                                    else:
                                        codigo = row[8]
                                    enviar_ticket_email(
                                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], ext_id, codigo
                                    )
                        
        return {"status": "ok"}
    except Exception as e:
        print(f">>> ERROR WEBHOOK: {e}")
        return {"status": "error", "detail": str(e)}

def enviar_ticket_email(email, nombre, apellido, evento_nombre, fecha, lugar, cantidad, total, entrada_id, codigo=None):
    import datetime
    
    codigo_display = codigo or f"GA-{entrada_id:06d}"
    
    qr_url = f"{QUICKCHART_URL}?size=300x300&text={codigo_display}"
    
    fecha_formateada = str(fecha)
    try:
        fecha_dt = datetime.datetime.strptime(str(fecha).split('.')[0], "%Y-%m-%d %H:%M:%S")
        fecha_formateada = fecha_dt.strftime("%d de %B de %Y - %H:%M")
    except:
        try:
            fecha_dt = datetime.datetime.strptime(str(fecha), "%Y-%m-%d")
            fecha_formateada = fecha_dt.strftime("%d de %B de %Y")
        except:
            pass
    
    email_content = f"""
        <h2 style="color: #1f2937; text-align: center; margin-bottom: 15px;">¡Hola {nombre} {apellido}!</h2>
        <p style="color: #4b5563; font-size: 16px; line-height: 1.6; text-align: center;">
            Tu entrada para <strong>{evento_nombre}</strong>
        </p>
        <div style="text-align: center; margin: 25px 0;">
            <p style="color: #6366f1; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 15px 0;">Escaneá este código en la entrada</p>
            <div style="background-color: #ffffff; display: inline-block; padding: 15px; border-radius: 12px; border: 2px solid #6366f1;">
                <img src="{qr_url}" alt="Código QR" style="width: 180px; height: 180px; display: block;">
            </div>
            <p style="color: #6366f1; font-size: 22px; font-weight: bold; margin: 15px 0 0 0; letter-spacing: 3px;">{codigo_display}</p>
        </div>
        <div style="background-color: #f3f4f6; border-radius: 8px; padding: 20px; margin: 25px 0;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                        <strong style="color: #4b5563;">📅 Fecha:</strong>
                    </td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                        {fecha_formateada}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                        <strong style="color: #4b5563;">📍 Lugar:</strong>
                    </td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                        {lugar}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                        <strong style="color: #4b5563;">🎟️ Cantidad:</strong>
                    </td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                        {cantidad} entrada{'s' if cantidad > 1 else ''}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 0;">
                        <strong style="color: #4b5563;">💵 Total:</strong>
                    </td>
                    <td style="padding: 10px 0; text-align: right; color: #10b981; font-weight: 800; font-size: 18px;">
                        ${total:,.2f}
                    </td>
                </tr>
            </table>
        </div>
        <div style="text-align: center; padding: 12px; background-color: #dcfce7; border-radius: 8px; margin: 20px 0;">
            <p style="color: #166534; margin: 0; font-weight: 700; font-size: 16px;">✅ PAGADA</p>
        </div>
        <p style="color: #6b7280; font-size: 14px; text-align: center;">
            Presentá el código QR en la entrada del evento o mostrá este email en tu celular.
        </p>
    """
    
    html_content = get_email_template(email_content)
    
    try:
        url = BREVO_API_URL
        headers = {"api-key": BREVO_API_KEY, "Content-Type": "application/json"}
        data = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": email}],
            "subject": f"🎫 Tu entrada para {evento_nombre} - Get Access",
            "htmlContent": html_content
        }
        response = requests.post(url, json=data, headers=headers, timeout=30)
        print(f">>> EMAIL ENVIADO A {email}: {response.status_code}")
    except Exception as e:
        print(f">>> ERROR ENVIANDO EMAIL: {e}")

@app.post("/api/pagos/carrito")
def crear_preferencia_carrito(datos: dict, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    entrada_ids = datos.get("entrada_ids", [])
    
    if not entrada_ids:
        raise HTTPException(status_code=400, detail="No hay entradas en el carrito")
    
    cursor = db.execute(f"""
        SELECT e.id, e.cantidad, e.total, ev.nombre
        FROM entradas e
        JOIN eventos ev ON e.evento_id = ev.id
        WHERE e.id IN ({','.join(['?'] * len(entrada_ids))}) AND e.estado = 'pendiente'
    """, entrada_ids)
    entradas = cursor.fetchall()
    
    if not entradas:
        raise HTTPException(status_code=404, detail="No hay entradas pendientes para pagar")
    
    items = []
    total = 0
    for ent in entradas:
        items.append({
            "id": str(ent[0]),
            "title": f"Entrada: {ent[3]}",
            "description": f"Entrada para {ent[3]}",
            "quantity": ent[1],
            "currency_id": "ARS",
            "unit_price": float(ent[2] / ent[1]),
            "category_id": "services"
        })
        total += ent[2]
    
    ext_refs = [str(e[0]) for e in entradas]
    
    back_url_base = os.environ.get("PRODUCTION_URL", "https://getaccess.com.ar")
    webhook_url = f"{RENDER_URL}/api/pagos/webhook"
    
    try:
        preference_data = {
            "items": items,
            "back_urls": {
                "success": f"{back_url_base}?pago=exito",
                "failure": f"{back_url_base}?pago=fallo",
                "pending": f"{back_url_base}?pago=pendiente"
            },
            "notification_url": webhook_url,
            "external_reference": ",".join(ext_refs)
        }
        
        response = requests.post(
            f"{MERCADOPAGO_API_URL}/checkout/preferences",
            json=preference_data,
            headers={"Authorization": f"Bearer {MERCADO_PAGO_ACCESS_TOKEN}"},
            timeout=30
        )
        
        if response.status_code == 201:
            return {"init_point": response.json()["init_point"], "total": total}
        else:
            raise HTTPException(status_code=500, detail="Error al crear preferencia de pago")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pagos/crear-preferencia")
def crear_preferencia_pago(datos: dict, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    entrada_id = datos.get("entrada_id")
    
    cursor = db.execute("""
        SELECT e.id, e.cantidad, e.total, ev.nombre
        FROM entradas e
        JOIN eventos ev ON e.evento_id = ev.id
        WHERE e.id = ? AND e.estado = 'pendiente'
    """, (entrada_id,))
    entrada = cursor.fetchone()
    
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada no encontrada o ya pagada")
    
    try:
        back_url_base = os.environ.get("PRODUCTION_URL", "https://getaccess.com.ar")
        webhook_url = f"{RENDER_URL}/api/pagos/webhook"
        preference_data = {
            "items": [
                {
                    "id": str(entrada_id),
                    "title": f"Entrada: {entrada[3]}",
                    "description": f"Entrada para {entrada[3]}",
                    "quantity": entrada[1],
                    "currency_id": "ARS",
                    "unit_price": entrada[2] / entrada[1],
                    "category_id": "services"
                }
            ],
            "back_urls": {
                "success": f"{back_url_base}?pago=exito",
                "failure": f"{back_url_base}?pago=fallo",
                "pending": f"{back_url_base}?pago=pendiente"
            },
            "notification_url": webhook_url,
            "external_reference": str(entrada_id)
        }
        
        response = requests.post(
            f"{MERCADOPAGO_API_URL}/checkout/preferences",
            json=preference_data,
            headers={"Authorization": f"Bearer {MERCADO_PAGO_ACCESS_TOKEN}"},
            timeout=30
        )
        
        if response.status_code == 201:
            return {"init_point": response.json()["init_point"]}
        else:
            raise HTTPException(status_code=500, detail="Error al crear preferencia de pago")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === RECUPERAR CONTRASEÑA ===

def generar_token_reset():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=64))

@app.post("/api/auth/recuperar")
def recuperar_password(datos: dict, request: Request, db = Depends(get_db)):
    client_id = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_id, db):
        raise HTTPException(status_code=429, detail="Demasiadas solicitudes. Intenta más tarde.")
    
    email = datos.get("email")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email requerido")
    
    cursor = db.execute("SELECT id, nombre FROM usuarios WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if not user:
        return {"message": "Si el email existe, recibirás un enlace de recuperación"}
    
    user_id, nombre = user
    
    token = generar_token_reset()
    expires = datetime.datetime.now() + datetime.timedelta(hours=1)
    
    db.execute("DELETE FROM password_reset WHERE email = ?", (email,))
    expires_str = expires.isoformat()
    db.execute("INSERT INTO password_reset (email, token, expires_at) VALUES (?, ?, ?)", (email, token, expires_str))
    db.commit()
    
    reset_url = f"https://getaccess.com.ar/?reset={token}"
    
    content = f"""
        <h2 style="color: #1f2937; text-align: center; margin-bottom: 20px;">🔐 Restablecer Contraseña</h2>
        <p style="color: #4b5563; font-size: 16px;">Hola <strong>{nombre}</strong>,</p>
        <p style="color: #4b5563; font-size: 16px; line-height: 1.6;">Recibimos una solicitud para restablecer tu contraseña. Haz clic en el botón de abajo:</p>
        <div style="text-align: center; margin: 35px 0;">
            <a href="{reset_url}" style="background-color: #10b981; color: #ffffff; padding: 16px 40px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; display: inline-block; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);">Restablecer Contraseña</a>
        </div>
        <div style="background-color: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p style="color: #6b7280; font-size: 14px; margin: 0;">O copia este enlace en tu navegador:</p>
            <p style="color: #6366f1; font-size: 13px; word-break: break-all; margin: 10px 0 0 0;">{reset_url}</p>
        </div>
        <p style="color: #ef4444; font-size: 14px; text-align: center; background-color: #fef2f2; padding: 12px; border-radius: 8px; margin: 20px 0;">⚠️ Este enlace expira en 1 hora</p>
    """
    
    email_content = get_email_template(content)
    
    try:
        url = BREVO_API_URL
        headers = {"api-key": BREVO_API_KEY, "Content-Type": "application/json"}
        data = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": email}],
            "subject": "🔐 Restablecer contraseña - Get Access",
            "htmlContent": email_content
        }
        response = requests.post(url, json=data, headers=headers, timeout=30)
        print(f">>> Email recuperación enviado: {response.status_code}")
    except Exception as e:
        print(f">>> Error enviando email: {e}")
    
    return {"message": "Si el email existe, recibirás un enlace de recuperación"}

@app.post("/api/admin/limpiar-tokens")
def limpiar_tokens(secret: str = None, db = Depends(get_db)):
    if not secret:
        raise HTTPException(status_code=401, detail="Secret requerido en header X-Admin-Secret")
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="No autorizado")
    db.execute("DELETE FROM password_reset")
    db.commit()
    return {"message": "Tokens de recuperación eliminados"}

@app.post("/api/auth/restablecer")
def restablecer_password(datos: dict, db = Depends(get_db)):
    token = datos.get("token")
    nueva_password = datos.get("nueva_password")
    
    if not token or not nueva_password:
        raise HTTPException(status_code=400, detail="Token y nueva contraseña son requeridos")
    
    valida, mensaje = validar_password(nueva_password)
    if not valida:
        raise HTTPException(status_code=400, detail=mensaje)
    
    cursor = db.execute("SELECT email, expires_at, usado FROM password_reset WHERE token = ? AND usado = 0", (token,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    
    email, expires_at, usado = row
    
    if usado:
        raise HTTPException(status_code=400, detail="Este enlace ya fue utilizado")
    
    try:
        if isinstance(expires_at, str):
            if 'Z' in expires_at:
                expires_at = expires_at.replace('Z', '+00:00')
            expires_at = datetime.datetime.fromisoformat(expires_at)
        elif hasattr(expires_at, 'year'):
            # Ya es datetime
            pass
        else:
            expires_at = datetime.datetime.fromisoformat(str(expires_at))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fecha: {str(e)}")
    
    if datetime.datetime.now() > expires_at:
        raise HTTPException(status_code=400, detail="El enlace ha expirado")
    
    hashed_password = hash_password(nueva_password)
    db.execute("UPDATE usuarios SET password = ? WHERE email = ?", (hashed_password, email))
    db.execute("UPDATE password_reset SET usado = 1 WHERE token = ?", (token,))
    db.commit()
    
    return {"message": "Contraseña restablecida correctamente"}

# === ADMIN ===

ADMIN_SECRET = "access_on_admin_secret_2026"

@app.post("/api/admin/hacer-admin")
def hacer_admin(datos: dict, db = Depends(get_db)):
    secret = datos.get("secret")
    email = datos.get("email")
    
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Secret inválido")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email requerido")
    
    db.execute("UPDATE usuarios SET rol = 'admin' WHERE email = ?", (email,))
    db.commit()
    
    cursor = db.execute("SELECT ROWID FROM usuarios WHERE email = ?", (email,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"message": f"{email} ahora es admin"}

# === VALIDACIÓN DE ENTRADAS ===

class ValidarEntradaRequest(BaseModel):
    codigo: str
    evento_id: Optional[int] = None

@app.post("/api/validar-entrada")
def validar_entrada(datos: ValidarEntradaRequest, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if not es_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Solo administradores pueden validar entradas")
    
    codigo = datos.codigo.strip().upper()
    parts = codigo.split("-")
    
    if len(parts) != 2 or parts[0] != "GA":
        raise HTTPException(status_code=400, detail="Código QR inválido")
    
    codigo_buscar = codigo
    
    cursor = db.execute("""
        SELECT e.id, e.cantidad, e.estado, e.evento_id, ev.nombre, ev.fecha, 
               u.nombre, u.apellido, e.usada
        FROM entradas e
        JOIN eventos ev ON e.evento_id = ev.id
        JOIN usuarios u ON e.usuario_id = u.id
        WHERE e.preference_id = ?
    """, (codigo_buscar,))
    entrada = cursor.fetchone()
    
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    
    if entrada[2] != "pagada":
        return {
            "valida": False,
            "estado": "rechazada",
            "mensaje": f"La entrada no ha sido pagada (Estado: {entrada[2]})",
            "entrada_id": entrada[0]
        }
    
    entrada_id = entrada[0]
    
    if entrada[8]:
        cursor_validaciones = db.execute("""
            SELECT COUNT(*) FROM validaciones WHERE entrada_id = ?
        """, (entrada_id,))
        veces_validada = cursor_validaciones.fetchone()[0]
        return {
            "valida": False,
            "estado": "ya_usada",
            "mensaje": f"Esta entrada ya fue utilizada ({veces_validada} vez/veces)",
            "entrada_id": entrada[0],
            "usuario": f"{entrada[6]} {entrada[7]}",
            "evento": entrada[4]
        }
    
    if datos.evento_id and entrada[3] != datos.evento_id:
        return {
            "valida": False,
            "estado": "evento_incorrecto",
            "mensaje": "Esta entrada es para otro evento",
            "entrada_id": entrada[0]
        }
    
    db.execute("""
        INSERT INTO validaciones (entrada_id, scanner_id, cantidad_original) 
        VALUES (?, ?, ?)
    """, (entrada_id, user_id, entrada[1]))
    db.execute("UPDATE entradas SET usada = 1 WHERE id = ?", (entrada_id,))
    db.commit()
    
    return {
        "valida": True,
        "estado": "aceptada",
        "mensaje": "Entrada válida. ¡Bienvenido!",
        "entrada_id": entrada[0],
        "usuario": f"{entrada[6]} {entrada[7]}",
        "evento": entrada[4],
        "fecha": entrada[5]
    }

@app.get("/api/validar/{codigo}")
def consultar_entrada(codigo: str, db = Depends(get_db)):
    codigo = codigo.strip().upper()
    parts = codigo.split("-")
    
    if len(parts) != 2 or parts[0] != "GA":
        raise HTTPException(status_code=400, detail="Código QR inválido")
    
    cursor = db.execute("""
        SELECT e.id, e.cantidad, e.estado, e.evento_id, ev.nombre, ev.fecha, ev.lugar,
               u.nombre, u.apellido, e.usada
        FROM entradas e
        JOIN eventos ev ON e.evento_id = ev.id
        JOIN usuarios u ON e.usuario_id = u.id
        WHERE e.preference_id = ?
    """, (codigo,))
    entrada = cursor.fetchone()
    
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    
    cursor_validaciones = db.execute("""
        SELECT COUNT(*) FROM validaciones WHERE entrada_id = ?
    """, (entrada_id,))
    veces_validada = cursor_validaciones.fetchone()[0]
    
    return {
        "entrada_id": entrada[0],
        "cantidad": entrada[1],
        "estado": entrada[2],
        "usada": entrada[9] == 1,
        "veces_validada": veces_validada,
        "evento": {
            "id": entrada[3],
            "nombre": entrada[4],
            "fecha": entrada[5],
            "lugar": entrada[6]
        },
        "usuario": f"{entrada[7]} {entrada[8]}"
    }

@app.get("/api/eventos/{evento_id}/estadisticas")
def estadisticas_evento(evento_id: int, db = Depends(get_db)):
    cursor = db.execute("SELECT id, nombre FROM eventos WHERE id = ?", (evento_id,))
    evento = cursor.fetchone()
    
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    cursor_entradas = db.execute("""
        SELECT COUNT(*), SUM(cantidad) FROM entradas 
        WHERE evento_id = ? AND estado = 'pagada'
    """, (evento_id,))
    row_entradas = cursor_entradas.fetchone()
    
    cursor_validadas = db.execute("""
        SELECT COUNT(DISTINCT v.entrada_id) FROM validaciones v
        JOIN entradas e ON v.entrada_id = e.id
        WHERE e.evento_id = ?
    """, (evento_id,))
    validadas = cursor_validadas.fetchone()[0] or 0
    
    cursor_pendientes = db.execute("""
        SELECT COUNT(*) FROM entradas 
        WHERE evento_id = ? AND estado = 'pagada' AND usada = 0
    """, (evento_id,))
    pendientes = cursor_pendientes.fetchone()[0] or 0
    
    return {
        "evento_id": evento_id,
        "evento_nombre": evento[1],
        "total_entradas": row_entradas[0] or 0,
        "total_personas": row_entradas[1] or 0,
        "validadas": validadas,
        "pendientes": pendientes
    }

@app.get("/api/validaciones/historial")
def historial_validaciones(evento_id: int = None, db = Depends(get_db)):
    from datetime import datetime, timedelta
    
    fecha_limite = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    
    query = """
        SELECT v.id, v.entrada_id, v.timestamp, v.scanner_id,
               e.evento_id, ev.nombre, u.nombre, u.apellido
        FROM validaciones v
        JOIN entradas e ON v.entrada_id = e.id
        JOIN eventos ev ON e.evento_id = ev.id
        JOIN usuarios u ON v.scanner_id = u.id
        WHERE v.timestamp >= ?
    """
    params = [fecha_limite]
    
    if evento_id:
        query += " AND e.evento_id = ?"
        params.append(evento_id)
    
    query += " ORDER BY v.timestamp DESC LIMIT 500"
    
    cursor = db.execute(query, params)
    rows = cursor.fetchall()
    
    return [
        {
            "id": r[0],
            "entrada_id": r[1],
            "timestamp": r[2],
            "scanner": f"{r[6]} {r[7]}",
            "evento_id": r[4],
            "evento_nombre": r[5]
        }
        for r in rows
    ]

@app.get("/api/eventos/{evento_id}/codigos-validos")
def get_codigos_validos(evento_id: int, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("""
        SELECT e.id, e.preference_id, e.estado, e.usada,
               (SELECT COUNT(*) FROM validaciones WHERE entrada_id = e.id) as veces_validada
        FROM entradas e
        WHERE e.evento_id = ? AND e.estado = 'pagada'
    """, (evento_id,))
    rows = cursor.fetchall()
    
    codigos = []
    for r in rows:
        codigos.append({
            "codigo": r[1],
            "usada": r[3] == 1 or r[4] > 0
        })
    
    return {"codigos": codigos, "total": len(codigos)}

# === ANALYTICS ===
@app.get("/api/analytics/{tipo}")
def get_analytics_general(tipo: str, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Obtener el rol del usuario
    cursor = db.execute("SELECT COALESCE(rol, 'usuario') FROM usuarios WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    user_rol = user_row[0] if isinstance(user_row, tuple) else user_row.get('rol', 'usuario')
    
    # Si es organizer, filtrar solo sus eventos
    if user_rol == 'organizer':
        # Solo mostrar eventos creados por este organizador
        cursor = db.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas JOIN eventos ON entradas.evento_id = eventos.id WHERE entradas.estado = 'pagada' AND eventos.creado_por = ?", (user_id,))
    else:
        # Admin o usuario: todos los eventos
        cursor = db.execute("SELECT COALESCE(SUM(cantidad), 0) as cnt_total, COALESCE(SUM(total), 0) as total FROM entradas WHERE estado = 'pagada'")
    
    row = cursor.fetchone()
    if isinstance(row, dict):
        ventas_total = row.get('cnt_total') or 0
        ingresos_total = row.get('total') or 0
    else:
        ventas_total = row[0] or 0
        ingresos_total = row[1] or 0
    
    # Por categoría - filtrar si es organizer
    if user_rol == 'organizer':
        cursor = db.execute("""
            SELECT COALESCE(eventos.categoria, 'sin_categoria') as cat, COUNT(*) as cantidad
            FROM entradas
            JOIN eventos ON entradas.evento_id = eventos.id
            WHERE entradas.estado = 'pagada' AND eventos.creado_por = ?
            GROUP BY cat
        """, (user_id,))
    else:
        cursor = db.execute("""
            SELECT COALESCE(eventos.categoria, 'sin_categoria') as cat, COUNT(*) as cantidad
            FROM entradas
            JOIN eventos ON entradas.evento_id = eventos.id
            WHERE entradas.estado = 'pagada'
            GROUP BY cat
        """)
    por_categoria = []
    for r in cursor.fetchall():
        if isinstance(r, dict):
            por_categoria.append({"categoria": r.get('cat', ''), "cantidad": r.get('cantidad', 0)})
        else:
            por_categoria.append({"categoria": r[0], "cantidad": r[1]})
    
    # Top eventos - filtrar si es organizer
    if user_rol == 'organizer':
        cursor = db.execute("""
            SELECT e.id, e.nombre, e.vendidos, (e.vendidos * e.precio) as ingresos
            FROM eventos e
            WHERE e.vendidos > 0 AND e.creado_por = ?
            ORDER BY e.vendidos DESC
            LIMIT 10
        """, (user_id,))
    else:
        cursor = db.execute("""
            SELECT e.id, e.nombre, e.vendidos, (e.vendidos * e.precio) as ingresos
            FROM eventos e
            WHERE e.vendidos > 0
            ORDER BY e.vendidos DESC
            LIMIT 10
        """)
    top_eventos = []
    for r in cursor.fetchall():
        if isinstance(r, dict):
            top_eventos.append({"id": r.get("id"), "nombre": r.get("nombre"), "vendidos": r.get("vendidos"), "ingresos": r.get("ingresos")})
        else:
            top_eventos.append({"id": r[0], "nombre": r[1], "vendidos": r[2], "ingresos": r[3]})
    
    # Validaciones - filtrar si es organizer
    if user_rol == 'organizer':
        cursor = db.execute("""
            SELECT COUNT(*) FROM validaciones v
            JOIN entradas e ON v.entrada_id = e.id
            JOIN eventos ev ON e.evento_id = ev.id
            WHERE ev.creado_por = ?
        """, (user_id,))
    else:
        cursor = db.execute("SELECT COUNT(*) FROM validaciones")
    row = cursor.fetchone()
    tickets_usados = row[0] if isinstance(row, tuple) else (row.get('count') or row.get('cnt') or 0) if isinstance(row, dict) else 0
    
    # Query compatible con SQLite y PostgreSQL
    if user_rol == 'organizer' and db.is_postgres:
        cursor = db.execute("""
            SELECT DATE(creada_en)::date as fecha, SUM(cantidad) as cantidad
            FROM entradas en
            JOIN eventos e ON en.evento_id = e.id
            WHERE en.estado = 'pagada' AND e.creado_por = ? AND creada_en >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY fecha
            ORDER BY fecha DESC
            LIMIT 14
        """, (user_id,))
    elif user_rol == 'organizer':
        cursor = db.execute("""
            SELECT DATE(creada_en) as fecha, SUM(cantidad) as cantidad
            FROM entradas en
            JOIN eventos e ON en.evento_id = e.id
            WHERE en.estado = 'pagada' AND e.creado_por = ? AND creada_en >= DATE('now', '-30 days')
            GROUP BY fecha
            ORDER BY fecha DESC
            LIMIT 14
        """, (user_id,))
    elif db.is_postgres:
        cursor = db.execute("""
            SELECT DATE(creada_en)::date as fecha, SUM(cantidad) as cantidad
            FROM entradas
            WHERE estado = 'pagada' AND creada_en >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY fecha
            ORDER BY fecha DESC
            LIMIT 14
        """)
    else:
        cursor = db.execute("""
            SELECT DATE(creada_en) as fecha, SUM(cantidad) as cantidad
            FROM entradas
            WHERE estado = 'pagada' AND creada_en >= DATE('now', '-30 days')
            GROUP BY fecha
            ORDER BY fecha DESC
            LIMIT 14
        """)
    ventas_por_dia = []
    for r in cursor.fetchall():
        if isinstance(r, dict):
            ventas_por_dia.append({"fecha": str(r.get("fecha", "")) if r.get("fecha") else "", "cantidad": r.get("cantidad", 0)})
        else:
            ventas_por_dia.append({"fecha": str(r[0]) if r[0] else "", "cantidad": r[1]})
    
    precio_promedio = ingresos_total / ventas_total if ventas_total > 0 else 0
    
    probabilidad = 0
    dias_promedio = 0
    tendencia = "estable"
    if top_eventos:
        evento = top_eventos[0]
        if evento['vendidos'] > evento.get('vendidos', 0) * 0.8:
            probabilidad = min(95, int((evento['vendidos'] / max(evento.get('vendidos', 1), 1)) * 100))
        dias_promedio = 15
        if len(ventas_por_dia) >= 2 and ventas_por_dia[0]['cantidad'] > ventas_por_dia[1]['cantidad']:
            tendencia = "al alza"
        elif len(ventas_por_dia) >= 2 and ventas_por_dia[0]['cantidad'] < ventas_por_dia[1]['cantidad']:
            tendencia = "a la baja"
    
    return {
        "ventas_total": ventas_total,
        "ingresos_total": ingresos_total,
        "tickets_usados": tickets_usados,
        "por_categoria": por_categoria,
        "top_eventos": top_eventos,
        "ventas_por_dia": ventas_por_dia,
        "precio_promedio": precio_promedio,
        "proyeccion": {
            "probabilidad_agotar": probabilidad,
            "dias_promedio_venta": dias_promedio,
            "tendencia": tendencia
        }
    }

@app.get("/api/admin/solicitudes-organizer")
def listar_solicitudes(credentials: HTTPAuthorizationCredentials = Depends(security), db: sqlite3.Connection = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if not es_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Solo administradores possono ver solicitudes")
    
    cursor = db.execute("""
        SELECT s.id, s.usuario_id, s.estado, s.motivo_rechazo, s.created_at, u.email, u.nombre, u.apellido
        FROM solicitud_organizer s
        JOIN usuarios u ON s.usuario_id = u.id
        ORDER BY s.created_at DESC
    """)
    rows = cursor.fetchall()
    
    solicitudes = []
    for r in rows:
        if isinstance(r, dict):
            solicitudes.append({
                "id": r["id"],
                "usuario_id": r["usuario_id"],
                "estado": r["estado"],
                "motivo_rechazo": r["motivo_rechazo"],
                "created_at": r["created_at"],
                "email": r["email"],
                "nombre": r["nombre"],
                "apellido": r["apellido"]
            })
        else:
            solicitudes.append({
                "id": r[0],
                "usuario_id": r[1],
                "estado": r[2],
                "motivo_rechazo": r[3],
                "created_at": r[4],
                "email": r[5],
                "nombre": r[6],
                "apellido": r[7]
            })
    
    return solicitudes

class SolicitudUpdate(BaseModel):
    solicitud_id: int
    motivo: Optional[str] = None

@app.post("/api/admin/aprobar-organizer")
def aprobar_organizer(data: SolicitudUpdate, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if not es_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Solo administradores pueden aprobar solicitudes")
    
    cursor = db.execute("SELECT usuario_id, estado FROM solicitud_organizer WHERE id = ?", (data.solicitud_id,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    usuario_id_solicitante = row[0]
    
    db.execute("UPDATE usuarios SET rol = 'organizer' WHERE id = ?", (usuario_id_solicitante,))
    db.execute("UPDATE solicitud_organizer SET estado = 'aprobado' WHERE id = ?", (data.solicitud_id,))
    db.commit()
    
    cursor = db.execute("SELECT email, nombre FROM usuarios WHERE id = ?", (usuario_id_solicitante,))
    user_row = cursor.fetchone()
    if user_row:
        email_destino = user_row[0] if isinstance(user_row, tuple) else user_row["email"]
        nombre_usuario = user_row[1] if isinstance(user_row, tuple) else user_row["nombre"]
        enviar_email(
            to_email=email_destino,
            subject="¡Tu solicitud de Organizador ha sido aprobada!",
            html_content=f"""
            <h2>¡Felicitaciones, {nombre_usuario}!</h2>
            <p>Tu solicitud para convertirte en organizador ha sido <strong>aprobada</strong>.</p>
            <p>Ahora puedes crear eventos y gestionar tus propias actividades en Get Access.</p>
            <p>Accede a tu panel de organizador desde el menú.</p>
            <hr>
            <p>Get Access - Sistema de Entradas</p>
            """
        )
    
    return {"message": "Organizador aprobado correctamente"}

@app.post("/api/admin/rechazar-organizer")
def rechazar_organizer(data: SolicitudUpdate, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if not es_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Solo administradores pueden rechazar solicitudes")
    
    cursor = db.execute("SELECT usuario_id, estado FROM solicitud_organizer WHERE id = ?", (data.solicitud_id,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    usuario_id_solicitante = row[0]
    
    db.execute("UPDATE solicitud_organizer SET estado = 'rechazado', motivo_rechazo = ? WHERE id = ?", (data.motivo or "Solicitud rechazada", data.solicitud_id))
    db.commit()
    
    cursor = db.execute("SELECT email, nombre FROM usuarios WHERE id = ?", (usuario_id_solicitante,))
    user_row = cursor.fetchone()
    if user_row:
        email_destino = user_row[0] if isinstance(user_row, tuple) else user_row["email"]
        nombre_usuario = user_row[1] if isinstance(user_row, tuple) else user_row["nombre"]
        enviar_email(
            to_email=email_destino,
            subject="Estado de tu solicitud de Organizador",
            html_content=f"""
            <h2>Hola, {nombre_usuario},</h2>
            <p>Lamentamos informarte que tu solicitud para convertirte en organizador ha sido <strong>rechazada</strong>.</p>
            {f"<p>Motivo: {data.motivo}</p>" if data.motivo else ""}
            <p>Si tienes alguna consulta, puedes contactarnos respondiendo este email.</p>
            <hr>
            <p>Get Access - Sistema de Entradas</p>
            """
        )
    
    return {"message": "Solicitud rechazada"}

@app.get("/api/analytics/evento/{evento_id}")
def get_analytics_evento(evento_id: int, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("SELECT COUNT(*), SUM(total), SUM(cantidad), precio, capacidad FROM entradas en JOIN eventos e ON en.evento_id = e.id WHERE en.evento_id = ? AND en.estado = 'pagada'", (evento_id,))
    row = cursor.fetchone()
    ventas_total = row[2] or 0
    ingresos_total = row[1] or 0
    
    cursor = db.execute("""
        SELECT COUNT(*) FROM validaciones v
        JOIN entradas e ON v.entrada_id = e.id
        WHERE e.evento_id = ?
    """, (evento_id,))
    tickets_usados = cursor.fetchone()[0]
    
    cursor = db.execute("""
        SELECT DATE(v.timestamp) as fecha, COUNT(*) as cantidad
        FROM validaciones v
        JOIN entradas e ON v.entrada_id = e.id
        WHERE e.evento_id = ? AND v.timestamp >= DATE('now', '-30 days')
        GROUP BY fecha
        ORDER BY fecha DESC
    """, (evento_id,))
    ventas_por_dia = [{"fecha": r[0], "cantidad": r[1]} for r in cursor.fetchall()]
    
    precio_promedio = ingresos_total / ventas_total if ventas_total > 0 else 0
    capacidad = row[4] or 1
    vendidos = row[3] or 0
    probabilidad = min(100, int((vendidos / capacidad) * 100))
    
    return {
        "ventas_total": ventas_total,
        "ingresos_total": ingresos_total,
        "tickets_usados": tickets_usados,
        "ventas_por_dia": ventas_por_dia,
        "precio_promedio": precio_promedio,
        "proyeccion": {
            "probabilidad_agotar": probabilidad,
            "dias_promedio_venta": 10,
            "tendencia": "estable" if len(ventas_por_dia) < 2 else ("al alza" if ventas_por_dia[0]['cantidad'] > ventas_por_dia[-1]['cantidad'] else "a la baja")
        }
    }
    
# === EMAIL TICKET ===

def generar_qr_base64(codigo: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(codigo)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    return base64.b64encode(buffer.getvalue()).decode()

@app.post("/api/email/enviar-ticket")
def enviar_ticket(entrada_id: int, credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    cursor = db.execute("""
        SELECT e.id, e.cantidad, e.total, e.estado, ev.nombre, ev.fecha, ev.lugar, u.email, u.nombre, u.apellido
        FROM entradas e
        JOIN eventos ev ON e.evento_id = ev.id
        JOIN usuarios u ON e.usuario_id = u.id
        WHERE e.id = ? AND e.usuario_id = ?
    """, (entrada_id, user_id))
    entrada = cursor.fetchone()
    
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    
    cursor = db.execute("SELECT preference_id FROM entradas WHERE id = ?", (entrada_id,))
    preference_id = cursor.fetchone()[0]
    
    codigo_qr = preference_id if preference_id else f"GA-{entrada[0]:06d}"
    qr_url = f"{QUICKCHART_URL}?size=300x300&text={codigo_qr}"
    
    fecha_formateada = entrada[5]
    try:
        fecha_dt = datetime.datetime.strptime(entrada[5].split('.')[0], "%Y-%m-%d %H:%M:%S")
        fecha_formateada = fecha_dt.strftime("%d de %B de %Y - %H:%M")
    except:
        try:
            fecha_dt = datetime.datetime.strptime(entrada[5], "%Y-%m-%d")
            fecha_formateada = fecha_dt.strftime("%d de %B de %Y")
        except:
            pass
    
    email_content = f"""
        <h2 style="color: #1f2937; text-align: center; margin-bottom: 15px;">¡Hola {entrada[8]} {entrada[9]}!</h2>
        <p style="color: #4b5563; font-size: 16px; line-height: 1.6; text-align: center;">
            Tu entrada para <strong>{entrada[4]}</strong>
        </p>
        <div style="text-align: center; margin: 25px 0;">
            <p style="color: #6366f1; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 15px 0;">Escaneá este código en la entrada</p>
            <div style="background-color: #ffffff; display: inline-block; padding: 15px; border-radius: 12px; border: 2px solid #6366f1;">
                <img src="{qr_url}" alt="Código QR" style="width: 180px; height: 180px; display: block;">
            </div>
            <p style="color: #6366f1; font-size: 22px; font-weight: bold; margin: 15px 0 0 0; letter-spacing: 3px;">{codigo_qr}</p>
        </div>
        <div style="background-color: #f3f4f6; border-radius: 8px; padding: 20px; margin: 25px 0;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                        <strong style="color: #4b5563;">📅 Fecha:</strong>
                    </td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                        {fecha_formateada}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                        <strong style="color: #4b5563;">📍 Lugar:</strong>
                    </td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                        {entrada[6]}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                        <strong style="color: #4b5563;">🎟️ Cantidad:</strong>
                    </td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                        {entrada[1]} entrada{'' if entrada[1] == 1 else 's'}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 0;">
                        <strong style="color: #4b5563;">💵 Total:</strong>
                    </td>
                    <td style="padding: 10px 0; text-align: right; color: #10b981; font-weight: 800; font-size: 18px;">
                        ${entrada[2]:,.2f}
                    </td>
                </tr>
            </table>
        </div>
        <div style="text-align: center; padding: 12px; background-color: #dcfce7; border-radius: 8px; margin: 20px 0;">
            <p style="color: #166534; margin: 0; font-weight: 700; font-size: 16px;">✅ {entrada[3].upper()}</p>
        </div>
        <p style="color: #6b7280; font-size: 14px; text-align: center;">
            Presentá el código QR en la entrada del evento o mostrá este email en tu celular.
        </p>
    """
    
    html_content = get_email_template(email_content)
    
    try:
        url = BREVO_API_URL
        headers = {"api-key": BREVO_API_KEY, "Content-Type": "application/json"}
        data = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": entrada[7]}],
            "subject": f"🎫 Tu entrada para {entrada[4]} - Get Access",
            "htmlContent": html_content
        }
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 201:
            return {"message": "Ticket enviado", "email": entrada[7], "codigo": codigo_qr}
        else:
            return {"message": "Error al enviar", "detail": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/email/reenviar-ticket")
def reenviar_ticket_sin_auth(entrada_id: int, email: str, db = Depends(get_db)):
    cursor = db.execute("""
        SELECT e.id, e.cantidad, e.total, e.estado, ev.nombre, ev.fecha, ev.lugar, u.email, u.nombre, u.apellido
        FROM entradas e
        JOIN eventos ev ON e.evento_id = ev.id
        JOIN usuarios u ON e.usuario_id = u.id
        WHERE e.id = ? AND u.email = ?
    """, (entrada_id, email))
    entrada = cursor.fetchone()
    
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada no encontrada para este email")
    
    cursor = db.execute("SELECT preference_id FROM entradas WHERE id = ?", (entrada_id,))
    pref_row = cursor.fetchone()
    preference_id = pref_row[0] if pref_row and pref_row[0] else None
    
    codigo_qr = preference_id if preference_id else f"GA-{entrada[0]:06d}"
    qr_url = f"{QUICKCHART_URL}?size=300x300&text={codigo_qr}"
    qr_cid = f"qr-{entrada_id}-{int(datetime.datetime.now().timestamp())}"
    
    fecha_formateada = entrada[5]
    try:
        fecha_dt = datetime.datetime.strptime(entrada[5].split('.')[0], "%Y-%m-%d %H:%M:%S")
        fecha_formateada = fecha_dt.strftime("%d de %B de %Y - %H:%M")
    except:
        try:
            fecha_dt = datetime.datetime.strptime(entrada[5], "%Y-%m-%d")
            fecha_formateada = fecha_dt.strftime("%d de %B de %Y")
        except:
            pass
    
    email_content = f"""
        <h2 style="color: #1f2937; text-align: center; margin-bottom: 15px;">¡Hola {entrada[8]} {entrada[9]}!</h2>
        <p style="color: #4b5563; font-size: 16px; line-height: 1.6; text-align: center;">
            Tu entrada para <strong>{entrada[4]}</strong>
        </p>
        <div style="text-align: center; margin: 25px 0;">
            <p style="color: #6366f1; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 15px 0;">Escaneá este código en la entrada</p>
            <div style="background-color: #ffffff; display: inline-block; padding: 15px; border-radius: 12px; border: 2px solid #6366f1;">
                <img src="{qr_url}" alt="Código QR" style="width: 180px; height: 180px; display: block; border: 0;">
            </div>
            <p style="color: #6366f1; font-size: 22px; font-weight: bold; margin: 15px 0 0 0; letter-spacing: 3px;">{codigo_qr}</p>
        </div>
        <div style="background-color: #f3f4f6; border-radius: 8px; padding: 20px; margin: 25px 0;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                        <strong style="color: #4b5563;">📅 Fecha:</strong>
                    </td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                        {fecha_formateada}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                        <strong style="color: #4b5563;">📍 Lugar:</strong>
                    </td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                        {entrada[6]}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db;">
                        <strong style="color: #4b5563;">🎟️ Entradas:</strong>
                    </td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #d1d5db; text-align: right; color: #1f2937;">
                        {entrada[1]} entrada{'' if entrada[1] == 1 else 's'}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 0;">
                        <strong style="color: #4b5563;">💵 Total:</strong>
                    </td>
                    <td style="padding: 10px 0; text-align: right; color: #10b981; font-weight: 800; font-size: 18px;">
                        ${entrada[2]:,.2f}
                    </td>
                </tr>
            </table>
        </div>
        <div style="text-align: center; padding: 12px; background-color: #dcfce7; border-radius: 8px; margin: 20px 0;">
            <p style="color: #166534; margin: 0; font-weight: 700; font-size: 16px;">✅ {entrada[3].upper()}</p>
        </div>
        <p style="color: #6b7280; font-size: 14px; text-align: center;">
            Presentá el código QR en la entrada del evento o mostrá este email en tu celular.
        </p>
    """
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
        <div style="text-align: center; margin-bottom: 25px; padding-bottom: 20px; border-bottom: 2px solid #e5e7eb;">
            <h1 style="color: #6366f1; font-size: 28px; margin: 0; font-weight: bold;">🎫 Get Access</h1>
        </div>
        {email_content}
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 25px 0;">
        <p style="color: #9ca3af; font-size: 12px; text-align: center;">© 2026 Get Access - Todos los derechos reservados</p>
    </div>
</body>
</html>"""
    
    try:
        url = BREVO_API_URL
        headers = {"api-key": BREVO_API_KEY, "Content-Type": "application/json"}
        data = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": entrada[7]}],
            "subject": f"🎫 Tu entrada para {entrada[4]} - Get Access",
            "htmlContent": html_content
        }
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 201:
            return {"message": "Ticket enviado", "email": entrada[7]}
        else:
            return {"message": "Error al enviar", "detail": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === CONTACTO ===
class ContactoRequest(BaseModel):
    nombre: str
    email: EmailStr
    asunto: str
    mensaje: str

@app.post("/api/contacto/enviar")
def enviar_mensaje_contacto(datos: ContactoRequest, db = Depends(get_db)):
    try:
        html_content = f"""
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 25px; padding-bottom: 20px; border-bottom: 2px solid #e5e7eb;">
                <h1 style="color: #6366f1; font-size: 28px; margin: 0; font-weight: bold;">📬 Nuevo Mensaje de Contacto - Get Access</h1>
            </div>
            <div style="background-color: #f3f4f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3 style="color: #1f2937; margin-top: 0;">📋 Datos del Contacto</h3>
                <p><strong>👤 Nombre:</strong> {datos.nombre}</p>
                <p><strong>📧 Email:</strong> {datos.email}</p>
                <p><strong>📝 Asunto:</strong> {datos.asunto}</p>
            </div>
            <div style="background-color: #ecfdf5; padding: 20px; border-radius: 10px;">
                <h3 style="color: #1f2937; margin-top: 0;">💬 Mensaje</h3>
                <p style="white-space: pre-wrap; line-height: 1.6;">{datos.mensaje}</p>
            </div>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 25px 0;">
            <p style="color: #9ca3af; font-size: 12px; text-align: center;">© 2026 Get Access - Sistema de Contacto</p>
        </div>
        """
        
        url = BREVO_API_URL
        headers = {"api-key": BREVO_API_KEY, "Content-Type": "application/json"}
        data = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": BREVO_SENDER_EMAIL}],
            "subject": f"📬 Nuevo mensaje de {datos.nombre} - {datos.asunto}",
            "htmlContent": html_content
        }
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 201:
            return {"message": "Mensaje enviado correctamente"}
        else:
            raise HTTPException(status_code=500, detail=f"Error al enviar email: {response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Initialize database
    if DATABASE_URL.startswith("postgresql"):
        # PostgreSQL - Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                password TEXT NOT NULL,
                verificado INTEGER DEFAULT 0,
                codigo_verificacion TEXT,
                rol TEXT DEFAULT 'usuario'
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id SERIAL PRIMARY KEY,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha TEXT,
                lugar TEXT,
                precio REAL,
                capacidad INTEGER DEFAULT 100,
                vendidos INTEGER DEFAULT 0,
                imagen TEXT,
                categoria TEXT,
                creado_por INTEGER
            )
        """)
        
        # Agregar columna si no existe
        try:
            cur.execute("ALTER TABLE eventos ADD COLUMN IF NOT EXISTS creado_por INTEGER")
        except:
            pass
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS evento_imagenes (
                id SERIAL PRIMARY KEY,
                evento_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                orden INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS entradas (
                id SERIAL PRIMARY KEY,
                evento_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                total REAL NOT NULL,
                estado TEXT DEFAULT 'comprada',
                preference_id TEXT UNIQUE,
                payment_id TEXT,
                creada_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usada INTEGER DEFAULT 0,
                transferida INTEGER DEFAULT 0,
                FOREIGN KEY (evento_id) REFERENCES eventos(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS validaciones (
                id SERIAL PRIMARY KEY,
                entrada_id INTEGER NOT NULL,
                scanner_id INTEGER NOT NULL,
                cantidad_original INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (entrada_id) REFERENCES entradas(id),
                FOREIGN KEY (scanner_id) REFERENCES usuarios(id)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transferencias (
                id SERIAL PRIMARY KEY,
                entrada_id INTEGER NOT NULL,
                usuario_origen INTEGER NOT NULL,
                usuario_destino INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accepted_at TIMESTAMP,
                FOREIGN KEY (entrada_id) REFERENCES entradas(id),
                FOREIGN KEY (usuario_origen) REFERENCES usuarios(id),
                FOREIGN KEY (usuario_destino) REFERENCES usuarios(id)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS password_reset (
                id SERIAL PRIMARY KEY,
                email TEXT NOT NULL,
                token TEXT UNIQUE NOT NULL,
                usado INTEGER DEFAULT 0,
                expires_at TIMESTAMP NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS solicitud_organizer (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                motivo_rechazo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS visitas (
                id SERIAL PRIMARY KEY,
                ip TEXT NOT NULL,
                fecha DATE DEFAULT CURRENT_DATE,
                contador INTEGER DEFAULT 1,
                UNIQUE(ip, fecha)
            )
        """)
        
        conn.commit()
        
        # Seed eventos if empty
        cur.execute("SELECT COUNT(*) FROM eventos")
        if cur.fetchone()[0] == 0:
            eventos_seed = [
                ("Coldplay - Music of the Spheres", "Gira mundial con producción spectacular. Ponte en órbita con Chris Martin y la banda.", "2026-06-15", "Estadio River Plate, Buenos Aires", 45000, 50000, 5000, DEFAULT_EVENT_IMAGES[0], "musica"),
                ("Flamenco en Buenos Aires", "Una noche mágica con los mejores artistas del flamenco español.", "2026-04-20", "Teatro Colón, Buenos Aires", 8500, 800, 150, DEFAULT_EVENT_IMAGES[1], "teatro"),
                ("Superclásico Boca vs River", "El partido más apasionante del fútbol mundial. No te lo pierdas!", "2026-05-10", "La Bombonera, Buenos Aires", 12000, 49000, 45000, DEFAULT_EVENT_IMAGES[2], "deportes"),
                ("Show de Stand Up - Fabian Pamberino", "El comediante más gracioso del país presenta su nuevo show.", "2026-04-05", "Teatro Metropolitan, Buenos Aires", 3500, 500, 200, DEFAULT_EVENT_IMAGES[3], "comedia"),
                ("Festival Electrónico 2026", "3 escenarios, 20 DJs internacionales, 12 horas de música continua.", "2026-07-20", "Rural Palermo, Buenos Aires", 8000, 15000, 8000, DEFAULT_EVENT_IMAGES[4], "musica"),
                ("Cirque du Soleil - O", "El espectáculo acuático más impresionante del mundo.", "2026-05-25", "Estadio GEBA, Buenos Aires", 12000, 3000, 1200, DEFAULT_EVENT_IMAGES[5], "espectaculo"),
                ("Conferencia Tech Summit 2026", "Los líderes tecnológicos del mundo comparten el futuro de la IA.", "2026-08-10", "Centro de Convenciones, Buenos Aires", 25000, 2000, 500, DEFAULT_EVENT_IMAGES[6], "conferencia"),
                ("Roger Waters - This Is Not A Drill", "El legendario líder de Pink Floyd presenta su gira de regreso.", "2026-09-15", "Estadio Monumental, Buenos Aires", 38000, 65000, 60000, DEFAULT_EVENT_IMAGES[7], "musica"),
            ]
            cur.executemany(
                "INSERT INTO eventos (nombre, descripcion, fecha, lugar, precio, capacidad, vendidos, imagen, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                eventos_seed
            )
            conn.commit()
            print(">>> Eventos de prueba creados en PostgreSQL")
        
        cur.close()
        conn.close()
    else:
        # SQLite - Desarrollo local
        conn = sqlite3.connect(DATABASE_URL)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                password TEXT NOT NULL,
                verificado INTEGER DEFAULT 0,
                codigo_verificacion TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha TEXT,
                lugar TEXT,
                precio REAL,
                capacidad INTEGER DEFAULT 100,
                vendidos INTEGER DEFAULT 0,
                imagen TEXT,
                categoria TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evento_imagenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evento_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                orden INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS validaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entrada_id INTEGER NOT NULL,
                scanner_id INTEGER NOT NULL,
                cantidad_original INTEGER,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (entrada_id) REFERENCES entradas(id),
                FOREIGN KEY (scanner_id) REFERENCES usuarios(id)
            )
        """)
        conn.commit()
        
        cursor = conn.execute("PRAGMA table_info(entradas)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'usada' not in columns:
            conn.execute("ALTER TABLE entradas ADD COLUMN usada INTEGER DEFAULT 0")
            conn.commit()
        
        cursor = conn.execute("PRAGMA table_info(usuarios)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'rol' not in columns:
            conn.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT DEFAULT 'usuario'")
            conn.commit()
        
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transferencias'")
        if not cursor.fetchone():
            conn.execute("""
                CREATE TABLE transferencias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entrada_id INTEGER NOT NULL,
                    usuario_origen INTEGER NOT NULL,
                    usuario_destino INTEGER NOT NULL,
                    token TEXT UNIQUE NOT NULL,
                    estado TEXT DEFAULT 'pendiente',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    accepted_at TEXT,
                    FOREIGN KEY (entrada_id) REFERENCES entradas(id),
                    FOREIGN KEY (usuario_origen) REFERENCES usuarios(id),
                    FOREIGN KEY (usuario_destino) REFERENCES usuarios(id)
                )
            """)
            conn.commit()
        
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='solicitud_organizer'")
        if not cursor.fetchone():
            conn.execute("""
                CREATE TABLE solicitud_organizer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    estado TEXT DEFAULT 'pendiente',
                    motivo_rechazo TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            """)
            conn.commit()

        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='visitas'")
        if not cursor.fetchone():
            conn.execute("""
                CREATE TABLE visitas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT NOT NULL,
                    fecha TEXT DEFAULT CURRENT_DATE,
                    contador INTEGER DEFAULT 1,
                    UNIQUE(ip, fecha)
            """)
            conn.commit()
        
        cursor = conn.execute("PRAGMA table_info(eventos)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'categoria' not in columns:
            conn.execute("ALTER TABLE eventos ADD COLUMN categoria TEXT")
            conn.commit()
        
        cursor = conn.execute("SELECT COUNT(*) FROM eventos")
        if cursor.fetchone()[0] == 0:
            eventos_seed = [
                ("Coldplay - Music of the Spheres", "Gira mundial con producción spectacular. Ponte en órbita con Chris Martin y la banda.", "2026-06-15", "Estadio River Plate, Buenos Aires", 45000, 50000, 5000, DEFAULT_EVENT_IMAGES[0], "musica"),
                ("Flamenco en Buenos Aires", "Una noche mágica con los mejores artistas del flamenco español.", "2026-04-20", "Teatro Colón, Buenos Aires", 8500, 800, 150, DEFAULT_EVENT_IMAGES[1], "teatro"),
                ("Superclásico Boca vs River", "El partido más apasionante del fútbol mundial. No te lo pierdas!", "2026-05-10", "La Bombonera, Buenos Aires", 12000, 49000, 45000, DEFAULT_EVENT_IMAGES[2], "deportes"),
                ("Show de Stand Up - Fabian Pamberino", "El comediante más gracioso del país presenta su nuevo show.", "2026-04-05", "Teatro Metropolitan, Buenos Aires", 3500, 500, 200, DEFAULT_EVENT_IMAGES[3], "comedia"),
                ("Festival Electrónico 2026", "3 escenarios, 20 DJs internacionales, 12 horas de música continua.", "2026-07-20", "Rural Palermo, Buenos Aires", 8000, 15000, 8000, DEFAULT_EVENT_IMAGES[4], "musica"),
                ("Cirque du Soleil - O", "El espectáculo acuático más impresionante del mundo.", "2026-05-25", "Estadio GEBA, Buenos Aires", 12000, 3000, 1200, DEFAULT_EVENT_IMAGES[5], "espectaculo"),
                ("Conferencia Tech Summit 2026", "Los líderes tecnológicos del mundo comparten el futuro de la IA.", "2026-08-10", "Centro de Convenciones, Buenos Aires", 25000, 2000, 500, DEFAULT_EVENT_IMAGES[6], "conferencia"),
                ("Roger Waters - This Is Not A Drill", "El legendario líder de Pink Floyd presenta su gira de regreso.", "2026-09-15", "Estadio Monumental, Buenos Aires", 38000, 65000, 60000, DEFAULT_EVENT_IMAGES[7], "musica"),
            ]
            conn.executemany(
                "INSERT INTO eventos (nombre, descripcion, fecha, lugar, precio, capacidad, vendidos, imagen, categoria) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                eventos_seed
            )
            conn.commit()
            print(">>> Eventos de prueba creados")
        
        conn.close()
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)