# ARCHITECTURE.md - Arquitectura del Sistema

## 1. Patrón Arquitectónico
El sistema sigue el patrón **MVT (Model-View-Template)** nativo de Django, extendido con una **Service Layer** para la lógica de negocio compleja.

## 2. Componentes Principales

### A. Capa de Datos (Modelos)
- Uso de `AbstractUser` para el modelo de `Usuario` (Roles: Admin, Vet, Dueño).
- Modelos con validaciones personalizadas (ej. fechas de mascotas).
- Soporte dual de Base de Datos controlado por variables de entorno.

### B. Capa de Servicios (Services.py)
- Encapsula la lógica que no pertenece estrictamente a los modelos o vistas.
- Ejemplo: Lógica para calcular si un collar GPS está "Desconectado" o validar la inmutabilidad de una historia médica (24h).

### C. Capa de Comunicación (WebSockets)
- **Django Channels:** Maneja conexiones bidireccionales para el tracking GPS.
- **Consumers:** Procesan el envío de coordenadas desde el dispositivo (API) hacia el cliente web del dueño.

### D. Capa de Presentación (Frontend)
- Renderizado en servidor (SSR) para velocidad y SEO interno.
- Integración de Mapas de OpenStreetMap mediante Leaflet.js en el cliente.

## 3. Flujo de Datos GPS
1. El Collar GPS envía un `POST` con Token al endpoint de DRF.
2. La vista de DRF valida el token y guarda la posición.
3. Se dispara un mensaje al `Channel Group` de la mascota.
4. El WebSocket del cliente (Dueño) recibe la coordenada y actualiza el marcador en el mapa de OSM.
