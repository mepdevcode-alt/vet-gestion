from django.contrib import admin
from .models import Turno


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ['mascota', 'veterinario', 'fecha_hora', 'motivo', 'estado']
    list_filter = ['estado', 'fecha_hora']
    search_fields = ['mascota__nombre', 'motivo']
    readonly_fields = ['fecha_creacion']
