# Get Access - Configuración centralizada
# NO incluir este archivo en git (ya está en .gitignore)

import os
from pathlib import Path

# ============================================
# URLS DEL SITIO
# ============================================

# URL de producción (Render)
PRODUCTION_URL = "https://getaccess-d3um.onrender.com"

# URLs de desarrollo
DEV_URLS = [
    "http://localhost:3000",
    "https://192.168.1.40:3443",
    "http://localhost:8000",
    "https://localhost:8443",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# Puerto default para desarrollo
DEV_HTTP_PORT = 8000
DEV_HTTPS_PORT = 8443
FRONTEND_HTTP_PORT = 3000
FRONTEND_HTTPS_PORT = 3443

# ============================================
# APIs EXTERNAS
# ============================================

# Brevo (Email)
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "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")
BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL", "support.getaccess@gmail.com")
BREVO_SENDER_NAME = "Get Access"

# MercadoPago
MERCADOPAGO_API_URL = "https://api.mercadopago.com"
MERCADOPAGO_ACCESS_TOKEN = os.environ.get("MERCADO_PAGO_ACCESS_TOKEN", "APP_USR-2888302331727804-031609-eb4c51fc6c1654d701d4a5f3b24fbcd7-1921694")
MERCADOPAGO_WEBHOOK_SECRET = os.environ.get("MERCADO_PAGO_WEBHOOK_SECRET", "webhook_secret_fallback")

# Admin
ADMIN_SECRET = "access_on_admin_secret_2026"

# QuickChart (QR codes)
QUICKCHART_URL = "https://quickchart.io/qr"

# Logo para emails
EMAIL_LOGO_URL = "https://getaccess.now.sh/logo.png"

# Imágenes por defecto para eventos (seed de base de datos)
DEFAULT_EVENT_IMAGES = [
    "https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=800",  # musica
    "https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=800",   # teatro
    "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800",   # deportes
    "https://images.unsplash.com/photo-1527224857830-43a7acc85260?w=800",  # comedia
    "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800",  # musicaelectronica
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800",   # espectaculo
    "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800",  # conferencia
    "https://images.unsplash.com/photo-1598387993441-a364f854c3e1?w=800",   # musica
]

# ============================================
# SEGURIDAD
# ============================================

SECRET_KEY = os.environ.get("SECRET_KEY", "access_on_super_secret_key_2026_fallback")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS - Allowed origins
_allowed = os.environ.get("ALLOWED_ORIGINS", "")
if _allowed:
    ALLOWED_ORIGINS = _allowed.split(",")
else:
    ALLOWED_ORIGINS = DEV_URLS + [PRODUCTION_URL]

# Rate Limiting
RATE_LIMIT_WINDOW = 60  # segundos
RATE_LIMIT_MAX = 100    # requests por ventana

# ============================================
# BASE DE DATOS
# ============================================

DATABASE_URL = "access_on.db"

# ============================================
# RUTAS DE ARCHIVOS
# ============================================

# Obtener directorio del archivo actual
BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
IMAGES_DIR = FRONTEND_DIR / "images"