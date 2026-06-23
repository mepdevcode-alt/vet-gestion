from django.contrib import admin
from .models import MascotaAdopcion, FotoAdicional


class FotoAdicionalInline(admin.TabularInline):
    model = FotoAdicional
    extra = 3
    fields = ['foto', 'orden']


@admin.register(MascotaAdopcion)
class MascotaAdopcionAdmin(admin.ModelAdmin):
    inlines = [FotoAdicionalInline]
    list_display = [
        'nombre', 'especie', 'raza', 'edad', 'sexo',
        'tamanio', 'vacunado', 'castrado', 'disponible', 'destacado', 'fecha_ingreso',
    ]
    list_filter = ['especie', 'sexo', 'tamanio', 'disponible', 'destacado', 'vacunado', 'castrado']
    search_fields = ['nombre', 'raza', 'descripcion', 'ubicacion', 'refugio']
    list_editable = ['disponible', 'destacado']
    prepopulated_fields = {'slug': ('nombre',)}
    date_hierarchy = 'fecha_ingreso'
    readonly_fields = ['fecha_publicacion']

    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'slug', 'especie', 'raza', 'edad', 'sexo', 'tamanio'),
        }),
        ('Descripción', {
            'fields': ('descripcion', 'foto_principal'),
        }),
        ('Estado sanitario', {
            'fields': ('vacunado', 'castrado'),
        }),
        ('Ubicación', {
            'fields': ('ubicacion', 'refugio'),
        }),
        ('Publicación', {
            'fields': ('disponible', 'destacado', 'fecha_ingreso', 'fecha_publicacion'),
        }),
    )
