# Módulo de Turnos — Definición de Requisitos

**Responsable:** Ariel  
**Fecha:** 2026-06-13  
**Estado:** Completado  

---

## Base de partida (Sprint 0)

El modelo `Turno` del Sprint 0 implementa:
- Campos: `mascota`, `veterinario`, `fecha_hora`, `motivo`, `estado`, `notas_recepcion`, `fecha_creacion`
- Estados: `Pendiente → Aprobado / Rechazado → Completado`

Gaps identificados en el Paso 1 (análisis funcional):
- Sin control de disponibilidad del veterinario
- Sin duración estimada por turno
- Sin estado "Cancelado"
- Sin motivo de rechazo explícito
- Sin tipo de consulta
- Sin auditoría de cambios de estado
- Sin vista de agenda
- Sin límite de turnos pendientes por dueño

---

## Requisitos Funcionales

### MUST HAVE

| ID | Requisito |
|---|---|
| REQ-F-001 | El Dueño puede solicitar un turno eligiendo mascota, veterinario, fecha/hora y tipo de consulta |
| REQ-F-002 | La Recepcionista y el Admin pueden aprobar o rechazar turnos pendientes |
| REQ-F-003 | Al rechazar un turno se debe registrar el motivo de rechazo (campo obligatorio) |
| REQ-F-004 | La Recepcionista y el Admin pueden marcar un turno como Completado |
| REQ-F-005 | El sistema debe permitir cancelar un turno (por el Dueño o la Recepcionista), con motivo obligatorio |
| REQ-F-006 | El sistema debe validar disponibilidad: no se puede aprobar un turno si el veterinario ya tiene uno aprobado en esa franja horaria |
| REQ-F-007 | Cada turno tiene una duración estimada (en minutos) según el tipo de consulta |
| REQ-F-008 | El sistema debe categorizar el turno por tipo de consulta (consulta general, vacunación, cirugía, urgencia, control) |

### SHOULD HAVE

| ID | Requisito |
|---|---|
| REQ-F-009 | La Recepcionista/Admin tienen una vista de agenda (lista del día o semana) con todos los turnos aprobados |
| REQ-F-010 | El sistema registra un historial de cambios de estado por turno (quién cambió, cuándo, de qué estado a cuál) |
| REQ-F-011 | Un Dueño no puede tener más de N turnos pendientes simultáneos (límite sugerido: 3) |
| REQ-F-012 | El Veterinario ve en su dashboard los turnos del día asignados a él |

### COULD HAVE

| ID | Requisito |
|---|---|
| REQ-F-013 | Notificación por email al Dueño cuando su turno es aprobado o rechazado |
| REQ-F-014 | Reprogramación de turno aprobado (cambio de fecha/hora sin cancelar y recrear) |

### WON'T HAVE (esta versión)

- Turnos recurrentes / periódicos
- Integración con Google Calendar
- Pagos online vinculados al turno

---

## Requisitos No Funcionales

| ID | Requisito |
|---|---|
| REQ-NF-001 | Todo el código (variables, clases, funciones, campos de BD) debe estar en español |
| REQ-NF-002 | La interfaz debe ser responsive usando Tailwind CSS vía CDN |
| REQ-NF-003 | Todas las vistas deben requerir autenticación (LoginRequiredMixin) |
| REQ-NF-004 | El acceso a turnos debe estar filtrado por rol — un Dueño solo ve sus propios turnos |
| REQ-NF-005 | La lógica compleja (validación de disponibilidad, cambios de estado) va en turnos/services.py |
| REQ-NF-006 | Se prefieren Class-Based Views (CBVs) sobre FBVs |
