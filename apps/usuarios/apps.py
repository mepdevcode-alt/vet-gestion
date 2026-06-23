import os

from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios'
    verbose_name = 'Usuarios'

    def ready(self) -> None:
        import sys
        # Solo cuando se levanta el servidor de desarrollo (no en otros comandos de manage.py)
        es_runserver = len(sys.argv) > 1 and sys.argv[1] == 'runserver'
        if es_runserver and os.environ.get('RUN_MAIN') == 'true':
            import warnings
            from django.core.management import call_command
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                call_command('flush', '--no-input', verbosity=0)
                call_command('cargar_datos_prueba', verbosity=0)
