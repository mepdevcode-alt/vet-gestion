import uuid
from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from apps.usuarios.models import Usuario


def validar_fecha_no_futura(valor: date) -> None:
    if valor > date.today():
        raise ValidationError('La fecha de nacimiento no puede ser una fecha futura.')


def ruta_foto_mascota(instancia: 'Mascota', nombre_archivo: str) -> str:
    return f'mascotas/{instancia.id}/{nombre_archivo}'


class Mascota(models.Model):
    ESPECIE_PERRO = 'perro'
    ESPECIE_GATO = 'gato'
    ESPECIE_AVE = 'ave'
    ESPECIE_OTRO = 'otro'

    ESPECIES = [
        (ESPECIE_PERRO, 'Perro'),
        (ESPECIE_GATO, 'Gato'),
        (ESPECIE_AVE, 'Ave'),
        (ESPECIE_OTRO, 'Otro'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    especie = models.CharField(max_length=20, choices=ESPECIES, verbose_name='Especie')
    raza = models.CharField(max_length=100, blank=True, verbose_name='Raza')
    fecha_nacimiento = models.DateField(
        validators=[validar_fecha_no_futura],
        verbose_name='Fecha de nacimiento',
    )
    foto = models.ImageField(
        upload_to=ruta_foto_mascota,
        blank=True,
        null=True,
        verbose_name='Foto',
    )
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Peso (kg)')
    dueno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='mascotas',
        limit_choices_to={'rol': Usuario.ROL_DUENO},
        verbose_name='Dueño',
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    token_collar = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name='Token collar QR')

    class Meta:
        verbose_name = 'mascota'
        verbose_name_plural = 'mascotas'
        ordering = ['nombre']

    def __str__(self) -> str:
        return f'{self.nombre} ({self.dueno.get_full_name() or self.dueno.username})'

    @property
    def edad(self) -> int:
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
