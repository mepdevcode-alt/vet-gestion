from django.contrib import admin
from .models import ConsultaMedica, HistoriaClinica


@admin.register(ConsultaMedica)
class ConsultaMedicaAdmin(admin.ModelAdmin):
    list_display = ['mascota', 'veterinario', 'fecha', 'motivo']
    list_filter = ['fecha', 'veterinario']
    search_fields = ['mascota__nombre', 'motivo', 'diagnostico']
    readonly_fields = ['fecha']


@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ['numero_hc', 'mascota', 'propietario_nombre', 'diagnostico_definitivo', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion', 'veterinario_responsable']
    search_fields = ['numero_hc', 'mascota__nombre', 'propietario_nombre', 'diagnostico_definitivo']
    readonly_fields = ['numero_hc', 'fecha_creacion', 'fecha_actualizacion']
