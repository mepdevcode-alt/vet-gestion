from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaFacturas.as_view(), name='lista_facturas'),
    path('<int:pk>/', views.DetalleFactura.as_view(), name='detalle_factura'),
    path('nueva/<int:turno_pk>/', views.CrearFactura.as_view(), name='crear_factura'),
    path('<int:pk>/cambiar-estado/', views.CambiarEstadoFactura.as_view(), name='cambiar_estado_factura'),
    # Mercado Pago
    path('<int:pk>/pagar/', views.IniciarPagoMP.as_view(), name='iniciar_pago_mp'),
    path('webhook/mp/', views.WebhookMP.as_view(), name='webhook_mp'),
    path('<int:pk>/pago-exitoso/', views.PagoExitosoMP.as_view(), name='pago_exitoso_mp'),
    path('<int:pk>/pago-pendiente/', views.PagoPendienteMP.as_view(), name='pago_pendiente_mp'),
    path('<int:pk>/pago-fallido/', views.PagoFallidoMP.as_view(), name='pago_fallido_mp'),
]
