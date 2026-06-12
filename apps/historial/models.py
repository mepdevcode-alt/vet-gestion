from django.db import models
from apps.mascotas.models import Mascota
from apps.usuarios.models import Usuario


class ConsultaMedica(models.Model):
    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='consultas',
        verbose_name='Mascota',
    )
    veterinario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='consultas_realizadas',
        limit_choices_to={'rol': Usuario.ROL_VETERINARIO},
        verbose_name='Veterinario',
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    motivo = models.CharField(max_length=255, verbose_name='Motivo de consulta')
    diagnostico = models.TextField(verbose_name='Diagnóstico')
    tratamiento = models.TextField(verbose_name='Tratamiento')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = 'consulta médica'
        verbose_name_plural = 'consultas médicas'
        ordering = ['-fecha']

    def __str__(self) -> str:
        return f'Consulta {self.mascota.nombre} - {self.fecha.strftime("%d/%m/%Y")}'
