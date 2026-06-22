from django.db import models
from apps.mascotas.models import Mascota
from apps.usuarios.models import Usuario


class HistoriaClinica(models.Model):
    SEXO_MACHO   = 'M'
    SEXO_HEMBRA  = 'H'
    SEXO_NO_ESP  = 'N'
    SEXO_CHOICES = [
        (SEXO_MACHO,  'Macho'),
        (SEXO_HEMBRA, 'Hembra'),
        (SEXO_NO_ESP, 'No especificado'),
    ]

    ESTADO_ACTIVA  = 'activa'
    ESTADO_CERRADA = 'cerrada'
    ESTADO_CHOICES = [
        (ESTADO_ACTIVA,  'Activa'),
        (ESTADO_CERRADA, 'Cerrada'),
    ]

    # Metadatos
    numero_hc           = models.CharField(max_length=20, unique=True, editable=False, verbose_name='N° HC')
    mascota             = models.ForeignKey(Mascota, on_delete=models.PROTECT, related_name='historias_clinicas', verbose_name='Mascota')
    creado_por          = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='historias_creadas', verbose_name='Creado por')
    fecha_creacion      = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    estado              = models.CharField(max_length=10, choices=ESTADO_CHOICES, default=ESTADO_ACTIVA, verbose_name='Estado')

    # Sección 1 — Datos del Propietario
    propietario_nombre    = models.CharField(max_length=200, verbose_name='Nombre')
    propietario_documento = models.CharField(max_length=20, blank=True, verbose_name='Documento')
    propietario_direccion = models.CharField(max_length=300, blank=True, verbose_name='Dirección')
    propietario_telefono  = models.CharField(max_length=50, blank=True, verbose_name='Teléfono')
    propietario_email     = models.EmailField(blank=True, verbose_name='Email')

    # Sección 2 — Datos del Paciente
    paciente_sexo               = models.CharField(max_length=1, choices=SEXO_CHOICES, default=SEXO_NO_ESP, verbose_name='Sexo')
    paciente_color_pelaje       = models.CharField(max_length=100, blank=True, verbose_name='Color / Pelaje')
    paciente_microchip          = models.CharField(max_length=50, blank=True, verbose_name='N° Microchip')
    paciente_procedencia        = models.CharField(max_length=200, blank=True, verbose_name='Procedencia')
    paciente_fin_zootecnico     = models.CharField(max_length=100, blank=True, verbose_name='Fin zootécnico')
    paciente_senas_particulares = models.TextField(blank=True, verbose_name='Señas particulares')

    # Sección 3 — Anamnesis
    motivo_consulta         = models.TextField(verbose_name='Motivo de consulta')
    dieta                   = models.CharField(max_length=300, blank=True, verbose_name='Dieta')
    enfermedades_previas    = models.TextField(blank=True, verbose_name='Enfermedades previas')
    medicacion_actual       = models.TextField(blank=True, verbose_name='Medicación actual')
    cirugias_previas        = models.TextField(blank=True, verbose_name='Cirugías previas')
    vacunacion              = models.TextField(blank=True, verbose_name='Vacunación')
    desparasitacion         = models.TextField(blank=True, verbose_name='Desparasitación')
    esterilizado            = models.BooleanField(default=False, verbose_name='Esterilizado/a')
    partos                  = models.TextField(blank=True, verbose_name='Partos')
    observaciones_anamnesis = models.TextField(blank=True, verbose_name='Observaciones')

    # Sección 4 — Examen Clínico
    temperatura             = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='Temperatura (°C)')
    frecuencia_cardiaca     = models.PositiveIntegerField(null=True, blank=True, verbose_name='FC (lpm)')
    frecuencia_respiratoria = models.PositiveIntegerField(null=True, blank=True, verbose_name='FR (rpm)')
    peso_actual             = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Peso actual (kg)')
    diagnostico_presuntivo  = models.TextField(blank=True, verbose_name='Diagnóstico presuntivo')
    diagnostico_definitivo  = models.TextField(verbose_name='Diagnóstico definitivo')
    tratamiento             = models.TextField(verbose_name='Tratamiento')
    medicacion_prescrita    = models.TextField(blank=True, verbose_name='Medicación prescrita')
    observaciones_clinicas  = models.TextField(blank=True, verbose_name='Observaciones clínicas')

    # Sección 5 — Seguimiento
    proxima_visita          = models.DateField(null=True, blank=True, verbose_name='Próxima visita')
    evolucion               = models.TextField(blank=True, verbose_name='Evolución')
    veterinario_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='historias_responsable',
        null=True, blank=True,
        limit_choices_to={'rol': Usuario.ROL_VETERINARIO},
        verbose_name='Veterinario responsable',
    )

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Historia Clínica'
        verbose_name_plural = 'Historias Clínicas'

    def __str__(self) -> str:
        return f'HC {self.numero_hc} — {self.mascota.nombre}'

    def save(self, *args, **kwargs) -> None:
        if not self.numero_hc:
            from django.utils import timezone
            year = timezone.now().year
            count = HistoriaClinica.objects.filter(fecha_creacion__year=year).count() + 1
            self.numero_hc = f'HC-{year}-{count:04d}'
        super().save(*args, **kwargs)


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
