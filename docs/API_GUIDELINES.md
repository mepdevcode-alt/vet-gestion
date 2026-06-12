# API_GUIDELINES.md - Guía de la API (DRF)

## 1. Autenticación
Todos los endpoints de la API (especialmente el de GPS) deben usar:
- `AuthenticationClasses`: `TokenAuthentication`.
- El token debe enviarse en el header: `Authorization: Token <tu_token>`.

## 2. Endpoint de Telemetría GPS
- **URL:** `/api/tracking/actualizar/`
- **Método:** `POST`
- **Payload:**
```json
{
    "id_collar": "ABC-123",
    "latitud": -34.6037,
    "longitud": -58.3816
}
```

## 3. Formato de Respuesta
Todas las respuestas deben ser en JSON:
- **Éxito:** `200 OK` o `201 Created`.
- **Error:** `400 Bad Request`, `401 Unauthorized` o `403 Forbidden` con detalle del error.

## 4. Throttling
Limitar el reporte de posición GPS a un máximo de **1 petición cada 10 segundos** por collar para evitar sobrecarga.
