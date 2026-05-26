# PLAN.md — App Mobile Get Access (Spec-Driven Development)

## 1. CONSTITUCIÓN

### Stack tecnológico (innegociable)

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Framework | Expo SDK | ~56.0.3 |
| UI | React Native | 0.85.3 |
| Navegación | Expo Router | ~56.2.5 |
| Lenguaje | TypeScript | ~6.0.3 (strict) |
| Estado global | Zustand | ^5.0.13 |
| Server state | TanStack React Query | ^5.100.11 |
| HTTP | axios | ^1.16.1 |
| Almacén seguro | expo-secure-store | ~56.0.4 |
| Cámara | expo-camera | ~56.0.7 |
| QR | react-native-qrcode-svg | ^6.3.21 |
| Íconos | @expo/vector-icons | ^15.0.2 |
| Web browser | expo-web-browser | ~56.0.5 |
| Notificaciones | expo-notifications | ~56.0.12 |
| Gestos | react-native-gesture-handler | ~2.31.1 |
| Animaciones | react-native-reanimated | 4.3.1 |
| Splash | expo-splash-screen | ~56.0.9 |

### Convenciones de código

- **Archivos**: PascalCase para componentes (`EventoCard.tsx`), camelCase para módulos/api (`authStore.ts`)
- **Estilos**: Siempre `StyleSheet.create()` al final del archivo, nunca inline
- **Componentes**: Solo funcionales con hooks, nada de clases
- **Imports**: Orden — React/librerías externas → módulos internos → types → estilos
- **Tipado**: `strict: true`. Todo tipo definido en `types/index.ts`. Sin `any` (excepto catch de errores)
- **Naming stores**: Prefijo `use` + nombre + `Store` (ej: `useAuthStore`, `useCartStore`)
- **Naming queries**: queryKey con strings planas (`['eventos']`, `['entrada', id]`)

### Prohibido

- ❌ Redux, MobX o cualquier state manager que no sea Zustand
- ❌ Clases React (Component, PureComponent)
- ❌ Tailwind CSS, styled-components o CSS modules — solo StyleSheet
- ❌ `any` en tipos (salvo catch blocks)
- ❌ Dependencias sin verificar compatibilidad con Expo SDK 56
- ❌ Código sin type-check (`npx tsc --noEmit` debe pasar)
- ❌ Comentarios explicativos en código (el código debe ser auto-documentado)
- ❌ Hardcode de URLs de API (usar `app.json` → `extra.apiUrl`)
- ❌ Almacenar tokens en AsyncStorage o state — solo SecureStore
- ❌ Fetch directo sin pasar por `api/client.ts` (pierde interceptor de token)

---

## 2. ESPECIFICACIÓN

### 2.1 Visión General

App mobile del sistema **Get Access** — plataforma de venta de entradas para eventos. Consume la API REST existente en `https://getaccess.com.ar`. La app replica las funcionalidades del frontend web (`frontend/index.html`) adaptadas a mobile nativo.

### 2.2 Roles de Usuario

| Rol | Permisos |
|-----|----------|
| `usuario` | Ver eventos, comprar entradas, ver mis entradas, transferir, editar perfil |
| `organizer` | Todo lo de usuario + crear/administrar sus eventos, escanear QR |
| `admin` | Todo lo de organizer + gestionar solicitudes de rol, dashboard global |

### 2.3 Flujos de Negocio

#### FLUJO A: Compra con registro
```
Login (si no está logueado) → Navegar eventos → Seleccionar evento
→ Elegir cantidad → Agregar al carrito → Ir al carrito
→ Elegir método de pago (QR o Link) → Pagar
→ Confirmación → Entrada disponible en "Mis Entradas"
```

#### FLUJO B: Compra como invitado (sin registro)
```
Navegar eventos → Seleccionar evento → Elegir cantidad
→ Agregar al carrito (redirige a carrito automáticamente)
→ Completar datos del comprador (nombre, apellido, email, repetir email, teléfono)
→ Elegir método de pago → Pagar
→ Confirmación → Email con entrada
→ Puede buscar entradas por email en "Buscar Mis Entradas"
```

#### FLUJO C: Validación de entrada (admin/organizer)
```
Abrir scanner → Escanear QR de entrada → API valida el código
→ Feedback visual + vibratorio (verde = válida, rojo = inválida)
```

#### FLUJO D: Admin/Organizer
```
Panel Admin → Menú con opciones según rol
→ Dashboard (stats generales)
→ Mis Eventos (lista con editar/eliminar)
→ Crear Evento (formulario completo)
→ Solicitudes (solo admin: aceptar/rechazar solicitudes organizer)
→ Validaciones (historial de escaneos)
```

### 2.4 Reglas de Negocio

1. **Disponibilidad**: No se puede comprar más entradas que `capacidad - vendidos`
2. **Expiración**: Las entradas pendientes expiran a los 20 min (manejado por backend)
3. **Comisión**: El precio final incluye comisión del evento: `precio * (1 + comision/100)`
4. **Pago QR**: Tiene countdown de 10 min con polling cada 3s al backend
5. **Invitado**: Los datos del comprador se guardan en la entrada (no se crea usuario)
6. **Código único**: Cada entrada pagada recibe un código GA-XXXXX
7. **Transferencia**: Solo usuarios registrados pueden transferir entradas

### 2.5 Restricciones Técnicas

- **API URL**: `https://getaccess.com.ar` (configurable en `app.json` → `extra.apiUrl`)
- **Endpoints**: Todos con prefijo `/api/`. Autenticación via `Authorization: Bearer <token>`
- **Tokens**: Almacenados en SecureStore, se borran al hacer logout o en 401
- **Sesión**: Se restaura al abrir la app leyendo SecureStore
- **Imágenes**: Los eventos pueden tener imágenes como string URL o array JSON

### 2.6 Pantallas (Sitemap)

```
Root Layout (Stack)
├── (tabs)
│   ├── eventos        → Lista de eventos
│   ├── entradas       → Mis Entradas (requiere auth)
│   ├── carrito        → Carrito de compras
│   └── perfil         → Perfil del usuario (requiere auth)
├── (auth)
│   ├── login          → Iniciar sesión
│   └── register       → Registro + verificación
├── evento/[id]        → Detalle de evento + agregar al carrito
├── carrito/index      → Checkout (QR o Link de pago)
├── entrada/[id]       → Detalle de entrada con QR
├── scanner/index      → Escáner QR (admin/organizer)
├── admin
│   ├── index          → Menú del panel admin
│   ├── dashboard      → Estadísticas
│   ├── mis-eventos    → Lista de eventos propios
│   ├── crear-evento   → Formulario de nuevo evento
│   ├── solicitudes    → Solicitudes de rol organizer (admin only)
│   └── validaciones   → Historial de escaneos
├── buscar-entradas    → Buscar por email
├── contacto           → Formulario de contacto
├── editar-perfil      → Editar nombre/apellido
└── recuperar-password → Solicitar/reset contraseña
```

---

## 3. PLAN Y TAREAS

### FASE 0: Proyecto Base (✅ YA IMPLEMENTADO)

| # | Tarea | Archivo | Estado |
|---|-------|---------|--------|
| 0.1 | Configurar Expo SDK 56 + TypeScript strict | `app.json`, `tsconfig.json` | ✅ |
| 0.2 | Definir tema oscuro | `theme/colors.ts` | ✅ |
| 0.3 | Definir tipos compartidos | `types/index.ts` | ✅ |
| 0.4 | Configurar API client con interceptores | `api/client.ts` | ✅ |
| 0.5 | Implementar stores (auth + cart) | `stores/` | ✅ |
| 0.6 | Layout raíz con providers | `app/_layout.tsx` | ✅ |
| 0.7 | Configurar EAS Build | `eas.json` | ✅ |
| 0.8 | Generar APK de prueba | via EAS Build | ✅ |

### FASE 1: Autenticación (✅ YA IMPLEMENTADO)

| # | Tarea | Archivo | Estado |
|---|-------|---------|--------|
| 1.1 | Pantalla de login | `app/(auth)/login.tsx` | ✅ |
| 1.2 | Pantalla de registro + verificación | `app/(auth)/register.tsx` | ✅ |
| 1.3 | Recuperar contraseña | `app/recuperar-password/index.tsx` | ✅ |
| 1.4 | Perfil de usuario | `app/(tabs)/perfil.tsx` | ✅ |
| 1.5 | Editar perfil | `app/editar-perfil/index.tsx` | ✅ |
| 1.6 | API de autenticación | `api/auth.ts` | ✅ |

### FASE 2: Eventos y Compra (✅ YA IMPLEMENTADO)

| # | Tarea | Archivo | Estado |
|---|-------|---------|--------|
| 2.1 | Listado de eventos | `app/(tabs)/eventos.tsx` | ✅ |
| 2.2 | Detalle de evento con selector de cantidad | `app/evento/[id].tsx` | ✅ |
| 2.3 | API de eventos | `api/eventos.ts` | ✅ |
| 2.4 | API de pagos | `api/pagos.ts` | ✅ |

### FASE 3: Carrito y Pago (✅ YA IMPLEMENTADO)

| # | Tarea | Archivo | Estado |
|---|-------|---------|--------|
| 3.1 | Tab de carrito con items y cantidades | `app/(tabs)/carrito.tsx` | ✅ |
| 3.2 | Checkout con selección QR/Link | `app/carrito/index.tsx` | ✅ |
| 3.3 | Formulario de datos del comprador (invitado) | `app/carrito/index.tsx` | ✅ |
| 3.4 | Renderizado de QR + polling de estado | `app/carrito/index.tsx` | ✅ |
| 3.5 | Apertura de link de pago con WebBrowser | `app/carrito/index.tsx` | ✅ |

### FASE 4: Entradas (✅ YA IMPLEMENTADO)

| # | Tarea | Archivo | Estado |
|---|-------|---------|--------|
| 4.1 | Mis Entradas con filtro pagadas/pendientes | `app/(tabs)/entradas.tsx` | ✅ |
| 4.2 | Detalle de entrada con QR dinámico | `app/entrada/[id].tsx` | ✅ |
| 4.3 | Compartir entrada | `app/entrada/[id].tsx` | ✅ |
| 4.4 | Buscar entradas por email | `app/buscar-entradas/index.tsx` | ✅ |
| 4.5 | API de entradas | `api/entradas.ts` | ✅ |

### FASE 5: Scanner QR (✅ YA IMPLEMENTADO)

| # | Tarea | Archivo | Estado |
|---|-------|---------|--------|
| 5.1 | Solicitar permiso de cámara | `app/scanner/index.tsx` | ✅ |
| 5.2 | Escaneo de QR + validación | `app/scanner/index.tsx` | ✅ |
| 5.3 | Feedback visual y vibratorio | `app/scanner/index.tsx` | ✅ |

### FASE 6: Panel Admin (✅ COMPLETADO — 21 MAY 2026)

| # | Tarea | Archivo | API | Esfuerzo |
|---|-------|---------|-----|----------|
| 6.1 | **Dashboard** — Stats: entradas vendidas, ingresos, tickets usados, precio promedio, top eventos, por categoría, proyección | `app/admin/dashboard/index.tsx` | `GET /api/analytics/general` | 1h |
| 6.2 | **Crear Evento** — Formulario con nombre, descripción, fecha, hora, lugar, precio, capacidad, categoría, comisión, subida de imágenes (picker) | `app/admin/crear-evento/index.tsx` | `POST /api/eventos/`, `PUT /api/eventos/{id}` | 3h |
| 6.3 | **Mis Eventos** — Lista de eventos propios con editar (navega precargado) y eliminar | `app/admin/mis-eventos/index.tsx` | `GET /api/eventos/?mis_eventos=true`, `DELETE /api/eventos/{id}` | 1.5h |
| 6.4 | **Solicitudes Organizer** — Solo admin. Lista con botones aprobar/rechazar | `app/admin/solicitudes/index.tsx` | `GET /api/admin/solicitudes-organizer`, `POST /api/admin/aprobar-organizer`, `POST /api/admin/rechazar-organizer` | 1.5h |
| 6.5 | **Validaciones** — Historial de escaneos de los últimos 7 días | `app/admin/validaciones/index.tsx` | `GET /api/validaciones/historial` | 1h |

**Total Fase 6:** ~8h de desarrollo

### FASE 7: Mejoras Post-MVP (✅ COMPLETADA — 22 MAY 2026)

| # | Tarea | Archivos | Estado |
|---|-------|---------|--------|
| 7.1 | Carga real de imágenes de eventos | `utils/format.ts`, `app/(tabs)/eventos.tsx`, `app/evento/[id].tsx` | ✅ |
| 7.2 | Pull-to-refresh en listas | `app/(tabs)/eventos.tsx`, `app/(tabs)/entradas.tsx` | ✅ |
| 7.3 | Deep linking para recuperar contraseña | `app/_layout.tsx`, `app/recuperar-password/index.tsx` | ✅ |
| 7.4 | Notificaciones push | `utils/notifications.ts`, `app/_layout.tsx` | ✅ |
| 7.5 | Offline support (React Query persist) | `app/_layout.tsx` + `@tanstack/react-query-persist-client` | ✅ |
| 7.6 | Transferencia de entradas | `app/entrada/[id].tsx`, `app/transferencias-pendientes/index.tsx`, `app/(tabs)/perfil.tsx` | ✅ |
| 7.7 | Modo oscuro consistente | Ya implementado | ✅ |
| 7.8 | Logo transparente, emoji avatar, auth routing, sort eventos | `app/(tabs)/eventos.tsx` | ✅ |
| 7.9 | Fix QR doble wrapping | `app/checkout/index.tsx` | ✅ |
| 7.10 | SafeArea footers (evento + carrito + checkout) | `app/evento/[id].tsx`, `app/(tabs)/carrito.tsx` | ✅ |
| 7.11 | Política de Privacidad — screen + ruta + menu item | `app/privacidad/index.tsx`, `app/_layout.tsx`, `app/(tabs)/perfil.tsx` | ✅ |

### Nuevos paquetes instalados
- `@tanstack/react-query-persist-client` — persistencia de React Query
- `@tanstack/query-async-storage-persister` — persister con AsyncStorage
- `@react-native-async-storage/async-storage` — almacenamiento offline

### Nuevas pantallas
- `app/transferencias-pendientes/index.tsx` — aceptar/rechazar transferencias entrantes
- `app/privacidad/index.tsx` — política de privacidad

### Nuevos módulos API
- `POST /api/auth/push-token` — registro de push token (requiere implementación en backend)

---

## 4. IMPLEMENTACIÓN

### 4.1 Metodología

Cada tarea sigue este proceso estricto:

```
1. LEER este PLAN.md → entender el contexto y especificación
2. LEER el archivo existente (si es una modificación) o la pantalla análoga más cercana
3. LEER el API module correspondiente (`api/*.ts`) para conocer endpoints disponibles
4. LEER `types/index.ts` para conocer los tipos de datos
5. REVISAR pantallas similares como referencia de estilo y patrones
6. IMPLEMENTAR el componente siguiendo las convenciones de código
7. VERIFICAR con `npx tsc --noEmit` (type-check)
8. VERIFICAR contra la especificación en sección 2
```

### 4.2 Patrón de Componente

Todo componente nuevo debe seguir esta estructura:

```tsx
import { View, Text, ... } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../../theme';
import { formatPrecio, parseFecha } from '../../../utils/format';

export default function NombreScreen() {
  // 1. Hooks de estado / store
  // 2. React Query (si aplica)
  // 3. Handlers
  // 4. Loading / Error / Empty states
  // 5. Render principal
}

const styles = StyleSheet.create({
  // ... estilos consistentes con el tema
});
```

### 4.3 Manejo de Estados

Toda pantalla con datos async debe manejar explícitamente:

- **Loading**: `ActivityIndicator` con color `colors.primary` centrado
- **Error**: Ícono + mensaje + opción de reintentar
- **Empty**: Ícono + mensaje descriptivo
- **Success**: Renderizado normal de datos

### 4.4 Navegación

- `router.push()` para navegación hacia adelante
- `router.back()` para volver
- `router.replace()` para redirecciones post-login/registro
- `router.push('/(tabs)/eventos')` para tabs
- Parámetros de ruta: `router.push(`/evento/${id}`)`

---

## 5. VERIFICACIÓN Y MANTENIMIENTO

### 5.1 Type Checking

```bash
npx tsc --noEmit
```
Debe pasar sin errores antes de cualquier commit o build.

### 5.2 Build de Prueba (APK)

```bash
eas build -p android --profile preview
```
Genera APK instalable para pruebas en dispositivo real.

### 5.3 Verificación contra Especificación

Cada feature implementada debe cumplir:

- [ ] ¿Coincide con el flujo descrito en sección 2.3?
- [ ] ¿Respeta las reglas de negocio en sección 2.4?
- [ ] ¿Maneja correctamente auth requerida / no requerida?
- [ ] ¿Muestra loading/error/empty según sección 4.3?
- [ ] ¿Pasa type-check?
- [ ] ¿Usa la API endpoint correcto?

### 5.4 Actualización del Documento

- Si la lógica de negocio cambia en el backend → actualizar sección 2 de este documento
- Si se agregan nuevas dependencias → actualizar sección 1
- Si se completan tareas → marcar como ✅
- Si se descubren bugs o mejoras → agregar a Fase 7

### 5.5 Commits

Siguiendo `AGENTS.md`:
```bash
git add -A
git commit -m "tipo: descripción"
git push
```

---

## 6. COMPARATIVA WEB VS MOBILE — PENDIENTES

Funcionalidades del frontend web (`frontend/index.html`) que faltan en la app mobile, priorizadas por esfuerzo:

| # | Tarea | Archivos afectados | Esfuerzo | Prioridad |
|---|-------|-------------------|----------|-----------|
| 6.1 | Buscar eventos por texto + filtro categorías | `app/(tabs)/eventos.tsx` | 1h | Alta |
| 6.2 | Solicitar ser Organizer desde Perfil | `app/(tabs)/perfil.tsx` | 30min | Alta |
| 6.3 | Reenviar ticket por email | `app/(tabs)/entradas.tsx` + `api/entradas.ts` | 30min | Media |
| 6.4 | Carrusel de imágenes en detalle de evento | `app/evento/[id].tsx` | 1h | Media |
| 6.5 | Admin imágenes desde detalle evento (subir/eliminar) | `app/evento/[id].tsx` | 1h | Baja |
| 6.6 | Panel de visitas (admin) | `app/admin/visitas/index.tsx` + `api/admin.ts` + `app/admin/index.tsx` | 1h | Baja |

---

*Documento generado: 22 de Mayo 2026*
*Metodología: Spec-Driven Development (SDD)*
*Proyecto: Get Access — App Mobile*
