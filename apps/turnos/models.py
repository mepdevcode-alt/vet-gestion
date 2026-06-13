from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.mascotas.models import Mascota
from apps.usuarios.models import Usuario


class Turno(models.Model):
    ESTADO_PENDIENTE  = 'pendiente'
    ESTADO_APROBADO   = 'aprobado'
    ESTADO_RECHAZADO  = 'rechazado'
    ESTADO_COMPLETADO = 'completado'
    ESTADO_CANCELADO  = 'cancelado'

    ESTADOS = [
        (ESTADO_PENDIENTE,  'Pendiente'),
        (ESTADO_APROBADO,   'Aprobado'),
        (ESTADO_RECHAZADO,  'Rechazado'),
        (ESTADO_COMPLETADO, 'Completado'),
        (ESTADO_CANCELADO,  'Cancelado'),
    ]

    CONSULTA_GENERAL    = 'consulta_general'
    CONSULTA_VACUNACION = 'vacunacion'
    CONSULTA_CONTROL    = 'control'
    CONSULTA_URGENCIA   = 'urgencia'
    CONSULTA_CIRUGIA    = 'cirugia'

    TIPOS_CONSULTA = [
        (CONSULTA_GENERAL,    'Consulta general'),
        (CONSULTA_VACUNACION, 'Vacunación'),
        (CONSULTA_CONTROL,    'Control'),
        (CONSULTA_URGENCIA,   'Urgencia'),
        (CONSULTA_CIRUGIA,    'Cirugía'),
    ]

    DURACIONES_POR_TIPO = {
        CONSULTA_GENERAL:    30,
        CONSULTA_VACUNACION: 15,
        CONSULTA_CONTROL:    20,
        CONSULTA_URGENCIA:   45,
        CONSULTA_CIRUGIA:    90,
    }

    COLORES_ESTADO = {
        ESTADO_PENDIENTE:  'bg-yellow-100 text-yellow-800',
        ESTADO_APROBADO:   'bg-green-100 text-green-800',
        ESTADO_RECHAZADO:  'bg-red-100 text-red-800',
        ESTADO_COMPLETADO: 'bg-blue-100 text-blue-800',
        ESTADO_CANCELADO:  'bg-gray-100 text-gray-800',
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
    tipo_consulta = models.CharField(
        max_length=20,
        choices=TIPOS_CONSULTA,
        default=CONSULTA_GENERAL,
        verbose_name='Tipo de consulta',
    )
    duracion_minutos = models.PositiveIntegerField(
        default=30,
        verbose_name='Duración (minutos)',
    )
    fecha_hora = models.DateTimeField(verbose_name='Fecha y hora')
    motivo = models.CharField(max_length=255, verbose_name='Motivo')
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ESTADO_PENDIENTE,
        verbose_name='Estado',
    )
    notas_recepcion    = models.TextField(blank=True, verbose_name='Notas de recepción')
    motivo_rechazo     = models.TextField(blank=True, verbose_name='Motivo de rechazo')
    motivo_cancelacion = models.TextField(blank=True, verbose_name='Motivo de cancelación')
    fecha_creacion     = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'turno'
        verbose_name_plural = 'turnos'
        ordering = ['fecha_hora']

    def __str__(self) -> str:
        return f'Turno {self.mascota.nombre} - {self.fecha_hora.strftime("%d/%m/%Y %H:%M")}'

    def clean(self) -> None:
        if self.fecha_hora and self.fecha_hora <= timezone.now():
            raise ValidationError({'fecha_hora': 'La fecha y hora del turno debe ser futura.'})

    @property
    def fecha_hora_fin(self):
        return self.fecha_hora + timedelta(minutes=self.duracion_minutos)

    def get_color_estado(self) -> str:
        return self.COLORES_ESTADO.get(self.estado, 'bg-gray-100 text-gray-800')

    def tiene_factura(self) -> bool:
        try:
            return bool(self.factura)
        except Exception:
            return False


class CambioEstadoTurno(models.Model):
    turno = models.ForeignKey(
        Turno,
        on_delete=models.CASCADE,
        related_name='historial_estados',
        verbose_name='Turno',
    )
    estado_anterior = models.CharField(
        max_length=20,
        choices=Turno.ESTADOS,
        verbose_name='Estado anterior',
    )
    estado_nuevo = models.CharField(
        max_length=20,
        choices=Turno.ESTADOS,
        verbose_name='Estado nuevo',
    )
    realizado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cambios_estado_turno',
        verbose_name='Realizado por',
    )
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
    motivo     = models.TextField(blank=True, verbose_name='Motivo')

    class Meta:
        verbose_name = 'cambio de estado de turno'
        verbose_name_plural = 'cambios de estado de turnos'
        ordering = ['fecha_hora']

    def __str__(self) -> str:
        return f'{self.turno} | {self.estado_anterior} → {self.estado_nuevo}'
