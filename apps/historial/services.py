from datetime import timedelta
from django.utils import timezone
from .models import ConsultaMedica

LIMITE_EDICION_HORAS = 24


def puede_editar_consulta(consulta: ConsultaMedica) -> bool:
    """Una consulta solo es editable dentro de las 24 horas posteriores a su creación."""
    limite = consulta.fecha + timedelta(hours=LIMITE_EDICION_HORAS)
    return timezone.now() < limite
