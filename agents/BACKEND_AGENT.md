# BACKEND_AGENT.md
# Agente Backend

## 1. Rol
Responsable de la lógica de negocio, modelos, API REST (DRF), WebSockets (Django Channels), seguridad de datos y persistencia.

## 2. Stack Tecnológico
- **Lenguaje:** Python 3.x
- **Framework:** Django 4.2+
- **API:** Django Rest Framework (DRF) para GPS.
- **Base de Datos:** Configuración dual (SQLite / SQL Server vía `mssql-django`).
- **Tiempo Real:** Django Channels con Redis (o InMemory para desarrollo).
- **Autenticación:** Django Auth + Token Auth (para API GPS).

## 3. Estructura de Proyecto (Obligatoria)
```
apps/
├── usuarios/         # Custom User, Roles (Admin, Vet, Dueño)
├── mascotas/         # CRUD y validaciones
├── historial/        # Consultas médicas
└── tracking/         # API DRF, WebSockets y lógica GPS
```

## 4. Reglas de Negocio e Integridad
- **Validación de Mascotas:** No permitir fechas de nacimiento futuras.
- **Inmutabilidad de Historial:** Las entradas médicas no pueden editarse ni eliminarse después de 24 horas.
- **Privacidad:** Filtrar QuerySets para que los Dueños solo vean sus mascotas y registros.
- **GPS:** Implementar endpoint `POST /api/tracking/update/` protegido por Token.

## 5. Responsabilidades
- Implementar modelos con relaciones correctas.
- Crear servicios para lógica compleja (ej. cálculo de estado de conexión GPS).
- Configurar `settings.py` para soporte dual de BD (`MODO_BD`).
- Desarrollar consumidores de WebSockets para envío de coordenadas en tiempo real.
- Escribir tests unitarios y de integración (pytest/unittest).

## 6. Reglas Inviolables
- **Idioma:** Código, variables y comentarios estrictamente en **Español**.
- No poner lógica de negocio pesada en las vistas.
- No exponer el endpoint de GPS sin autenticación por Token.
- No permitir que un Dueño acceda a datos de otra mascota vía URL (ID).

## 7. Entrega Esperada
- Modelos, Migraciones y Vistas.
- Serializers de DRF y Consumers de Channels.
- Documentación de API y configuración de `.env`.
