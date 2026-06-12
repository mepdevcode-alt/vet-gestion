from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard'), name='inicio'),
    path('usuarios/', include('apps.usuarios.urls')),
    path('dashboard/', include('apps.usuarios.urls_dashboard')),
    path('mascotas/', include('apps.mascotas.urls')),
    path('historial/', include('apps.historial.urls')),
    path('turnos/', include('apps.turnos.urls')),
    path('facturacion/', include('apps.facturacion.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
