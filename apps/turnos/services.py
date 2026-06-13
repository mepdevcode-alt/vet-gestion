from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Turno, CambioEstadoTurno

LIMITE_TURNOS_PENDIENTES = 3


def _registrar_cambio(turno: Turno, estado_anterior: str, estado_nuevo: str,
                      usuario, motivo: str = '') -> None:
    CambioEstadoTurno.objects.create(
        turno=turno,
        estado_anterior=estado_anterior,
        estado_nuevo=estado_nuevo,
        realizado_por=usuario,
        motivo=motivo,
    )


def crear_turno(dueno, datos: dict) -> Turno:
    """Crea un turno nuevo para el dueño. Valida límite de pendientes y fecha futura."""
    pendientes = Turno.objects.filter(
        mascota__dueno=dueno,
        estado=Turno.ESTADO_PENDIENTE,
    ).count()
    if pendientes >= LIMITE_TURNOS_PENDIENTES:
        raise ValidationError(
            f'Ya tenés {pendientes} turnos pendientes. '
            f'El límite es {LIMITE_TURNOS_PENDIENTES}.'
        )

    tipo = datos.get('tipo_consulta', Turno.CONSULTA_GENERAL)
    duracion = Turno.DURACIONES_POR_TIPO.get(tipo, 30)

    turno = Turno(
        mascota=datos['mascota'],
        veterinario=datos.get('veterinario'),
        tipo_consulta=tipo,
        duracion_minutos=datos.get('duracion_minutos', duracion),
        fecha_hora=datos['fecha_hora'],
        motivo=datos.get('motivo', ''),
    )
    turno.full_clean()
    turno.save()

    _registrar_cambio(turno, '', Turno.ESTADO_PENDIENTE, dueno)
    return turno


def aprobar_turno(turno: Turno, usuario) -> Turno:
    """Aprueba un turno pendiente. Valida disponibilidad del veterinario."""
    if turno.estado != Turno.ESTADO_PENDIENTE:
        raise ValidationError('Solo se pueden aprobar turnos en estado Pendiente.')

    conflicto = _buscar_conflicto_horario(turno)
    if conflicto:
        raise ValidationError(
            f'El veterinario ya tiene un turno aprobado que se solapa: '
            f'{conflicto.mascota.nombre} a las '
            f'{conflicto.fecha_hora.strftime("%H:%M")} '
            f'({conflicto.get_tipo_consulta_display()}).'
        )

    estado_anterior = turno.estado
    turno.estado = Turno.ESTADO_APROBADO
    turno.save()
    _registrar_cambio(turno, estado_anterior, Turno.ESTADO_APROBADO, usuario)
    return turno


def rechazar_turno(turno: Turno, usuario, motivo: str) -> Turno:
    """Rechaza un turno pendiente con motivo obligatorio."""
    if turno.estado != Turno.ESTADO_PENDIENTE:
        raise ValidationError('Solo se pueden rechazar turnos en estado Pendiente.')
    if not motivo.strip():
        raise ValidationError('El motivo de rechazo es obligatorio.')

    estado_anterior = turno.estado
    turno.estado = Turno.ESTADO_RECHAZADO
    turno.motivo_rechazo = motivo.strip()
    turno.save()
    _registrar_cambio(turno, estado_anterior, Turno.ESTADO_RECHAZADO, usuario, motivo)
    return turno


def cancelar_turno(turno: Turno, usuario, motivo: str) -> Turno:
    """Cancela un turno pendiente o aprobado. Anula factura pendiente si existe."""
    if turno.estado not in (Turno.ESTADO_PENDIENTE, Turno.ESTADO_APROBADO):
        raise ValidationError('Solo se pueden cancelar turnos en estado Pendiente o Aprobado.')
    if not motivo.strip():
        raise ValidationError('El motivo de cancelación es obligatorio.')

    estado_anterior = turno.estado
    turno.estado = Turno.ESTADO_CANCELADO
    turno.motivo_cancelacion = motivo.strip()
    turno.save()
    _registrar_cambio(turno, estado_anterior, Turno.ESTADO_CANCELADO, usuario, motivo)

    # RN-010: anular factura pendiente si existe
    _anular_factura_si_pendiente(turno)
    return turno


def completar_turno(turno: Turno, usuario) -> Turno:
    """Marca un turno aprobado como completado."""
    if turno.estado != Turno.ESTADO_APROBADO:
        raise ValidationError('Solo se pueden completar turnos en estado Aprobado.')

    estado_anterior = turno.estado
    turno.estado = Turno.ESTADO_COMPLETADO
    turno.save()
    _registrar_cambio(turno, estado_anterior, Turno.ESTADO_COMPLETADO, usuario)
    return turno


def _buscar_conflicto_horario(turno: Turno):
    """Devuelve el primer turno aprobado del mismo veterinario que se solapa, o None."""
    if not turno.veterinario:
        return None

    nuevo_inicio = turno.fecha_hora
    nuevo_fin = turno.fecha_hora_fin

    candidatos = Turno.objects.filter(
        veterinario=turno.veterinario,
        estado=Turno.ESTADO_APROBADO,
    ).exclude(pk=turno.pk)

    for candidato in candidatos:
        if candidato.fecha_hora < nuevo_fin and candidato.fecha_hora_fin > nuevo_inicio:
            return candidato
    return None


def _anular_factura_si_pendiente(turno: Turno) -> None:
    """Si el turno tiene factura en estado Pendiente, la anula."""
    try:
        factura = turno.factura
        if factura.estado == 'pendiente':
            factura.estado = 'anulado'
            factura.save()
    except Exception:
        pass
