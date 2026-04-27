# Get Access - Proyecto de Entradas

⚠️⚠️⚠️ IMPORTANTE: SIEMPRE PRODUCCIÓN, NUNCA LOCAL - NO TRABAJAMOS EN MODO LOCAL ⚠️⚠️⚠️

⚠️⚠️⚠️ IMPORTANTE: Cada vez que hagas UNA SOLA modificación en cualquier archivo (backend/main.py, frontend/*.html), DEBES reiniciar los servicios antes de decir "Listo" o "Listo, servicios iniciados". Si no lo haces, el usuario no podrá probar los cambios. ⚠️⚠️⚠️

## 🏭 PRUEBAS EN PRODUCCIÓN - NO HAY LOCAL
**TODAS las pruebas se realizan en producción:** https://getaccess.com.ar
- NO se prueba en localhost
- NO se hace debug local
- Solo se desarrolla local y se sube a producción para probar
- ** Siempre dar URLs de PRODUCCIÓN al usuario, nunca localhost**

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

## URLs
### Solo Producción
- **Frontend**: https://getaccess.com.ar
- **Scanner**: https://getaccess.com.ar/scanner.html
- **Backend**: https://getaccess-d3um.onrender.com

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
Cada vez que se modifique el scanner (scanner.html), DEBO enviar las URLs de producción al usuario:
- **Producción**: https://getaccess.com.ar/scanner.html

## ⚠️ REGLA: CERRAR SESIÓN
Cuando el usuario diga **"Cerrar sesión"** o indique que terminó la sesión de trabajo, DEBO:

1. **Guardar notas en `notas.txt`**: Actualizar el archivo C:\Users\guill\eventos_tickets_full\notas.txt con:
   - Fecha de la sesión
   - Cambios realizados
   - Estado actual del proyecto
   - Problemas pendientes
   - Próximos pasos sugeridos

2. **Confirmar que ambos servicios están corriendo**

---

## 🐛 ERRORES COMUNES DE JSX

### Error: "Expected corresponding JSX closing tag"
Este error ocurre cuando hay un desbalanceo en los tags de apertura y cierre en JSX.

**Causa comunes:**
1. Cerrar un div多余的 (sobra un tag de cierre)
2. Olvidar cerrar un tag
3. Estructura de tags mal anidada

**Cómo evitarlo:**
- Cada `<div>` de apertura debe tener su `</div>` de cierre
- Cada `<>` (fragment) debe cerrar con `</>`
- Verificar indentación al hacer cambios en componentes JSX
- Usar el comando "Check syntax" antes de commit si está disponible

**Ejemplo de error típico:**
```jsx
// ❌ MAL - tiene un </div> de más
<div>
    <form>...</form>
    </div>    // <- ESTE SOBRA
</div>

// ✅ BIEN
<div>
    <form>...</form>
</div>
```

