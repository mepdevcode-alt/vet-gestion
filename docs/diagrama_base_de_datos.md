# Diagrama de Base de Datos

```mermaid
erDiagram

    USUARIO {
        int id PK
        varchar username
        varchar password
        varchar first_name
        varchar last_name
        varchar email
        varchar rol
        varchar telefono
    }

    MASCOTA {
        int id PK
        varchar nombre
        varchar especie
        varchar raza
        date fecha_nacimiento
        varchar foto
        decimal peso
        int dueno_id FK
        datetime fecha_registro
    }

    CONSULTA_MEDICA {
        int id PK
        int mascota_id FK
        int veterinario_id FK
        datetime fecha
        varchar motivo
        text diagnostico
        text tratamiento
        text observaciones
    }

    TURNO {
        int id PK
        int mascota_id FK
        int veterinario_id FK
        datetime fecha_hora
        varchar motivo
        varchar estado
        text notas_recepcion
        datetime fecha_creacion
    }

    FACTURA {
        int id PK
        int turno_id FK
        int dueno_id FK
        varchar estado
        datetime fecha_emision
        text notas
    }

    ITEM_FACTURA {
        int id PK
        int factura_id FK
        varchar descripcion
        decimal precio_unitario
        int cantidad
    }

    USUARIO ||--o{ MASCOTA : "es dueño de"
    USUARIO ||--o{ TURNO : "atiende como veterinario"
    USUARIO ||--o{ CONSULTA_MEDICA : "realiza como veterinario"
    USUARIO ||--o{ FACTURA : "es facturado como dueño"

    MASCOTA ||--o{ TURNO : "tiene"
    MASCOTA ||--o{ CONSULTA_MEDICA : "tiene historial"

    TURNO ||--o| FACTURA : "genera"

    FACTURA ||--o{ ITEM_FACTURA : "contiene"
```
