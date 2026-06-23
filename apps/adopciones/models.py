from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def ruta_foto_adopcion(instancia: 'MascotaAdopcion', nombre_archivo: str) -> str:
    return f'adopciones/{instancia.slug or "tmp"}/{nombre_archivo}'


def ruta_foto_galeria(instancia: 'FotoAdicional', nombre_archivo: str) -> str:
    return f'adopciones/{instancia.mascota.slug or "tmp"}/galeria/{nombre_archivo}'


class MascotaAdopcion(models.Model):
    ESPECIE_PERRO = 'perro'
    ESPECIE_GATO = 'gato'
    ESPECIE_AVE = 'ave'
    ESPECIE_ROEDOR = 'roedor'
    ESPECIE_CONEJO = 'conejo'
    ESPECIE_OTRO = 'otro'

    ESPECIES = [
        (ESPECIE_PERRO, 'Perro'),
        (ESPECIE_GATO, 'Gato'),
        (ESPECIE_AVE, 'Ave'),
        (ESPECIE_ROEDOR, 'Roedor'),
        (ESPECIE_CONEJO, 'Conejo'),
        (ESPECIE_OTRO, 'Otro'),
    ]

    SEXO_MACHO = 'macho'
    SEXO_HEMBRA = 'hembra'
    SEXO_DESCONOCIDO = 'desconocido'

    SEXOS = [
        (SEXO_MACHO, 'Macho'),
        (SEXO_HEMBRA, 'Hembra'),
        (SEXO_DESCONOCIDO, 'Desconocido'),
    ]

    TAMANIO_PEQUEÑO = 'pequeño'
    TAMANIO_MEDIANO = 'mediano'
    TAMANIO_GRANDE = 'grande'

    TAMANIOS = [
        (TAMANIO_PEQUEÑO, 'Pequeño'),
        (TAMANIO_MEDIANO, 'Mediano'),
        (TAMANIO_GRANDE, 'Grande'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    especie = models.CharField(max_length=20, choices=ESPECIES, verbose_name='Especie')
    raza = models.CharField(max_length=100, blank=True, verbose_name='Raza')
    edad = models.CharField(max_length=50, verbose_name='Edad', help_text='Ej: "Cachorro", "1 año", "3 años"')
    sexo = models.CharField(max_length=15, choices=SEXOS, verbose_name='Sexo')
    tamanio = models.CharField(max_length=20, choices=TAMANIOS, verbose_name='Tamaño')
    descripcion = models.TextField(verbose_name='Descripción')
    foto_principal = models.ImageField(
        upload_to=ruta_foto_adopcion,
        blank=True,
        null=True,
        verbose_name='Foto principal',
    )
    vacunado = models.BooleanField(default=False, verbose_name='Vacunado')
    castrado = models.BooleanField(default=False, verbose_name='Castrado/Esterilizado')
    disponible = models.BooleanField(default=True, verbose_name='Disponible para adopción')
    destacado = models.BooleanField(default=False, verbose_name='Destacado')
    fecha_ingreso = models.DateField(verbose_name='Fecha de ingreso')
    fecha_publicacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de publicación')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug', blank=True)
    ubicacion = models.CharField(max_length=150, blank=True, verbose_name='Ubicación')
    refugio = models.CharField(max_length=150, blank=True, verbose_name='Refugio/Organización')

    class Meta:
        verbose_name = 'mascota en adopción'
        verbose_name_plural = 'mascotas en adopción'
        ordering = ['-destacado', '-fecha_publicacion']

    def __str__(self) -> str:
        return f'{self.nombre} ({self.get_especie_display()})'

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            contador = 1
            while MascotaAdopcion.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{contador}'
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('detalle_adopcion', kwargs={'slug': self.slug})

    @property
    def icono_especie(self) -> str:
        iconos = {
            self.ESPECIE_PERRO: '🐶',
            self.ESPECIE_GATO: '🐱',
            self.ESPECIE_AVE: '🦜',
            self.ESPECIE_ROEDOR: '🐭',
            self.ESPECIE_CONEJO: '🐰',
            self.ESPECIE_OTRO: '🐾',
        }
        return iconos.get(self.especie, '🐾')


class FotoAdicional(models.Model):
    mascota = models.ForeignKey(
        MascotaAdopcion,
        on_delete=models.CASCADE,
        related_name='fotos_adicionales',
        verbose_name='Mascota',
    )
    foto = models.ImageField(upload_to=ruta_foto_galeria, verbose_name='Foto')
    orden = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')

    class Meta:
        verbose_name = 'foto adicional'
        verbose_name_plural = 'fotos adicionales'
        ordering = ['orden']

    def __str__(self) -> str:
        return f'Foto de {self.mascota.nombre} (orden {self.orden})'
