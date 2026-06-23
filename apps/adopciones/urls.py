from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaAdopciones.as_view(), name='lista_adopciones'),
    path('favoritos/', views.MisFavoritos.as_view(), name='mis_favoritos'),
    path('<slug:slug>/', views.DetalleAdopcion.as_view(), name='detalle_adopcion'),
]
