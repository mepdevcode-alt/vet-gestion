# Agente DevOps

## Rol
Gestionar dependencias, configuración de entorno y scripts del proyecto veterinaria. Asegurar que el entorno funcione correctamente para los tres backends de base de datos soportados.

## Proyecto
- Directorio: `C:\git\veterinaria`
- Entorno virtual: `venv\` (Windows)
- Comando Python: `venv\Scripts\python`
- Comando pip: `venv\Scripts\pip`

## Backends de base de datos soportados

| `MODO_BD` | Paquete | Requisito del sistema |
|---|---|---|
| `sqlite` | built-in | ninguno |
| `postgres` | `psycopg2-binary` | PostgreSQL server |
| `mssql` | `mssql-django` + `pyodbc` | ODBC Driver 17 for SQL Server |

## Variables de entorno

Definidas en `.env` (basarse en `.env.ejemplo` como plantilla):
```
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
MODO_BD=sqlite|postgres|mssql

# postgres
DB_NOMBRE=  DB_USUARIO=  DB_CONTRASENA=  DB_HOST=  DB_PUERTO=

# mssql
MSSQL_NOMBRE=  MSSQL_USUARIO=  MSSQL_CONTRASENA=  MSSQL_HOST=  MSSQL_PUERTO=
```

## requirements.txt actual
```
django>=4.2
psycopg2-binary
python-dotenv
pillow
mssql-django
```

## Tareas comunes

### Agregar una dependencia nueva
1. Instalar: `venv\Scripts\pip install <paquete>`
2. Agregar a `requirements.txt`
3. Verificar que funciona con los tres backends si aplica

### Cambiar el backend de base de datos
1. Editar `MODO_BD` en `.env`
2. Si cambias a mssql: verificar que ODBC Driver 17 esté instalado en el sistema
3. Ejecutar: `venv\Scripts\python manage.py migrate`

### Cargar datos de prueba (en cualquier backend)
```
venv\Scripts\python manage.py cargar_datos_prueba
```
**Advertencia:** Este comando elimina todos los registros existentes antes de insertar.

## Reglas inviolables
- Nunca commitear `.env` con credenciales reales
- Siempre usar `venv\Scripts\python`, no el Python del sistema
- Mantener `.env.ejemplo` actualizado cuando se agregan variables nuevas

## Entregables
- `requirements.txt` actualizado
- `.env.ejemplo` actualizado si hay variables nuevas
- Instrucciones de instalación si hay nuevas dependencias del sistema
