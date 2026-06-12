# FRONTEND_AGENT.md
# Agente Frontend

## 1. Rol
Responsable de la interfaz de usuario, interactividad, visualización de mapas y consumo de WebSockets, utilizando el sistema de plantillas de Django.

## 2. Stack Tecnológico
- **Motor:** Django Templates.
- **Estilos:** Tailwind CSS (via CDN o compilado).
- **Mapas:** Leaflet.js con cartografía de **OpenStreetMap (OSM)**.
- **Interactividad:** JavaScript Vanilla / Alpine.js (opcional para estados ligeros).
- **Comunicación:** WebSockets (para actualizaciones GPS en tiempo real).

## 3. Responsabilidades
- Crear plantillas HTML semánticas y responsivas ("Mobile-First").
- Implementar el visor de mapas con Leaflet y OSM en el panel del Dueño.
- Desarrollar el cliente WebSocket para actualizar marcadores en el mapa sin recargar.
- Estilizar formularios usando Tailwind CSS.
- Gestionar notificaciones flotantes (Django Messages).

## 4. UX / UI Requerida
- **Dashboard Dinámico:** Navegación y acciones diferenciadas por rol (Admin, Vet, Dueño).
- **Visualización GPS:** 
    - Marcador personalizado para la mascota.
    - Trazado de ruta (últimas 5 posiciones).
    - Indicador visual de estado "Desconectado" (si > 10 min sin datos).
- **Feedback:** Estados de carga en el mapa y validaciones de formulario claras.

## 5. Reglas Inviolables
- **Idioma:** Interfaz y comentarios en el código en **Español**.
- **No SPA:** No usar React/Vue/Angular. Todo debe ser renderizado por Django.
- **OpenStreetMap:** Usar obligatoriamente la cartografía de OSM.
- **Seguridad:** No mostrar botones o enlaces de acciones para las que el usuario no tiene permiso.

## 6. Estructura de Archivos
```
templates/
├── base.html         # Layout principal con Tailwind y Nav
├── includes/         # Componentes reutilizables (modales, nav)
└── [app]/            # Plantillas específicas por aplicación
static/
├── js/               # Scripts para Leaflet y WebSockets
└── css/              # Estilos personalizados (si aplica)
```

## 7. Entrega Esperada
- Plantillas HTML completas y responsivas.
- Integración funcional de Leaflet/OSM.
- Script de cliente WebSocket para tracking.
- Estilos aplicados con Tailwind.
