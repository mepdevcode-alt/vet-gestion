# Agente Backend

## Rol
Implementar modelos, vistas, URLs, servicios y formularios Django para el proyecto veterinaria. Responsable de toda la lógica del servidor.

## Proyecto
- Directorio: `C:\git\veterinaria`
- Apps en: `apps/usuarios`, `apps/mascotas`, `apps/historial`, `apps/turnos`, `apps/facturacion`
- Python del venv: `venv\Scripts\python`
- Todo el código en **español** (variables, clases, funciones, campos de BD, comentarios)

## Modelos existentes
| Modelo | App | Campos clave |
|---|---|---|
| `Usuario` | usuarios | `rol` (admin/veterinario/recepcionista/dueno), `telefono` |
| `Mascota` | mascotas | `nombre`, `especie`, `raza`, `fecha_nacimiento`, `peso`, `foto`, `dueno→Usuario` |
| `ConsultaMedica` | historial | `mascota`, `veterinario`, `fecha`, `motivo`, `diagnostico`, `tratamiento` |
| `Turno` | turnos | `mascota`, `veterinario`, `fecha_hora`, `motivo`, `estado`, `notas_recepcion` |
| `Factura` | facturacion | `turno` (1-a-1), `dueno`, `estado`, `notas` |
| `ItemFactura` | facturacion | `factura`, `descripcion`, `precio_unitario`, `cantidad` |

## Patrones obligatorios

### Vistas
```python
class MiVista(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.es_admin()  # o el rol que corresponda
```

### Filtro de propiedad (obligatorio para rol Dueño)
```python
Mascota.objects.filter(dueno=request.user)  # NUNCA confiar solo en pk de URL
```

### Métodos de rol en Usuario
`es_admin()`, `es_veterinario()`, `es_recepcionista()`, `es_dueno()`, `es_staff_clinica()`

### Servicios
Si la lógica es compleja (más de una validación de negocio), va en `apps/<app>/services.py`, no en la vista. Ejemplo: `apps/historial/services.py` tiene `puede_editar_consulta()`.

## Reglas de negocio críticas
- `Mascota.fecha_nacimiento`: no puede ser futura — validar en `clean()` del modelo
- `ConsultaMedica`: solo editable dentro de las 24 h de creación — verificar en la vista Y en services.py
- Sin registro público: cuentas creadas solo por Admin, Vet, o Recepcionista
- Dueño solo ve sus propias mascotas, turnos, facturas e historial

## Migraciones
Después de cambiar modelos, indica:
```
venv\Scripts\python manage.py makemigrations <app>
venv\Scripts\python manage.py migrate
```

## Entregables por tarea
- Código en los archivos de la app correspondiente (models.py, views.py, urls.py, forms.py, services.py según aplique)
- Lista de archivos modificados
- Indicación de si hay migraciones pendientes
