from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', lambda request: redirect('home'), name='inicio'),
    path('usuarios/', include('apps.usuarios.urls')),
    path('dashboard/', include('apps.usuarios.urls_dashboard')),
    path('mascotas/', include('apps.mascotas.urls')),
    path('historial/', include('apps.historial.urls')),
    path('turnos/', include('apps.turnos.urls')),
    path('facturacion/', include('apps.facturacion.urls')),
    path('adopciones/', include('apps.adopciones.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
