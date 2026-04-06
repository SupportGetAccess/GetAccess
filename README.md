# Eventos Tickets - Sitio Completo

Sitio web completo para compra de entradas a eventos con:
- ✅ **Frontend**: React (embebido en HTML)
- ✅ **Backend**: FastAPI con Python
- ✅ **Autenticación**: JWT (tokens seguros)
- ✅ **Pagos**: Integración con MercadoPago
- ✅ **Email**: Envío de tickets por correo

## Estructura

```
eventos_tickets_full/
├── backend/
│   ├── main.py          # API completa
│   └── requirements.txt # Dependencias
└── frontend/
    └── index.html       # App React
```

## Instalación y Ejecución

### 1. Instalar dependencias del backend

```powershell
cd C:\Users\guill\eventos_tickets_full\backend
pip install -r requirements.txt
```

### 2. Iniciar el servidor

```powershell
python -m uvicorn main:app --reload --port 8000
```

El servidor estará en: http://localhost:8000

### 3. Abrir el frontend

Abrir en navegador:
```
C:\Users\guill\eventos_tickets_full\frontend\index.html
```

O arrastrar el archivo al navegador.

---

## Funcionalidades

### Autenticación JWT
- Registro de usuarios con email y contraseña
- Login con token JWT
- Sesión persistente (localStorage)
- Endpoint: `/api/auth/registro`, `/api/auth/login`, `/api/auth/me`

### Eventos
- Listar todos los eventos
- Ver detalle de evento
- Crear evento (requiere auth)
- Endpoint: `/api/eventos/`

### Compra de Entradas
- Seleccionar cantidad
- Crear preferencia de pago MercadoPago
- Simulación de checkout
- Endpoint: `/api/entradas/`, `/api/pagos/crear-preferencia`

### Email
- Enviar ticket por email
- Simulación (listo para integrar con SendGrid/SMTP)
- Endpoint: `/api/email/enviar-ticket`

---

## API Endpoints

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | / | Raíz API | No |
| POST | /api/auth/registro | Registrarse | No |
| POST | /api/auth/login | Iniciar sesión | No |
| GET | /api/auth/me | Datos usuario actual | Sí |
| GET | /api/eventos/ | Listar eventos | No |
| POST | /api/eventos/ | Crear evento | Sí |
| GET | /api/entradas/ | Mis entradas | Sí |
| POST | /api/entradas/ | Comprar entrada | Sí |
| POST | /api/pagos/crear-preferencia | Generar pago MP | Sí |
| POST | /api/email/enviar-ticket | Enviar ticket | Sí |

---

## MercadoPago - Integración Real

### Paso 1: Obtener credenciales
1. Ve a [MercadoPago Developers](https://www.mercadopago.com.ar/developers/)
2. Crea una cuenta o usa una existente
3. En "Mis Apps", crea una nueva aplicación
4. Copia el **Access Token** de prueba (TEST_ACCESS_TOKEN)

### Paso 2: Configurar en el backend
Edita el archivo `backend/main.py` y reemplaza:

```python
MERCADO_PAGO_ACCESS_TOKEN = "TU_ACCESS_TOKEN_AQUI"
```

Por tu token real:

```python
MERCADO_PAGO_ACCESS_TOKEN = "APP_USR-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Paso 3: Probar
1. Inicia el backend: `python -m uvicorn main:app --reload`
2. Inicia el frontend
3. Compra una entrada - ahora redirigirá a MercadoPago real
4. Usa las tarjetas de prueba de MercadoPago:
   - Número: 4509 9535 0134 9620
   - CVV: 123
   - Vencimiento: cualquier fecha futura

### Notas
- El frontend detectará automáticamente si hay un token configurado
- Si el token no está configurado, funciona en modo simulación
- Los callbacks (success/failure) actualizan automáticamente el estado de las entradas

```python
import mercadopago

sdk = mercadopago.SDK("TU_ACCESS_TOKEN")

def crear_preferencia(entrada, evento, usuario):
    preference_data = {
        "items": [{
            "title": evento["nombre"],
            "quantity": entrada["cantidad"],
            "unit_price": evento["precio"],
            "currency_id": "ARS"
        }],
        "payer": {
            "email": usuario["email"]
        },
        "back_urls": {
            "success": "http://tu-sitio.com/exito",
            "failure": "http://tu-sitio.com/fallo"
        }
    }
    
    result = sdk.preference().create(preference_data)
    return result["response"]["init_point"]
```

---

## Email - Configuración

Para producción, usar SMTP o servicios como:
- SendGrid
- Resend
- Mailgun

Ejemplo con SMTP:

```python
import smtplib
from email.mime.text import MIMEText

def enviar_ticket_email(email, entrada, evento):
    msg = MIMEText(f"""
    ¡Gracias por tu compra!
    
    Evento: {evento['nombre']}
    Fecha: {evento['fecha']}
    Lugar: {evento['lugar']}
    Cantidad: {entrada['cantidad']}
    Total: ${entrada['total']}
    
    Tu código de entrada: #{entrada['id']}
    """)
    
    msg["Subject"] = f"Tu entrada para {evento['nombre']}"
    msg["From"] = "tickets@tusitio.com"
    msg["To"] = email
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("tu@email.com", "tu_password")
        server.send_message(msg)
```

---

## Datos de prueba

El sistema incluye 3 eventos de ejemplo:
1. Festival de Música 2026 - $15.000
2. Concierto de Rock - $8.000
3. Show de Comedia - $3.500
