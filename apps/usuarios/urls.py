from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.IniciarSesion.as_view(), name='login'),
    path('logout/', views.CerrarSesion.as_view(), name='logout'),
    path('crear-dueno/', views.CrearDueno.as_view(), name='crear_dueno'),
    path('lista/', views.ListaUsuarios.as_view(), name='lista_usuarios'),
]
