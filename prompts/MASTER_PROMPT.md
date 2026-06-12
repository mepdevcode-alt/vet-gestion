  # Prompt Inicial – Sistema de Gestión Veterinaria (Versión Refinada)

## Instrucción principal
Eres un desarrollador Fullstack Senior con experiencia en Python y Django. Tu tarea es generar una aplicación web completa para una clínica veterinaria. El sistema debe ser robusto, seguro y con una interfaz moderna y profesional.

---

## Stack tecnológico
- **Backend:** Python 3.x con Django 4.2+
- **API:** Django Rest Framework (DRF) para el ingreso de datos GPS.
- **Base de datos:** Configuración dual (SQLite para desarrollo / PostgreSQL para producción con `mssql-django`).
- **Frontend:** Django Templates + Tailwind CSS (via CDN para simplicidad).
- **Idioma:** Código, variables, comentarios e interfaz totalmente en **Español**.

---

## Roles y Seguridad (Crítico)
1. **Administrador:** Control total del sistema y gestión de personal.
2. **Veterinario:** Gestión de mascotas e historias médicas.
3. **Dueño:** Registro propio, gestión de sus mascotas y visualización de ubicación en tiempo real.

**Requisito de Seguridad:** 
- Implementar `LoginRequiredMixin` y controles de permisos estrictos. 
- Los dueños **solo** pueden ver los registros que les pertenecen (filtrado a nivel de QuerySet).
- El historial médico es de solo lectura para los dueños.

---

## Módulos Detallados

### 1. Autenticación y Perfiles
- Registro público para dueños.
- Login/Logout.
- Dashboard personalizado según el rol (Estadísticas para admin, citas para veterinarios, lista de mascotas para dueños).

### 2. Gestión de Mascotas (CRUD)
- Campos: Nombre, especie, raza, fecha de nacimiento, foto, peso actual y dueño.
- **Validación:** No permitir fechas de nacimiento futuras.
- Interfaz: Uso de Cards de Tailwind con estados visuales (ej. indicador de "En clínica" o "En casa").

### 3. Historia Médica Profesional
- Registro de consultas vinculado a mascota y veterinario.
- Campos: Motivo, Diagnóstico, Tratamiento, Observaciones y Fecha.
- **Regla de integridad:** Las entradas de historial son inmutables después de 24 horas de su creación.

## Configuración Técnica Obligatoria

### Estructura de Proyecto
```
veterinaria/
├── manage.py
├── requirements.txt
├── .env.ejemplo
├── veterinaria/          # Settings, URLs, ASGI
├── apps/
│   ├── usuarios/         # Custom User Model (AbstractUser)
│   ├── mascotas/         # CRUD y Validaciones
│   ├── historial/        # Consultas médicas
│   └── tracking/         # API DRF, WebSockets y OSM
├── static/               # JS para Leaflet y Websockets
└── templates/            # Base.html con Tailwind y Navigation
```

### Configuración de Base de Datos (en `settings.py`)
Controlar mediante `MODO_BD` en el `.env`. Usar `mssql-django` para SQL Server con el driver "ODBC Driver PostgreSql".

---

## Requisitos de Calidad y UX
1. **Interfaz:** Diseño limpio, responsive y "mobile-first".
2. **Feedback:** Uso de `django.contrib.messages` (notificaciones flotantes) para confirmar acciones.
3. **Formularios:** Estilizar formularios con clases de Tailwind (bordes redondeados, focus de color).
4. **Documentación:** Generar un `README.md` con los pasos para:
   - Crear el entorno virtual.
   - Migrar la base de datos.
   - Crear el primer superusuario.
   - Ejecutar el servidor de desarrollo y el worker de Channels.

---

## Entregables
- Código fuente completo organizado en apps.
- `requirements.txt` con: `django`, `mssql-django`, `channels`, `djangorestframework`, `python-dotenv`, `pillow`.
- Scripts de migración iniciales.
- Template base con navegación dinámica por roles.
