# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sistema de Agentes

El proyecto usa un sistema multi-agente activado mediante comandos de barra. Cada agente tiene su definición en `agents/`.

### Comandos disponibles

| Comando | Descripción |
|---|---|
| `/tarea <descripción>` | **Orquestador principal** — analiza la tarea, activa los agentes necesarios en orden, integra resultados |
| `/backend <tarea>` | Agente backend directo (modelos, vistas, servicios) |
| `/frontend <tarea>` | Agente frontend directo (templates, CSS, JS) |
| `/qa <tarea>` | Agente QA directo (tests y validaciones) |
| `/seguridad <tarea>` | Agente de seguridad directo (auditoría de permisos y IDOR) |

### Flujo del orquestador (`/tarea`)

```
/tarea <descripción>
         │
         ▼
   Orquestador lee CLAUDE.md
   y clasifica la tarea
         │
    ┌────┴────┐
    │         │
 DevOps   Backend     ← en paralelo si no hay dependencias
(si hace falta)  │
                 ▼
             Frontend  ← después del backend (necesita sus URLs y campos)
                 │
         ┌───────┘
         ▼       ▼
        QA   Seguridad  ← en paralelo al final
         │       │
         └───┬───┘
             ▼
       Informe consolidado
```

Para tareas simples que solo tocan un área, usar el comando directo (`/backend`, `/frontend`, etc.) en lugar del orquestador.

---

## Descripción del Proyecto

Sistema de gestión para clínica veterinaria construido con Django. Implementación completa con 5 apps (`usuarios`, `mascotas`, `historial`, `turnos`, `facturacion`), autenticación basada en roles y soporte multi-base de datos.

## Comandos de Desarrollo

**Siempre usar el intérprete del venv, no el Python del sistema:**

```bash
# Activar entorno (Windows)
venv\Scripts\activate

# Dependencias
pip install -r requirements.txt

# Base de datos
venv\Scripts\python manage.py migrate
venv\Scripts\python manage.py createsuperuser

# Servidor de desarrollo
venv\Scripts\python manage.py runserver

# Cargar datos de prueba (borra y recrea todos los registros)
venv\Scripts\python manage.py cargar_datos_prueba

# Shell interactivo
venv\Scripts\python manage.py shell
```

No hay suite de tests implementada aún. Para correr tests cuando se agreguen:
```bash
venv\Scripts\python manage.py test apps.<nombre_app>
```

## Configuración de Base de Datos

Controlada por `MODO_BD` en `.env`. Soporta tres backends:

| `MODO_BD` | Backend | Variables requeridas |
|---|---|---|
| `sqlite` (default) | SQLite local | — |
| `postgres` | PostgreSQL | `DB_NOMBRE`, `DB_USUARIO`, `DB_CONTRASENA`, `DB_HOST`, `DB_PUERTO` |
| `mssql` | SQL Server (paquete `mssql-django`) | `MSSQL_NOMBRE`, `MSSQL_USUARIO`, `MSSQL_CONTRASENA`, `MSSQL_HOST`, `MSSQL_PUERTO` |

Al usar `mssql`, el driver ODBC 17 for SQL Server debe estar instalado en el sistema y `mssql-django` en el venv.

## Stack Tecnológico

- **Backend:** Python 3.x + Django 4.2+
- **Base de datos:** SQLite / PostgreSQL / SQL Server según `MODO_BD`
- **Frontend:** Django Templates + Tailwind CSS (CDN) + Vanilla JS
- **Estilo de código:** PEP 8, type hints obligatorios, CBVs preferidas sobre FBVs

## Arquitectura

### Estructura de URLs

```
/                       → redirect a /dashboard/
/usuarios/              → login, logout, crear dueño, lista usuarios
/dashboard/             → dispatcher por rol → /dashboard/admin|veterinario|recepcionista|dueno/
/mascotas/              → CRUD de mascotas
/historial/             → historial médico por mascota
/turnos/                → ciclo de vida de turnos
/facturacion/           → facturas e ítems
```

El dashboard usa un archivo de URLs separado: `apps/usuarios/urls_dashboard.py`. La vista `Dashboard` redirige según `request.user.rol` sin renderizar nada propio.

### Patrón de Servicios

Solo `historial` tiene capa de servicios (`apps/historial/services.py`). La función clave es:

```python
puede_editar_consulta(consulta: ConsultaMedica) -> bool
# Retorna False si han pasado más de LIMITE_EDICION_HORAS = 24 horas desde la creación
```

Esta validación **debe aplicarse en la vista** (`EditarConsulta`) además del servicio. No depender de que el template oculte el botón de edición.

### Apps (`apps/`)

| App | Responsabilidad | Archivos clave |
|---|---|---|
| `usuarios/` | AbstractUser con campo `rol`; login/logout; dashboards por rol | `models.py`, `views.py`, `urls_dashboard.py` |
| `mascotas/` | CRUD de mascotas; carga de fotos con Pillow | `models.py`, `forms.py` |
| `historial/` | Registros médicos; inmutabilidad de 24 h | `services.py`, `views.py` |
| `turnos/` | Ciclo `Pendiente → Aprobado/Rechazado → Completado` | `views.py`, `forms.py` |
| `facturacion/` | Facturas con ítems mediante inlineformset | `forms.py` (ItemFormSet) |

### Formsets en Facturación

`CrearFactura` usa `ItemFormSet = inlineformset_factory(Factura, ItemFactura, extra=1, min_num=1)`. El template debe manejar el management form del formset. Al agregar ítems dinámicamente desde JS, actualizar `TOTAL_FORMS`.

### Matriz de Roles

| Acción | Admin | Veterinario | Recepcionista | Dueño |
|---|:---:|:---:|:---:|:---:|
| Crear usuarios (Vet/Admin/Recep) | ✅ | ❌ | ❌ | ❌ |
| Crear cuentas de Dueño | ✅ | ✅ | ✅ | ❌ |
| CRUD Mascotas | ✅ | ✅ | ❌ | Ver propias |
| Crear/editar Historia Médica | ✅ | ✅ (<24 h) | ❌ | ❌ |
| Ver Historia Médica | ✅ | ✅ | ❌ | Solo propias |
| Gestionar Turnos (aprobar/rechazar) | ✅ | ❌ | ✅ | Solo solicitar |
| Facturación | ✅ | ❌ | ✅ | Ver propias |

## Reglas de Negocio Críticas

- **Idioma:** Todo el código (variables, clases, funciones), campos en BD, comentarios e interfaz **en español**.
- **Mascotas:** `fecha_nacimiento` no puede ser futura — validar en `clean()` del modelo.
- **Filtro de propiedad:** Todo queryset en vistas accesibles por el rol `Dueño` **debe** filtrar por `dueño=request.user`. Nunca confiar en parámetros de URL.
- **Sin registro público:** Las cuentas las crea únicamente Admin, Veterinario o Recepcionista.

## Patrones de Seguridad

```python
# Todas las vistas requieren login + test de rol
class MiVista(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.es_admin()

# Aislamiento por dueño — obligatorio en cualquier queryset accesible por Dueño
Mascota.objects.filter(dueño=request.user)
```

Los métodos de rol en `Usuario`: `es_admin()`, `es_veterinario()`, `es_recepcionista()`, `es_dueno()`, `es_staff_clinica()`.

## Plantillas

`templates/base.html` es el layout maestro. Los ítems de navegación están en `templates/includes/navbar.html` y se muestran/ocultan según `request.user.rol`. Todas las plantillas nuevas deben extender `base.html`.

## Datos de Prueba

El comando `cargar_datos_prueba` **elimina todos los registros existentes** antes de insertar. Credenciales generadas (contraseña `Test1234!`):

```
admin_clinica / dra_sofia / dr_carlos / recep_lucia
juan_perez / maria_lopez / andres_garcia
```
