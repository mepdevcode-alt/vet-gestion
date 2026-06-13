import uuid
from django.db import migrations, models


def asignar_tokens(apps, schema_editor):
    Mascota = apps.get_model('mascotas', 'Mascota')
    for mascota in Mascota.objects.all():
        mascota.token_collar = uuid.uuid4()
        mascota.save(update_fields=['token_collar'])


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas', '0002_initial'),
    ]

    operations = [
        # Paso 1: agregar columna nullable sin restricción unique
        migrations.AddField(
            model_name='mascota',
            name='token_collar',
            field=models.UUIDField(null=True, editable=False, verbose_name='Token collar QR'),
        ),
        # Paso 2: poblar UUIDs únicos en filas existentes
        migrations.RunPython(asignar_tokens, migrations.RunPython.noop),
        # Paso 3: hacer la columna NOT NULL y unique
        migrations.AlterField(
            model_name='mascota',
            name='token_collar',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name='Token collar QR'),
        ),
    ]
