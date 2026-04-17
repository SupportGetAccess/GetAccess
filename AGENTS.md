# Get Access - Proyecto de Entradas

⚠️⚠️⚠️ IMPORTANTE: Cada vez que hagas UNA SOLA modificación en cualquier archivo (backend/main.py, frontend/*.html), DEBES reiniciar los servicios antes de decir "Listo" o "Listo, servicios iniciados". Si no lo haces, el usuario no podrá probar los cambios. ⚠️⚠️⚠️

## 🏭 PRUEBAS EN PRODUCCIÓN - NO HAY LOCAL
**TODAS las pruebas se realizan en producción:** https://getaccess.com.ar
- NO se prueba en localhost
- NO se hace debug local
- Solo se desarrolla local y se sube a producción para probar

## URLs de Producción
- **Frontend**: https://getaccess.com.ar
- **Scanner**: https://getaccess.com.ar/scanner.html
- **Backend API**: https://getaccess-d3um.onrender.com (solo para API/webhooks)

## Estructura del Proyecto
- **Backend**: C:\Users\guill\eventos_tickets_full\backend\main.py
- **Frontend**: C:\Users\guill\eventos_tickets_full\frontend\index.html
- **Scanner QR**: C:\Users\guill\eventos_tickets_full\frontend\scanner.html
- **Servidor frontend**: C:\Users\guill\eventos_tickets_full\frontend\serve.py
- **Base de datos**: C:\Users\guill\eventos_tickets_full\backend\access_on.db

## ⚠️ REGLA: ANÁLISIS DE IMPACTO EN CAMBIOS
**Cada vez que el usuario pida una modificación o implementación nueva, DEBO:**

1. **Evaluar el impacto**: Antes de hacer cualquier cambio, analizar si puede alterar el funcionamiento correcto del sitio.

2. **Si no estás seguro**: Si no tienes certeza del 100% de que el cambio es seguro, directamente enviarás un comentario diciendo: **"No sé si esto es 100% seguro - necesita verificación"** y esperarás confirmación del usuario.

3. **No asumir**: No asumas que un cambio es seguro sin verificarlo. Siempre consulta si tenés dudas.

4. **Documentar riesgos**: Si identificás posibles problemas, comunicarlos claramente al usuario antes de proceder.

---

## ⚠️ REGLA IMPORTANTE
**Cada vez que el usuario pida una modificación o implementación nueva, se deben reiniciar TODOS los servicios (backend y frontend).**

**SIEMPRE que se reinicie el backend O el frontend, se deben reiniciar TODOS los servicios (HTTP y HTTPS).**

**TAMBIEN: Cada vez que se modifique el frontend (archivos HTML/CSS/JS), se deben reiniciar TODOS los servicios.**

Para reiniciar todos los servicios en Windows PowerShell:
```powershell
# 1. Matar todos los procesos Python
powershell -Command "Stop-Process -Name python -Force -ErrorAction SilentlyContinue"

# 2. Iniciar backend HTTP (Puerto 8000)
powershell -Command "Start-Process python -ArgumentList '-m','uvicorn','main:app','--host','0.0.0.0','--port','8000' -WorkingDirectory 'C:\Users\guill\eventos_tickets_full\backend'"

# 3. Iniciar backend HTTPS (Puerto 8443)
powershell -Command "Start-Process python -ArgumentList 'C:/Users/guill/eventos_tickets_full/backend/serve_https.py'"

# 4. Iniciar frontend HTTP (Puerto 3000)
powershell -Command "Start-Process python -ArgumentList 'C:/Users/guill/eventos_tickets_full/frontend/serve.py'"

# 5. Verificar
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:8000/health' -UseBasicParsing | Select-Object -ExpandProperty StatusCode"
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:3000/' -UseBasicParsing | Select-Object -ExpandProperty StatusCode"
```

## URLs
### PC (localhost - HTTP)
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Scanner QR: http://localhost:3000/scanner.html

### Celular (Red local - HTTPS)
- Frontend: https://192.168.1.40:3443
- Backend API: https://192.168.1.40:8443
- Scanner QR: https://192.168.1.40:3443/scanner.html

## Credenciales
- Las credenciales de admin están en las variables de entorno del sistema
- Para hacer admin a un usuario: `UPDATE usuarios SET rol='admin' WHERE email='email'`

## Nombre del sitio: Get Access
- En frontend: buscar y reemplazar "Access ON" por "Get Access"
- En backend: BREVO_SENDER_NAME = "Get Access"

## 🔒 REGLA: ANÁLISIS DE SEGURIDAD
**Cada vez que se implemente una nueva funcionalidad, DEBO:**

1. **Analizar vulnerabilidades potenciales** de la nueva funcionalidad:
   - Inyección SQL en queries dinámicas
   - Falta de autenticación/autorización en endpoints
   - Exposición de datos sensibles
   - Validación insuficiente de inputs
   - Rate limiting ausente en endpoints públicos
   - Almacenamiento de tokens/sesiones (usar sessionStorage para cerrar sesión al cerrar navegador)

2. **Sugerir tareas de seguridad** al usuario antes de finalizar:
   - ¿Hay endpoints que requieren autenticación JWT?
   - ¿Se necesita validación de roles (admin/usuario)?
   - ¿Hay inputs de usuario que deben sanitizarse?
   - ¿Se debe agregar rate limiting?
   - ¿El CORS está correctamente configurado?
   - ¿Hay secretos/keys hardcodeadas a mover a variables de entorno?

3. **Ejemplo de respuesta esperada:**
   ```
   "Esta funcionalidad añade /api/nueva-ruta. Seguridad a verificar:
   - [ ] ¿Requiere auth? → Agregar Depends(security)
   - [ ] ¿Solo admin? → Agregar verificación es_admin()
   - [ ] ¿Input público? → Agregar validación de datos
   - [ ] ¿Endpoint masivo? → Agregar rate limiting"
   ```

## 🔐 REGLA: ALMACENAMIENTO SEGURO DE CREDENCIALES

**NUNCA almacenar credenciales directamente en el código fuente.**

1. **Variables de entorno**: Usar `os.environ.get()` para acceder a secrets
   ```python
   # ✅ Correcto
   SECRET_KEY = os.environ.get("SECRET_KEY", "fallback")
   
   # ❌ Incorrecto
   SECRET_KEY = "hardcoded_secret"
   ```

2. **Secrets a proteger**:
   - Claves API (Brevo, MercadoPago, etc.)
   - Keys de JWT
   - Credenciales de base de datos
   - Tokens de-webhook

3. **En producción**: Usar servicios de gestión de secrets (AWS Secrets Manager, HashiCorp Vault, etc.)

4. **Contraseñas**: Usar bcrypt con salt para hash (ya implementado)

## 📱 REGLA: MODIFICACIONES AL SCANNER QR
Cada vez que se modifique el scanner (scanner.html), DEBO enviar las URLs de prueba al usuario:
- **PC**: http://localhost:3000/scanner.html
- **Celular**: https://192.168.1.40:3443/scanner.html

## ⚠️ REGLA: CERRAR SESIÓN
Cuando el usuario diga **"Cerrar sesión"** o indique que terminó la sesión de trabajo, DEBO:

1. **Guardar notas en `notas.txt`**: Actualizar el archivo C:\Users\guill\eventos_tickets_full\notas.txt con:
   - Fecha de la sesión
   - Cambios realizados
   - Estado actual del proyecto
   - Problemas pendientes
   - Próximos pasos sugeridos

2. **Confirmar que ambos servicios están corriendo**

