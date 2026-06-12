from django.contrib import admin
from .models import Mascota


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'especie', 'raza', 'dueno', 'peso', 'fecha_nacimiento']
    list_filter = ['especie']
    search_fields = ['nombre', 'raza', 'dueno__username', 'dueno__first_name', 'dueno__last_name']
    autocomplete_fields = ['dueno']
