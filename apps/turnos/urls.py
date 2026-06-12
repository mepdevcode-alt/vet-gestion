from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaTurnos.as_view(), name='lista_turnos'),
    path('solicitar/', views.SolicitarTurno.as_view(), name='solicitar_turno'),
    path('<int:pk>/', views.DetalleTurno.as_view(), name='detalle_turno'),
    path('<int:pk>/aprobar/', views.AprobarTurno.as_view(), name='aprobar_turno'),
    path('<int:pk>/rechazar/', views.RechazarTurno.as_view(), name='rechazar_turno'),
    path('<int:pk>/completar/', views.CompletarTurno.as_view(), name='completar_turno'),
]
