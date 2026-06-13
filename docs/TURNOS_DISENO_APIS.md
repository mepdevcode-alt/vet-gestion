# Módulo de Turnos — Diseño de URLs y Vistas

**Responsable:** Ariel  
**Fecha:** 2026-06-13  
**Estado:** Completado  

> Este proyecto usa Django Templates (sin DRF). Las "APIs" son las URLs y vistas Django — la interfaz entre el frontend y el backend.

---

## Mapa de URLs

| Método | URL | Vista | Rol requerido | Caso de uso |
|---|---|---|---|---|
| GET | `/turnos/` | `MisTurnosView` | Dueño | CU-002 |
| GET/POST | `/turnos/solicitar/` | `SolicitarTurnoView` | Dueño | CU-001 |
| GET/POST | `/turnos/<id>/cancelar/` | `CancelarTurnoView` | Dueño / Recep / Admin | CU-003, CU-006 |
| GET | `/turnos/gestion/` | `GestionTurnosView` | Recep / Admin | — |
| GET | `/turnos/agenda/` | `AgendaView` | Recep / Admin | CU-008 |
| POST | `/turnos/<id>/aprobar/` | `AprobarTurnoView` | Recep / Admin | CU-004 |
| GET/POST | `/turnos/<id>/rechazar/` | `RechazarTurnoView` | Recep / Admin | CU-005 |
| POST | `/turnos/<id>/completar/` | `CompletarTurnoView` | Recep / Admin | CU-007 |
| GET | `/turnos/<id>/` | `DetalleTurnoView` | Todos | — |
| GET | `/turnos/mis-turnos-hoy/` | `TurnosHoyVetView` | Veterinario | CU-009 |

---

## Detalle de vistas

### MisTurnosView — GET
- Filtra: `Turno.objects.filter(mascota__dueno=request.user)` (RN-007)
- Contexto: lista de turnos ordenados por fecha, paginados
- Template: `turnos/mis_turnos.html`

### SolicitarTurnoView — GET / POST
- GET: renderiza formulario con mascotas del dueño y veterinarios disponibles
- POST: llama a `services.crear_turno(dueno, datos)` — valida RN-005 y RN-006
- Template: `turnos/solicitar.html`

### GestionTurnosView — GET
- Muestra todos los turnos, filtrables por estado / veterinario / fecha
- Solo Recepcionista / Admin
- Template: `turnos/gestion.html`

### AprobarTurnoView — POST
- Sin template propio (acción directa, redirige)
- Llama a `services.aprobar_turno(turno, usuario)` — valida RN-003 (disponibilidad)
- Conflicto: redirige con mensaje de error | OK: redirige a gestión con éxito

### RechazarTurnoView — GET / POST
- GET: formulario con campo `motivo_rechazo`
- POST: llama a `services.rechazar_turno(turno, usuario, motivo)`
- Template: `turnos/rechazar.html`

### CancelarTurnoView — GET / POST
- Funciona para Dueño y para Recep/Admin (misma vista, permiso diferente)
- GET: formulario con campo `motivo_cancelacion`
- POST: llama a `services.cancelar_turno(turno, usuario, motivo)` — verifica RN-010 (factura)
- Template: `turnos/cancelar.html`

### CompletarTurnoView — POST
- Sin template propio (acción directa, redirige)
- Llama a `services.completar_turno(turno, usuario)`
- Solo funciona si `turno.estado == APROBADO`

### AgendaView — GET
- Parámetro opcional `?fecha=YYYY-MM-DD` (default: hoy) y `?veterinario=<id>`
- Filtra: turnos aprobados del día ordenados por hora
- Template: `turnos/agenda.html`

### TurnosHoyVetView — GET
- Filtra: turnos aprobados de hoy del veterinario logueado
- Template: `turnos/turnos_hoy_vet.html`

### DetalleTurnoView — GET
- Muestra el turno + historial de cambios de estado (`historial_estados`)
- Dueño solo puede ver sus propios turnos (filtro por rol)
- Template: `turnos/detalle.html`

---

## urls.py

```python
from django.urls import path
from . import views

app_name = 'turnos'

urlpatterns = [
    path('',                    views.MisTurnosView.as_view(),      name='mis_turnos'),
    path('solicitar/',          views.SolicitarTurnoView.as_view(), name='solicitar'),
    path('gestion/',            views.GestionTurnosView.as_view(),  name='gestion'),
    path('agenda/',             views.AgendaView.as_view(),         name='agenda'),
    path('mis-turnos-hoy/',     views.TurnosHoyVetView.as_view(),   name='turnos_hoy_vet'),
    path('<int:pk>/',           views.DetalleTurnoView.as_view(),   name='detalle'),
    path('<int:pk>/aprobar/',   views.AprobarTurnoView.as_view(),   name='aprobar'),
    path('<int:pk>/rechazar/',  views.RechazarTurnoView.as_view(),  name='rechazar'),
    path('<int:pk>/cancelar/',  views.CancelarTurnoView.as_view(),  name='cancelar'),
    path('<int:pk>/completar/', views.CompletarTurnoView.as_view(), name='completar'),
]
```
