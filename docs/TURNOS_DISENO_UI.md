# Módulo de Turnos — Diseño de Interfaz y UX

**Responsable:** Ariel  
**Fecha:** 2026-06-13  
**Estado:** Completado  

---

## Pantallas del módulo

### 1. Mis Turnos — Dueño (`turnos/mis_turnos.html`)

- Lista de tarjetas, una por turno
- Cada tarjeta: mascota, tipo de consulta, veterinario, fecha/hora, badge de estado
- Botón "Cancelar" visible solo en Pendiente o Aprobado
- Botón "Ver detalle" siempre visible
- Botón prominente "Solicitar turno" en el encabezado
- Sin turnos: mensaje vacío + botón "Solicitar tu primer turno"

### 2. Solicitar Turno — Dueño (`turnos/solicitar.html`)

- Select de mascota (solo las del dueño)
- Select de tipo de consulta con duración estimada visible junto al label
- Select de veterinario
- DateTimePicker para fecha y hora
- Campo de texto para motivo
- Si el dueño ya tiene 3 pendientes: banner de advertencia arriba del formulario

### 3. Gestión de Turnos — Recep / Admin (`turnos/gestion.html`)

- Tabla con filtros: estado, veterinario, fecha
- Filtro por estado por defecto en "Pendiente" al entrar
- Columnas: hora, mascota, veterinario, tipo, estado, acciones
- Acciones por estado:
  - Pendiente: Aprobar | Rechazar | Ver
  - Aprobado: Completar | Cancelar | Ver
  - Terminales: solo Ver

### 4. Agenda — Recep / Admin (`turnos/agenda.html`)

- Vista de lista del día ordenada por hora
- Navegación entre días: ← Anterior | Fecha actual | Siguiente →
- Filtro por veterinario
- Barras de color proporcionales a la duración del turno
- "Sin turnos aprobados para este día" si no hay

### 5. Detalle de Turno — Todos (`turnos/detalle.html`)

- Info completa: mascota, veterinario, tipo, motivo, estado, duración
- Timeline del historial de cambios de estado: quién, cuándo, de qué estado a cuál
- Dueño: solo ve sus propios turnos

### 6. Rechazar (`turnos/rechazar.html`) / Cancelar (`turnos/cancelar.html`)

- Formulario simple con info del turno arriba para contexto
- Campo de motivo obligatorio
- Botones: Volver | Confirmar

### 7. Turnos del día — Veterinario (`turnos/turnos_hoy_vet.html`)

- Lista compacta de turnos aprobados de hoy asignados al veterinario
- Columnas: hora, mascota, dueño, tipo de consulta, duración

---

## Decisiones de UX

| Decisión | Justificación |
|---|---|
| Rechazar y cancelar requieren formulario (GET+POST) | Evita acciones destructivas accidentales desde un link |
| Aprobar y Completar son POST directos | Acciones positivas que no requieren texto de confirmación |
| Filtro de gestión por defecto en Pendiente | La recepcionista entra a resolver lo que está pendiente |
| Badge de color por estado | Reconocimiento visual sin necesidad de leer el texto |
| Duración visible junto al tipo de consulta | El dueño entiende cuánto tiempo reservar |
| Historial de estados en detalle | Transparencia: el dueño ve quién y cuándo cambió cada estado |

---

## Templates a crear

| Template | Ruta |
|---|---|
| Lista dueño | `templates/turnos/mis_turnos.html` |
| Solicitar | `templates/turnos/solicitar.html` |
| Gestión | `templates/turnos/gestion.html` |
| Agenda | `templates/turnos/agenda.html` |
| Detalle | `templates/turnos/detalle.html` |
| Rechazar | `templates/turnos/rechazar.html` |
| Cancelar | `templates/turnos/cancelar.html` |
| Turnos hoy (vet) | `templates/turnos/turnos_hoy_vet.html` |
