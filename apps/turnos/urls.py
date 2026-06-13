from django.urls import path
from . import views

app_name = 'turnos'

urlpatterns = [
    path('',                    views.MisTurnosView.as_view(),      name='mis_turnos'),
    path('solicitar/',          views.SolicitarTurnoView.as_view(), name='solicitar'),
    path('gestion/',            views.GestionTurnosView.as_view(),  name='gestion'),
    path('agenda/',             views.AgendaView.as_view(),         name='agenda'),
    path('mis-turnos-hoy/',     views.TurnosHoyVetView.as_view(),   name='turnos_hoy_vet'),
    path('<int:pk>/',           views.DetalleTurnoView.as_view(),   name='detalle'),
    path('<int:pk>/aprobar/',   views.AprobarTurnoView.as_view(),   name='aprobar'),
    path('<int:pk>/rechazar/',  views.RechazarTurnoView.as_view(),  name='rechazar'),
    path('<int:pk>/cancelar/',  views.CancelarTurnoView.as_view(),  name='cancelar'),
    path('<int:pk>/completar/', views.CompletarTurnoView.as_view(), name='completar'),
]
