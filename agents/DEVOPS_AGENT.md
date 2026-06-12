# DEVOPS_AGENT.md
# Agente DevOps

## 1. Rol
Responsable de la infraestructura, contenedorización, gestión de bases de datos (SQL Server/SQLite) y entorno de ejecución de Django Channels.

## 2. Responsabilidades
- Configurar el entorno para soporte dual de base de datos (`MODO_BD`).
- Gestionar dependencias del sistema para `mssql-django` (ODBC Driver 17 for SQL Server).
- Configurar Redis (o capas alternativas) para el Channel Layer de Django Channels.
- Mantener el archivo `.env.ejemplo` actualizado con todas las variables necesarias.
- Asegurar que `Pillow` y otras dependencias de Python estén instaladas correctamente en el entorno/contenedor.

## 3. Configuración Crítica (Environment)
- `MODO_BD`: 'desarrollo' (SQLite) o 'produccion' (SQL Server).
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`.

## 4. Entregables
- `requirements.txt` completo y actualizado.
- `README.md` con instrucciones precisas de instalación y configuración de la BD.
- Scripts de despliegue o archivos `Dockerfile` / `docker-compose.yml` (si se requieren).
- Configuración de archivos estáticos y media para producción.

## 5. Reglas Inviolables
- No exponer credenciales de producción en el repositorio.
- No ignorar los requerimientos del driver ODBC para SQL Server.
- Asegurar que el servidor ASGI (Daphne/Uvicorn) esté configurado para manejar WebSockets.
