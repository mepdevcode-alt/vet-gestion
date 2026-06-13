# Módulo de Turnos — Diseño de Entidades y Base de Datos

**Responsable:** Ariel  
**Fecha:** 2026-06-13  
**Estado:** Completado  

---

## Entidades

### Turno (actualizado)

Extiende el modelo del Sprint 0. Campos nuevos: `tipo_consulta`, `duracion_minutos`, `motivo_rechazo`, `motivo_cancelacion`. Estado `cancelado` agregado.

| Campo | Tipo | Descripción |
|---|---|---|
| id | AutoField | PK |
| mascota | FK → Mascota | Mascota del turno |
| veterinario | FK → Usuario | Veterinario asignado (rol=veterinario) |
| tipo_consulta | CharField choices | consulta_general / vacunacion / control / urgencia / cirugia |
| duracion_minutos | PositiveIntegerField | Auto-set por tipo, ajustable. Default 30 |
| fecha_hora | DateTimeField | Fecha y hora del turno (debe ser futura) |
| motivo | CharField(255) | Motivo ingresado por el Dueño |
| estado | CharField choices | pendiente / aprobado / rechazado / completado / cancelado |
| notas_recepcion | TextField | Notas internas (blank) |
| motivo_rechazo | TextField | Obligatorio al rechazar (blank en otros estados) |
| motivo_cancelacion | TextField | Obligatorio al cancelar (blank en otros estados) |
| fecha_creacion | DateTimeField | Auto al crear |

**Propiedad calculada:** `fecha_hora_fin = fecha_hora + timedelta(minutes=duracion_minutos)`  
Usada para el control de disponibilidad (RN-003).

---

### CambioEstadoTurno (nuevo — auditoría)

Registra cada transición de estado de un turno. Implementa RN-008.

| Campo | Tipo | Descripción |
|---|---|---|
| id | AutoField | PK |
| turno | FK → Turno | Turno al que pertenece |
| estado_anterior | CharField choices | Estado antes del cambio |
| estado_nuevo | CharField choices | Estado después del cambio |
| realizado_por | FK → Usuario | Quién hizo el cambio |
| fecha_hora | DateTimeField | Auto al crear |
| motivo | TextField | Motivo cuando aplica (blank en otros casos) |

---

## Diagrama de relaciones

```
Usuario ◄──────────────────── Turno ────────────────────► Mascota
  ▲                             │                              │
  │ (realizado_por)             │ (historial_estados)          │ (dueno)
  │                             ▼                              ▼
  └──────────── CambioEstadoTurno                          Usuario
```

---

## Decisiones de diseño

**CambioEstadoTurno como modelo separado**
El historial es una lista (N registros por turno). Usar campos individuales en Turno (aprobado_por, rechazado_por...) genera columnas que quedan vacías y no soportan múltiples cambios del mismo tipo.

**duracion_minutos como campo editable**
Se auto-completa desde el tipo de consulta pero la recepcionista puede ajustarlo caso a caso. El valor por defecto viene del diccionario `DURACIONES_POR_TIPO`.

**motivo_rechazo / motivo_cancelacion en Turno**
Permiten acceso rápido desde la vista del Dueño sin join adicional. El modelo de auditoría también los guarda para el historial completo.

---

## Duraciones por tipo de consulta

| Tipo | Duración (min) |
|---|---|
| Consulta general | 30 |
| Vacunación | 15 |
| Control | 20 |
| Urgencia | 45 |
| Cirugía | 90 |

---

## Transiciones de estado válidas (ver RN-001)

```
Pendiente ──► Aprobado   (Recepcionista/Admin)
Pendiente ──► Rechazado  (Recepcionista/Admin)
Pendiente ──► Cancelado  (Dueño / Recepcionista / Admin)
Aprobado  ──► Completado (Recepcionista/Admin)
Aprobado  ──► Cancelado  (Dueño / Recepcionista / Admin)
Rechazado, Cancelado, Completado → estados terminales
```
