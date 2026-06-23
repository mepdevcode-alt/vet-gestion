import apps.adopciones.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MascotaAdopcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('especie', models.CharField(
                    choices=[
                        ('perro', 'Perro'),
                        ('gato', 'Gato'),
                        ('ave', 'Ave'),
                        ('roedor', 'Roedor'),
                        ('conejo', 'Conejo'),
                        ('otro', 'Otro'),
                    ],
                    max_length=20,
                    verbose_name='Especie',
                )),
                ('raza', models.CharField(blank=True, max_length=100, verbose_name='Raza')),
                ('edad', models.CharField(max_length=50, verbose_name='Edad', help_text='Ej: "Cachorro", "1 año", "3 años"')),
                ('sexo', models.CharField(
                    choices=[
                        ('macho', 'Macho'),
                        ('hembra', 'Hembra'),
                        ('desconocido', 'Desconocido'),
                    ],
                    max_length=15,
                    verbose_name='Sexo',
                )),
                ('tamanio', models.CharField(
                    choices=[
                        ('pequeño', 'Pequeño'),
                        ('mediano', 'Mediano'),
                        ('grande', 'Grande'),
                    ],
                    max_length=20,
                    verbose_name='Tamaño',
                )),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('foto_principal', models.ImageField(
                    blank=True,
                    null=True,
                    upload_to=apps.adopciones.models.ruta_foto_adopcion,
                    verbose_name='Foto principal',
                )),
                ('vacunado', models.BooleanField(default=False, verbose_name='Vacunado')),
                ('castrado', models.BooleanField(default=False, verbose_name='Castrado/Esterilizado')),
                ('disponible', models.BooleanField(default=True, verbose_name='Disponible para adopción')),
                ('destacado', models.BooleanField(default=False, verbose_name='Destacado')),
                ('fecha_ingreso', models.DateField(verbose_name='Fecha de ingreso')),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de publicación')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'mascota en adopción',
                'verbose_name_plural': 'mascotas en adopción',
                'ordering': ['-destacado', '-fecha_publicacion'],
            },
        ),
    ]
