import os

from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios'
    verbose_name = 'Usuarios'

    def ready(self) -> None:
        # Solo en el proceso principal del servidor de desarrollo (no en el watcher del autoreloader)
        if os.environ.get('RUN_MAIN') == 'true':
            import warnings
            from django.core.management import call_command
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                call_command('flush', '--no-input', verbosity=0)
                call_command('cargar_datos_prueba', verbosity=0)
