from django.contrib import admin
from .models import Factura, ItemFactura


class ItemFacturaInline(admin.TabularInline):
    model = ItemFactura
    extra = 1


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'dueno', 'turno', 'estado', 'fecha_emision', 'total']
    list_filter = ['estado', 'fecha_emision']
    search_fields = ['dueno__username', 'dueno__first_name', 'dueno__last_name']
    readonly_fields = ['fecha_emision']
    inlines = [ItemFacturaInline]
