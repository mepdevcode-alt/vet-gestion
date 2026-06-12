from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaFacturas.as_view(), name='lista_facturas'),
    path('<int:pk>/', views.DetalleFactura.as_view(), name='detalle_factura'),
    path('nueva/<int:turno_pk>/', views.CrearFactura.as_view(), name='crear_factura'),
    path('<int:pk>/cambiar-estado/', views.CambiarEstadoFactura.as_view(), name='cambiar_estado_factura'),
]
