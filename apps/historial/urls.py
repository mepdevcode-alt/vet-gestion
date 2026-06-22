from django.urls import path
from . import views

urlpatterns = [
    # Consulta Médica (existente)
    path('mascota/<int:mascota_pk>/',       views.HistorialMascota.as_view(), name='historial_mascota'),
    path('mascota/<int:mascota_pk>/nueva/', views.CrearConsulta.as_view(),    name='crear_consulta'),
    path('<int:pk>/editar/',                views.EditarConsulta.as_view(),   name='editar_consulta'),

    # Historia Clínica
    path('hc/',                              views.ListaHistoriasClinicas.as_view(),    name='hc_lista'),
    path('hc/nueva/',                        views.CrearHistoriaClinica.as_view(),      name='hc_crear'),
    path('hc/nueva/<int:mascota_pk>/',       views.CrearHistoriaClinica.as_view(),      name='hc_crear_mascota'),
    path('hc/<int:pk>/',                     views.DetalleHistoriaClinica.as_view(),    name='hc_detalle'),
    path('hc/<int:pk>/editar/',              views.EditarHistoriaClinica.as_view(),     name='hc_editar'),
    path('hc/<int:pk>/eliminar/',            views.EliminarHistoriaClinica.as_view(),   name='hc_eliminar'),
    path('hc/<int:pk>/pdf/',                 views.DescargarPDFHistoriaClinica.as_view(), name='hc_pdf'),
]
