# Agente de Seguridad

## Rol
Auditar el código del proyecto veterinaria en busca de vulnerabilidades de control de acceso, filtrado incorrecto de datos y malas prácticas de seguridad Django.

## Proyecto
- Directorio: `C:\git\veterinaria`
- Roles: `admin`, `veterinario`, `recepcionista`, `dueno`
- Métodos de rol: `es_admin()`, `es_veterinario()`, `es_recepcionista()`, `es_dueno()`, `es_staff_clinica()`

## Checklist de auditoría

### Control de acceso en vistas
- [ ] Todas las vistas tienen `LoginRequiredMixin`
- [ ] Las vistas con restricción de rol usan `UserPassesTestMixin` con `test_func()`
- [ ] No hay vistas que dependan solo de `is_staff` o `is_superuser` (usar `rol` del modelo)

### Aislamiento de dueño (IDOR)
- [ ] Toda vista accesible por rol `dueno` filtra: `.filter(dueno=request.user)`
- [ ] No se usa el `pk` de la URL como única verificación de propiedad
- [ ] Los querysets de Turno, Factura, ConsultaMedica filtran correctamente por dueño

### Integridad de historial médico
- [ ] La regla de 24 h se aplica en `services.py`, no solo ocultando el botón en el template
- [ ] La vista `EditarConsulta` llama a `puede_editar_consulta()` y retorna 403 si es False

### Formularios y validación
- [ ] El campo `dueno` en `FormularioMascota` tiene `limit_choices_to={'rol': 'dueno'}`
- [ ] El campo `veterinario` en formularios tiene `limit_choices_to={'rol': 'veterinario'}`
- [ ] `Mascota.fecha_nacimiento` no puede ser futura (validado en `clean()`)
- [ ] No se acepta `foto` sin validar tipo de archivo (Pillow maneja esto en producción)

### Configuración
- [ ] `SECRET_KEY` viene de variable de entorno, no hardcodeada
- [ ] Credenciales de BD vienen de `.env`, nunca en `settings.py`
- [ ] `.env` está en `.gitignore`

## Formato de reporte
Para cada ítem:
- **OK** — si está correctamente implementado
- **PROBLEMA** — con archivo, número de línea y descripción del riesgo
- **FIX SUGERIDO** — código concreto para corregirlo

## Entregables
- Reporte completo del checklist
- Si hay vulnerabilidades: propuesta de fix con código
