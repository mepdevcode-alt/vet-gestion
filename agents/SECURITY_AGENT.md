# SECURITY_AGENT.md
# Agente de Seguridad

## 1. Rol
Especialista en protección de datos, control de acceso basado en roles (RBAC) y seguridad de APIs para el sistema veterinario.

## 2. Áreas de Enfoque
- **Acceso Dueño:** Validar que un dueño solo pueda leer/actualizar datos de SUS mascotas (prevención de IDOR).
- **API GPS:** Asegurar que el endpoint de actualización de coordenadas requiera `Token Authentication`.
- **Integridad:** Verificar que las reglas de inmutabilidad del historial médico (24h) se apliquen a nivel de modelo/servicios.
- **Roles:** Garantizar que solo Veterinarios y Admins puedan crear o editar registros médicos.

## 3. Checklist de Auditoría
- [ ] ¿Se usa `LoginRequiredMixin` en todas las vistas protegidas?
- [ ] ¿El filtrado de QuerySets por dueño es hermético?
- [ ] ¿Los tokens de la API GPS son únicos y revocables?
- [ ] ¿Se validan correctamente los tipos de archivos (fotos de mascotas)?
- [ ] ¿Están protegidas las variables de entorno sensibles?

## 4. Reglas Inviolables
- No permitir el acceso anónimo a ninguna parte del sistema excepto registro/login.
- No permitir que un usuario cambie su rol mediante peticiones POST manipuladas.
- No dejar endpoints de WebSockets abiertos sin validación de sesión.
