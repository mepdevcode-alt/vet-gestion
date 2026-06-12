# FOLDER_STRUCTURE.md - Estructura de Carpetas

```text
veterinaria/
├── manage.py
├── requirements.txt
├── .env.ejemplo
├── README.md
├── veterinaria/          # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py           # Configuración para WebSockets
│   └── ws_urls.py        # Rutas de WebSockets
├── apps/                 # Directorio de aplicaciones
│   ├── usuarios/         # App: Auth y Roles
│   │   ├── models.py     # CustomUser(AbstractUser)
│   │   ├── views.py
│   │   └── urls.py
│   ├── mascotas/         # App: Gestión de Mascotas
│   │   ├── models.py     # Mascota
│   │   ├── services.py   # Lógica de validación
│   │   └── urls.py
│   ├── historial/        # App: Historias Médicas
│   │   ├── models.py     # ConsultaMedica
│   │   └── urls.py
│   └── tracking/         # App: GPS y WebSockets
│       ├── api_views.py  # Endpoints DRF
│       ├── consumers.py  # Lógica de Channels
│       └── models.py     # PosicionGPS
├── templates/            # Django Templates
│   ├── base.html
│   ├── includes/         # Navbar, footers, etc.
│   └── [app_name]/       # Templates por app
└── static/               # CSS, JS, Imágenes
    ├── js/               # Leaflet + WS logic
    └── css/              # Tailwind custom (opcional)
```
