from django.contrib import admin
from .models import ConsultaMedica


@admin.register(ConsultaMedica)
class ConsultaMedicaAdmin(admin.ModelAdmin):
    list_display = ['mascota', 'veterinario', 'fecha', 'motivo']
    list_filter = ['fecha', 'veterinario']
    search_fields = ['mascota__nombre', 'motivo', 'diagnostico']
    readonly_fields = ['fecha']
