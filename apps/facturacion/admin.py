from django.contrib import admin
from .models import Factura, ItemFactura, PagoMercadoPago


class ItemFacturaInline(admin.TabularInline):
    model = ItemFactura
    extra = 1


class PagoMPInline(admin.TabularInline):
    model = PagoMercadoPago
    extra = 0
    readonly_fields = ['preference_id', 'payment_id', 'estado_mp', 'fecha_creacion', 'fecha_actualizacion']
    can_delete = False


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'dueno', 'turno', 'estado', 'fecha_emision', 'total']
    list_filter = ['estado', 'fecha_emision']
    search_fields = ['dueno__username', 'dueno__first_name', 'dueno__last_name']
    readonly_fields = ['fecha_emision']
    inlines = [ItemFacturaInline, PagoMPInline]


@admin.register(PagoMercadoPago)
class PagoMercadoPagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'factura', 'estado_mp', 'payment_id', 'fecha_creacion']
    list_filter = ['estado_mp']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
