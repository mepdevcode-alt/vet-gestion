# STACK.md - Stack Tecnológico Refinado

## Backend
- **Framework:** Django 4.2+ (LTS).
- **API:** Django REST Framework (DRF) para telemetría GPS.
- **Base de Datos:**
  - Desarrollo: SQLite 3.
  - Producción: Microsoft SQL Server (vía `mssql-django`).
- **Tiempo Real:** Django Channels + Redis (Channel Layer).
- **Tareas Async:** Celery + Redis (opcional para reportes pesados).

## Frontend (Server-Side Rendering)
- **Motor:** Django Templates.
- **Estilos:** Tailwind CSS (via CDN para prototipado rápido).
- **Mapas:** Leaflet.js + Cartografía de **OpenStreetMap (OSM)**.
- **Interactividad:** JavaScript Vanilla / Alpine.js.

## Integraciones y Seguridad
- **GPS:** Endpoint protegido por Token Auth.
- **Autenticación:** Django Auth System (Session + Token).
- **Media:** Pillow para procesamiento de imágenes (fotos de mascotas).

## Variables de Entorno (.env)
- `MODO_BD`: 'desarrollo' | 'produccion'.
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
- `REDIS_URL` para WebSockets.
