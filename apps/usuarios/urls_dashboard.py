from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('admin/', views.DashboardAdmin.as_view(), name='dashboard_admin'),
    path('veterinario/', views.DashboardVeterinario.as_view(), name='dashboard_veterinario'),
    path('recepcionista/', views.DashboardRecepcionista.as_view(), name='dashboard_recepcionista'),
    path('dueno/', views.DashboardDueno.as_view(), name='dashboard_dueno'),
]
