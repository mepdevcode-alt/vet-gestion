# Módulo de Turnos — Casos de Uso

**Responsable:** Ariel  
**Fecha:** 2026-06-13  
**Estado:** Completado  

---

## Actores

| Actor | Descripción |
|---|---|
| Dueño | Solicita y cancela sus propios turnos |
| Recepcionista | Gestiona (aprueba, rechaza, cancela, completa) todos los turnos |
| Admin | Mismos permisos que Recepcionista + acceso total |
| Veterinario | Consulta sus turnos del día (solo lectura) |

---

## CU-001 — Solicitar turno

**Actor:** Dueño  
**Precondición:** El Dueño tiene sesión iniciada y al menos una mascota registrada.

**Flujo principal:**
1. El Dueño accede a "Solicitar turno"
2. Selecciona una de sus mascotas
3. Selecciona el tipo de consulta (consulta general / vacunación / cirugía / urgencia / control)
4. Selecciona un veterinario disponible
5. Selecciona fecha y hora
6. Confirma la solicitud
7. El sistema crea el turno en estado Pendiente

**Flujos alternativos:**
- 2a. El Dueño no tiene mascotas → el sistema muestra un mensaje indicándolo y enlaza al alta de mascota
- 4a. No hay veterinarios activos → el sistema informa que no hay disponibilidad
- 7a. El Dueño ya tiene 3 turnos pendientes → el sistema bloquea la solicitud con mensaje explicativo

**Postcondición:** Turno creado en estado Pendiente, visible para Recepcionista/Admin.

---

## CU-002 — Ver mis turnos

**Actor:** Dueño  
**Precondición:** Sesión iniciada.

**Flujo principal:**
1. El Dueño accede a "Mis turnos"
2. El sistema muestra únicamente los turnos de sus propias mascotas
3. Cada turno muestra: mascota, veterinario, fecha/hora, tipo de consulta, estado

**Flujos alternativos:**
- 2a. Sin turnos → el sistema muestra mensaje vacío con botón "Solicitar turno"

---

## CU-003 — Cancelar turno (Dueño)

**Actor:** Dueño  
**Precondición:** El turno existe, pertenece al Dueño, y está en estado Pendiente o Aprobado.

**Flujo principal:**
1. El Dueño selecciona un turno y elige "Cancelar"
2. El sistema solicita motivo de cancelación (obligatorio)
3. El Dueño confirma
4. El sistema cambia el estado a Cancelado y registra el motivo y quién canceló

**Flujos alternativos:**
- 1a. El turno está en estado Completado, Rechazado o ya Cancelado → opción "Cancelar" no disponible

---

## CU-004 — Aprobar turno

**Actor:** Recepcionista / Admin  
**Precondición:** El turno existe en estado Pendiente.

**Flujo principal:**
1. El actor accede a la lista de turnos pendientes
2. Selecciona un turno y elige "Aprobar"
3. El sistema verifica que el veterinario no tenga otro turno aprobado que se solape en esa franja horaria (fecha_hora + duración)
4. El sistema cambia el estado a Aprobado y registra quién aprobó y cuándo

**Flujos alternativos:**
- 3a. Hay conflicto de horario → el sistema bloquea la aprobación e informa el conflicto (turno y horario que colisiona)

---

## CU-005 — Rechazar turno

**Actor:** Recepcionista / Admin  
**Precondición:** El turno existe en estado Pendiente.

**Flujo principal:**
1. El actor selecciona el turno y elige "Rechazar"
2. El sistema solicita motivo de rechazo (obligatorio)
3. El actor ingresa el motivo y confirma
4. El sistema cambia el estado a Rechazado, guarda el motivo y registra quién rechazó y cuándo

---

## CU-006 — Cancelar turno (Recepcionista / Admin)

**Actor:** Recepcionista / Admin  
**Precondición:** El turno está en estado Pendiente o Aprobado.

**Flujo principal:**
1. El actor selecciona el turno y elige "Cancelar"
2. El sistema solicita motivo (obligatorio)
3. El actor confirma
4. El sistema cambia el estado a Cancelado y registra el motivo y quién canceló

---

## CU-007 — Completar turno

**Actor:** Recepcionista / Admin  
**Precondición:** El turno está en estado Aprobado.

**Flujo principal:**
1. El actor selecciona el turno y elige "Completar"
2. El sistema cambia el estado a Completado y registra quién completó y cuándo
3. El sistema habilita la creación de factura asociada al turno

**Flujos alternativos:**
- 1a. El turno no está Aprobado → opción "Completar" no disponible

---

## CU-008 — Ver agenda

**Actor:** Recepcionista / Admin  
**Precondición:** Sesión iniciada.

**Flujo principal:**
1. El actor accede a "Agenda"
2. El sistema muestra los turnos aprobados del día actual organizados por hora
3. El actor puede navegar entre días (anterior / siguiente)
4. Puede filtrar por veterinario

---

## CU-009 — Ver turnos del día (Veterinario)

**Actor:** Veterinario  
**Precondición:** Sesión iniciada.

**Flujo principal:**
1. El Veterinario accede a su dashboard o a "Mis turnos del día"
2. El sistema muestra los turnos aprobados del día asignados a ese veterinario
3. Cada turno muestra: hora, mascota, dueño, tipo de consulta, duración estimada

---

## Diagrama de estados del Turno

```
                    ┌─────────┐
         solicitud  │         │
        ──────────► │PENDIENTE│
                    │         │
                    └────┬────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
           aprobar    rechazar   cancelar
              │          │          │
              ▼          ▼          ▼
         ┌─────────┐ ┌──────────┐ ┌──────────┐
         │APROBADO │ │RECHAZADO │ │CANCELADO │
         └────┬────┘ └──────────┘ └──────────┘
              │
     ┌────────┴────────┐
  completar          cancelar
     │                 │
     ▼                 ▼
┌───────────┐    ┌──────────┐
│COMPLETADO │    │CANCELADO │
└───────────┘    └──────────┘
```
