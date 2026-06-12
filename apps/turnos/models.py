from django.db import models
from apps.mascotas.models import Mascota
from apps.usuarios.models import Usuario


class Turno(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_APROBADO = 'aprobado'
    ESTADO_RECHAZADO = 'rechazado'
    ESTADO_COMPLETADO = 'completado'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_APROBADO, 'Aprobado'),
        (ESTADO_RECHAZADO, 'Rechazado'),
        (ESTADO_COMPLETADO, 'Completado'),
    ]

    COLORES_ESTADO = {
        ESTADO_PENDIENTE: 'bg-yellow-100 text-yellow-800',
        ESTADO_APROBADO: 'bg-green-100 text-green-800',
        ESTADO_RECHAZADO: 'bg-red-100 text-red-800',
        ESTADO_COMPLETADO: 'bg-blue-100 text-blue-800',
    }

    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='turnos',
        verbose_name='Mascota',
    )
    veterinario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='turnos_asignados',
        limit_choices_to={'rol': Usuario.ROL_VETERINARIO},
        verbose_name='Veterinario',
    )
    fecha_hora = models.DateTimeField(verbose_name='Fecha y hora')
    motivo = models.CharField(max_length=255, verbose_name='Motivo')
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ESTADO_PENDIENTE,
        verbose_name='Estado',
    )
    notas_recepcion = models.TextField(blank=True, verbose_name='Notas de recepción')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'turno'
        verbose_name_plural = 'turnos'
        ordering = ['fecha_hora']

    def __str__(self) -> str:
        return f'Turno {self.mascota.nombre} - {self.fecha_hora.strftime("%d/%m/%Y %H:%M")}'

    def get_color_estado(self) -> str:
        return self.COLORES_ESTADO.get(self.estado, 'bg-gray-100 text-gray-800')

    def tiene_factura(self) -> bool:
        try:
            return bool(self.factura)
        except Exception:
            return False
