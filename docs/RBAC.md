# RBAC.md - Control de Acceso basado en Roles

## Definición de Roles
1. **ADMIN:** Acceso total a la administración, gestión de veterinarios y configuración del sistema.
2. **VETERINARIO:** Gestión de mascotas (CRUD) y creación de historias médicas. Puede ver todos los registros médicos.
3. **DUEÑO:** Gestión de sus propias mascotas. Visualización de ubicación GPS en tiempo real. Lectura de historial médico propio.

## Matriz de Permisos

| Módulo | Admin | Veterinario | Dueño |
| :--- | :---: | :---: | :---: |
| Crear Usuarios (Vet/Admin) | ✅ | ❌ | ❌ |
| Crear Mascotas | ✅ | ✅ | ❌ (Solo ver propias) |
| Editar Mascota | ✅ | ✅ | ❌ |
| Ver Mapa GPS | ✅ | ✅ | ✅ (Solo propias) |
| Crear Historia Médica | ❌ | ✅ | ❌ |
| Editar Historia Médica | ❌ | ✅ (< 24h) | ❌ |
| Ver Historial Médico | ✅ | ✅ | ✅ (Solo propias) |

## Implementación en Django
- Uso de `user.role` (campo en `AbstractUser`).
- Decoradores `@login_required` y `@user_passes_test`.
- Mixins como `LoginRequiredMixin` y `UserPassesTestMixin`.
- **Filtro de Ownership:** En las vistas de Dueño, siempre usar `Mascota.objects.filter(dueño=request.user)`.
