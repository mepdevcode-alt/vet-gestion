from decimal import Decimal
from django.db import models
from apps.turnos.models import Turno
from apps.usuarios.models import Usuario


class Factura(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_PAGADO = 'pagado'
    ESTADO_ANULADO = 'anulado'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_ANULADO, 'Anulado'),
    ]

    COLORES_ESTADO = {
        ESTADO_PENDIENTE: 'bg-yellow-100 text-yellow-800',
        ESTADO_PAGADO: 'bg-green-100 text-green-800',
        ESTADO_ANULADO: 'bg-red-100 text-red-800',
    }

    turno = models.OneToOneField(
        Turno,
        on_delete=models.CASCADE,
        related_name='factura',
        verbose_name='Turno',
    )
    dueno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='facturas',
        verbose_name='Dueño',
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ESTADO_PENDIENTE,
        verbose_name='Estado',
    )
    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de emisión')
    notas = models.TextField(blank=True, verbose_name='Notas')

    class Meta:
        verbose_name = 'factura'
        verbose_name_plural = 'facturas'
        ordering = ['-fecha_emision']

    def __str__(self) -> str:
        return f'Factura #{self.id} - {self.dueno.get_full_name() or self.dueno.username}'

    @property
    def total(self) -> Decimal:
        return sum(item.subtotal for item in self.items.all()) or Decimal('0.00')

    def get_color_estado(self) -> str:
        return self.COLORES_ESTADO.get(self.estado, 'bg-gray-100 text-gray-800')


class ItemFactura(models.Model):
    factura = models.ForeignKey(
        Factura,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Factura',
    )
    descripcion = models.CharField(max_length=255, verbose_name='Descripción')
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio unitario',
    )
    cantidad = models.PositiveIntegerField(default=1, verbose_name='Cantidad')

    class Meta:
        verbose_name = 'ítem de factura'
        verbose_name_plural = 'ítems de factura'

    def __str__(self) -> str:
        return f'{self.descripcion} x{self.cantidad}'

    @property
    def subtotal(self) -> Decimal:
        return self.precio_unitario * self.cantidad
