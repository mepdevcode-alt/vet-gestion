# Módulo de Turnos — Reglas de Negocio

**Responsable:** Ariel  
**Fecha:** 2026-06-13  
**Estado:** Completado  

---

## RN-001 — Transiciones de estado válidas

Solo estas transiciones están permitidas. Cualquier otra debe ser bloqueada por el sistema.

| Desde | Hacia | Quién puede hacerlo |
|---|---|---|
| Pendiente | Aprobado | Recepcionista / Admin |
| Pendiente | Rechazado | Recepcionista / Admin |
| Pendiente | Cancelado | Dueño / Recepcionista / Admin |
| Aprobado | Completado | Recepcionista / Admin |
| Aprobado | Cancelado | Dueño / Recepcionista / Admin |
| Rechazado | — | Estado terminal, sin salida |
| Cancelado | — | Estado terminal, sin salida |
| Completado | — | Estado terminal, sin salida |

**Dónde se aplica:** `turnos/services.py`

---

## RN-002 — Motivo obligatorio en ciertos cambios

- Al rechazar un turno: motivo obligatorio (campo `motivo_rechazo`)
- Al cancelar un turno: motivo obligatorio (campo `motivo_cancelacion`)
- Al aprobar o completar: no se requiere motivo

**Dónde se aplica:** formulario + `turnos/services.py`

---

## RN-003 — Control de disponibilidad del veterinario

Al intentar aprobar un turno, el sistema verifica:

> ¿Existe algún turno del mismo veterinario en estado Aprobado cuya franja horaria se solape con la del turno a aprobar?

La franja se calcula como: `fecha_hora` hasta `fecha_hora + duración_minutos`.

Hay solapamiento si: `turno_existente.inicio < turno_nuevo.fin` Y `turno_existente.fin > turno_nuevo.inicio`

Si hay conflicto, la aprobación es bloqueada y se informa qué turno colisiona.

**Dónde se aplica:** `turnos/services.py` → `validar_disponibilidad()`

---

## RN-004 — Duración estimada por tipo de consulta

| Tipo de consulta | Duración (minutos) |
|---|---|
| Consulta general | 30 |
| Vacunación | 15 |
| Control | 20 |
| Urgencia | 45 |
| Cirugía | 90 |

La duración se establece automáticamente al crear el turno según el tipo seleccionado. Puede ajustarse manualmente si es necesario.

**Dónde se aplica:** model `choices` + `turnos/services.py` al crear el turno

---

## RN-005 — Límite de turnos pendientes por dueño

Un Dueño no puede solicitar un nuevo turno si ya tiene 3 o más turnos en estado Pendiente.

**Dónde se aplica:** `turnos/services.py` → `validar_limite_pendientes(dueno)`

---

## RN-006 — Los turnos solo pueden solicitarse en el futuro

La `fecha_hora` del turno debe ser posterior al momento actual al momento de la solicitud. No se permite agendar en el pasado.

**Dónde se aplica:** `clean()` del modelo + validación en el formulario

---

## RN-007 — Aislamiento estricto por rol Dueño

Todo queryset accesible por el rol Dueño debe filtrar por las mascotas que le pertenecen:

```python
Turno.objects.filter(mascota__dueno=request.user)
```

Nunca confiar en parámetros de URL para identificar al dueño.

**Dónde se aplica:** todas las vistas accesibles por Dueño

---

## RN-008 — Auditoría de cambios de estado

Cada cambio de estado genera un registro de auditoría con:
- Estado anterior
- Estado nuevo
- Usuario que realizó el cambio
- Fecha y hora del cambio
- Motivo (cuando aplica)

Requiere modelo adicional `CambioEstadoTurno` con FK a `Turno`.

**Dónde se aplica:** `turnos/services.py` → cada función de cambio de estado llama al registro de auditoría

---

## RN-009 — El Veterinario es solo lectura

El Veterinario puede ver sus turnos del día pero no puede aprobar, rechazar, cancelar ni completar turnos. Esas acciones son exclusivas de Recepcionista y Admin.

**Dónde se aplica:** `UserPassesTestMixin` en las vistas de gestión

---

## RN-010 — Vinculación con facturación

- Una factura solo puede crearse para un turno en estado Completado
- Si un turno con factura en estado Pendiente es cancelado, la factura debe cambiar automáticamente a Anulado

**Dónde se aplica:** `turnos/services.py` → `completar_turno()` habilita la factura; `cancelar_turno()` verifica y anula factura pendiente
