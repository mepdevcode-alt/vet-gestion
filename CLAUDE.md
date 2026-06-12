# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Descripción del Proyecto

Sistema de gestión para clínica veterinaria construido con Django. El proyecto está actualmente en Sprint 0 (fase de especificación): existen documentación y plantillas HTML, pero el código de la aplicación Django aún no ha sido implementado.

## Comandos de Configuración

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.ejemplo .env           # luego configurar .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Stack Tecnológico

- **Backend:** Python 3.x + Django 4.2+ (sin DRF, sin Django Channels)
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción) — controlado por variable de entorno `MODO_BD`
- **Frontend:** Django Templates + Tailwind CSS (CDN) + Vanilla JS únicamente (sin React/Vue)
- **Estilo de código:** PEP 8, type hints obligatorios, Class-Based Views (CBVs) preferidas sobre FBVs

## Configuración de Base de Datos

Controlada por `MODO_BD` en `.env` (`sqlite` o `postgres`):

```python
MODO_BD = os.getenv('MODO_BD', 'sqlite')
if MODO_BD == 'postgres':
    # usa DB_NOMBRE, DB_USUARIO, DB_CONTRASENA, DB_HOST, DB_PUERTO
```

## Arquitectura

Patrón MVT con una capa de servicios (`services.py` por app) para la lógica de negocio compleja.

### Apps (`apps/`)

| App | Responsabilidad |
|---|---|
| `usuarios/` | `AbstractUser` personalizado con campo `rol`; login/logout; dashboards por rol |
| `mascotas/` | CRUD de mascotas (Admin y Vet únicamente); carga de fotos con Pillow |
| `historial/` | Registros médicos; inmutabilidad de 24 horas aplicada en la capa de servicios |
| `turnos/` | Ciclo de vida de turnos: `Pendiente → Aprobado/Rechazado → Completado` |
| `facturacion/` | Ítems de factura manuales; ciclo de facturas: `Pendiente → Pagado → Anulado` |

### Matriz de Roles

| Acción | Admin | Veterinario | Recepcionista | Dueño |
|---|:---:|:---:|:---:|:---:|
| Crear usuarios (Vet/Admin/Recep) | ✅ | ❌ | ❌ | ❌ |
| Crear cuentas de Dueño | ✅ | ✅ | ✅ | ❌ |
| CRUD Mascotas | ✅ | ✅ | ❌ | Ver propias |
| Crear/editar Historia Médica | ✅ | ✅ (<24h) | ❌ | ❌ |
| Ver Historia Médica | ✅ | ✅ | ❌ | Solo propias |
| Gestionar Turnos (aprobar/rechazar) | ✅ | ❌ | ✅ | Solo solicitar |
| Facturación | ✅ | ❌ | ✅ | Ver propias |

## Reglas de Negocio Críticas

- **Idioma:** Todo el código (variables, clases, funciones), nombres de campos en BD, comentarios e interfaz de usuario **deben estar en español**.
- **Mascotas:** La `fecha_nacimiento` no puede ser futura — validar en el método `clean()` del modelo.
- **Historial médico:** Los registros solo son editables/eliminables dentro de las 24 horas posteriores a su creación. Aplicar en `historial/services.py`, no solo en la vista.
- **Filtro de propiedad:** Todo queryset en vistas accesibles por el rol `Dueño` **debe** filtrar por `dueño=request.user`. Nunca confiar únicamente en parámetros de URL.
- **Sin registro público:** Las cuentas son creadas únicamente por Admin, Veterinario o Recepcionista.

## Patrones de Seguridad

```python
# Todas las vistas requieren login
class MiVista(LoginRequiredMixin, UserPassesTestMixin, View): ...

# Aislamiento por dueño — obligatorio en cualquier queryset accesible por Dueño
Mascota.objects.filter(dueño=request.user)
```

Usar `LoginRequiredMixin` + `UserPassesTestMixin` (o `PermissionRequiredMixin`) en todas las vistas.

## Plantillas

`templates/base.html` es el layout maestro. Los ítems de navegación en `templates/includes/navbar.html` se muestran u ocultan según `request.user.rol`. Todas las plantillas nuevas deben extender `base.html`.
