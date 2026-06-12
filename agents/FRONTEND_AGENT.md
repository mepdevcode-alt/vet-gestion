# Agente Frontend

## Rol
Crear y modificar templates Django, estilos con Tailwind CSS y JavaScript vanilla para el proyecto veterinaria.

## Stack obligatorio
- **Templates:** Django Templates — extender siempre `base.html`
- **Estilos:** Tailwind CSS vía CDN (ya incluido en `base.html`)
- **JavaScript:** Vanilla JS únicamente — sin React, Vue, Angular
- **Sin compilación:** No agregar pasos de build al proyecto

## Estructura de archivos
```
templates/
├── base.html              ← layout maestro, NO modificar sin causa mayor
├── includes/navbar.html   ← navegación por rol, modificar si hay nuevas secciones
├── usuarios/              ← login, dashboards por rol
├── mascotas/              ← lista, detalle, crear, editar
├── historial/             ← historial por mascota, crear/editar consulta
├── turnos/                ← lista, detalle, solicitar, gestionar
└── facturacion/           ← lista, detalle, crear factura
```

## Reglas de templates

### Siempre extender base.html
```html
{% extends 'base.html' %}
{% block content %}
  {# contenido aquí #}
{% endblock %}
```

### Navegación por rol
Los ítems de `navbar.html` se muestran/ocultan con:
```html
{% if request.user.es_admin %}...{% endif %}
{% if request.user.es_veterinario %}...{% endif %}
```

### Ocultar acciones sin permiso
No mostrar botones de editar/eliminar si el usuario no tiene el rol requerido. Ejemplo:
```html
{% if request.user.es_admin or request.user.es_veterinario %}
  <a href="{% url 'mascotas:editar' mascota.pk %}">Editar</a>
{% endif %}
```

### Formularios
Usar clases Tailwind para inputs:
```html
<input class="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500">
```

### Mensajes Django
`base.html` ya maneja los mensajes flash de Django. No duplicar la lógica.

## Interfaz en español
Todos los textos, etiquetas, títulos y mensajes en español.

## Entregables por tarea
- Archivos de template creados o modificados
- Sin cambios en Python (ese es trabajo del agente backend)
