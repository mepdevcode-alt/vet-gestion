# Prompt Final – Sistema de Gestión Veterinaria

## Instrucción principal
Eres un desarrollador Fullstack Senior con experiencia en Python y Django. Tu tarea es generar una aplicación web completa para una clínica veterinaria. El sistema debe ser robusto, seguro y con una interfaz moderna y profesional. Todo el código, variables, comentarios e interfaz deben estar **en español**.

---

## Stack tecnológico
- **Backend:** Python 3.x con Django 4.2+
- **Base de datos:** Dual — SQLite para desarrollo / PostgreSQL para producción (controlado por variable de entorno `MODO_BD` en `.env`)
- **Frontend:** Django Templates + Tailwind CSS (via CDN)

---

## Roles y Seguridad (Crítico)

| Rol | Permisos |
|---|---|
| **Administrador** | Control total: usuarios, mascotas, historial, turnos, facturación |
| **Veterinario** | Gestión de mascotas, historias médicas y creación de dueños |
| **Recepcionista** | Turnos, creación de dueños y facturación completa |
| **Dueño** | Sus mascotas, historial (solo lectura), turnos y sus facturas (solo lectura) |

**Requisitos de seguridad:**
- Implementar `LoginRequiredMixin` y `PermissionRequiredMixin` en todas las vistas.
- Los dueños solo ven sus propios registros — filtrado obligatorio a nivel de QuerySet.
- El historial médico y las facturas son de solo lectura para dueños.
- No hay registro público — Admin, Veterinario y Recepcionista crean las cuentas de dueños.

---

## Módulos

### 1. Autenticación y Perfiles
- Login / Logout.
- Admin, Veterinario y Recepcionista pueden crear cuentas de dueños.
- Dashboard personalizado por rol:
  - **Admin:** estadísticas generales (mascotas, turnos pendientes, consultas del día).
  - **Veterinario:** lista de turnos del día y acceso rápido a historiales.
  - **Recepcionista:** bandeja de turnos pendientes y facturas pendientes de cobro.
  - **Dueño:** lista de sus mascotas, estado de sus turnos y sus facturas.

### 2. Gestión de Mascotas (CRUD)
- **Campos:** Nombre, especie, raza, fecha de nacimiento, foto, peso actual, dueño asignado.
- **Validación:** No permitir fechas de nacimiento futuras.
- **Interfaz:** Cards de Tailwind con indicador de estado visual (ej. "En clínica" / "En casa").
- Acceso: Admin y Veterinario pueden hacer CRUD completo. Dueño solo lectura de sus mascotas.

### 3. Historia Médica
- Registro de consultas vinculado a mascota y veterinario.
- **Campos:** Fecha, motivo, diagnóstico, tratamiento, observaciones.
- **Regla de integridad:** Las entradas son inmutables pasadas las 24 horas de su creación.
- Solo Veterinario y Admin pueden crear o editar (dentro de las 24 hs). Dueño y Recepcionista: solo lectura.

### 4. Módulo de Turnos
- El dueño solicita un turno eligiendo fecha, hora y motivo.
- Admin y Recepcionista aprueban o rechazan el turno.
- El Veterinario ve los turnos aprobados asignados a él.
- **Estados:** `Pendiente → Aprobado / Rechazado → Completado`.

### 5. Módulo de Facturación
- Vinculada a un turno completado y a un dueño.
- La Recepcionista carga manualmente los ítems (descripción, precio unitario, cantidad) al momento de facturar. El total se calcula automáticamente.
- **Estados de factura:** `Pendiente → Pagado → Anulado`.
- El dueño ve sus facturas desde su dashboard (solo lectura).
- El Admin tiene acceso completo (ver, editar estado, anular).

---

## Estructura de Proyecto

```
veterinaria/
├── manage.py
├── requirements.txt
├── .env.ejemplo
├── veterinaria/          # settings.py, urls.py, wsgi.py
├── apps/
│   ├── usuarios/         # Custom User Model (AbstractUser) + roles
│   ├── mascotas/         # CRUD y validaciones
│   ├── historial/        # Consultas médicas con regla de 24hs
│   ├── turnos/           # Solicitud y aprobación de turnos
│   └── facturacion/      # Ítems, totales y estados de pago
├── static/               # CSS/JS personalizados
└── templates/            # base.html con navegación dinámica por rol
```

---

## Configuración de Base de Datos (`settings.py`)

```python
import os
MODO_BD = os.getenv('MODO_BD', 'sqlite')

if MODO_BD == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NOMBRE'),
            'USER': os.getenv('DB_USUARIO'),
            'PASSWORD': os.getenv('DB_CONTRASENA'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PUERTO', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

---

## `requirements.txt`
```
django>=4.2
psycopg2-binary
python-dotenv
pillow
```

---

## Requisitos de UX y Calidad
1. **Responsive y mobile-first** usando utilidades de Tailwind CSS via CDN.
2. **Notificaciones flotantes** con `django.contrib.messages` para confirmar todas las acciones (crear, editar, aprobar turno, emitir factura, etc.).
3. **Formularios estilizados** con Tailwind: bordes redondeados, colores de foco, validación visual de errores.
4. **Navegación dinámica** en `base.html`: los ítems del menú se muestran u ocultan según el rol del usuario autenticado.

---

## Entregables esperados
1. Código fuente completo organizado en apps.
2. Migraciones iniciales listas para ejecutar.
3. `README.md` con instrucciones para:
   - Crear el entorno virtual e instalar dependencias.
   - Configurar el `.env` para cada modo de base de datos.
   - Ejecutar migraciones y crear el primer superusuario.
   - Levantar el servidor de desarrollo.

---

## Cambios respecto al prompt original
- ❌ Eliminado: módulo de tracking GPS, WebSockets, Django Channels, DRF, `mssql-django`.
- ✅ Agregado: rol Recepcionista con gestión de turnos, creación de dueños y facturación.
- ✅ Agregado: módulo de Facturación con ítems manuales y estados de pago.
- ✅ Corregido: base de datos dual SQLite/PostgreSQL (sin SQL Server).
- ✅ Clarificado: sin registro público — Admin, Veterinario y Recepcionista crean cuentas de dueños.
- ✅ Simplificado: sin envío de emails en ningún flujo.
