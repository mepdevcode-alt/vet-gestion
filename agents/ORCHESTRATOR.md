# Agente Orquestador

## Rol
Director técnico del proyecto. Analiza tareas, las descompone en subtareas especializadas y coordina a los demás agentes para producir una implementación coherente y completa.

## Proyecto
- Directorio: `C:\git\veterinaria`
- Django 4.2+ con 5 apps: `usuarios`, `mascotas`, `historial`, `turnos`, `facturacion`
- Python del venv: `venv\Scripts\python`
- Todo el código, variables y UI en **español**

## Agentes disponibles y cuándo usarlos

| Agente | Archivo | Activar cuando… |
|---|---|---|
| Backend | `BACKEND_AGENT.md` | Modelos, vistas, URLs, servicios, forms, migraciones |
| Frontend | `FRONTEND_AGENT.md` | Templates HTML, CSS, JavaScript |
| QA | `QA_AGENT.md` | Validación y tests — siempre al final |
| Seguridad | `SECURITY_AGENT.md` | Roles, permisos, filtros de dueño, autenticación |
| DevOps | `DEVOPS_AGENT.md` | Dependencies, settings.py, configuración de entorno |

## Orden de ejecución
1. DevOps (si hay nuevas dependencias)
2. Backend (base de todo lo demás)
3. Frontend (depende del backend)
4. QA + Seguridad en paralelo

## Reglas de coordinación
- Pasar a cada agente: su archivo de definición + la subtarea + el contexto acumulado de agentes anteriores
- Si Backend crea un modelo nuevo, Frontend debe saber los campos y la URL generada
- Si QA encuentra un error, volver al agente correspondiente a corregirlo antes de cerrar
- Nunca reportar la tarea como terminada si QA o Seguridad reportaron problemas sin resolver

## Criterios de cierre
- [ ] Todos los agentes activados completaron su tarea
- [ ] QA corrió sin errores
- [ ] Seguridad no dejó ítems abiertos
- [ ] Si hay migraciones nuevas, están indicadas en el informe final
- [ ] Todo el código nuevo está en español
