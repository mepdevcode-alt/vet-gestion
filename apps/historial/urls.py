from django.urls import path
from . import views

urlpatterns = [
    path('mascota/<int:mascota_pk>/', views.HistorialMascota.as_view(), name='historial_mascota'),
    path('mascota/<int:mascota_pk>/nueva/', views.CrearConsulta.as_view(), name='crear_consulta'),
    path('<int:pk>/editar/', views.EditarConsulta.as_view(), name='editar_consulta'),
]
