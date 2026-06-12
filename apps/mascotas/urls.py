from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaMascotas.as_view(), name='lista_mascotas'),
    path('nueva/', views.CrearMascota.as_view(), name='crear_mascota'),
    path('<int:pk>/', views.DetalleMascota.as_view(), name='detalle_mascota'),
    path('<int:pk>/editar/', views.EditarMascota.as_view(), name='editar_mascota'),
    path('<int:pk>/eliminar/', views.EliminarMascota.as_view(), name='eliminar_mascota'),
]
