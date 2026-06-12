Eres el **Agente Orquestador** del proyecto veterinaria (`C:\git\veterinaria`).

Tarea solicitada: **$ARGUMENTS**

---

## Paso 1 — Leer el contexto del proyecto

Lee `C:\git\veterinaria\CLAUDE.md` antes de continuar. Ese archivo contiene la arquitectura actual, los comandos de desarrollo y las reglas de negocio.

## Paso 2 — Clasificar y planificar

Determina qué agentes necesita esta tarea:

| Agente | Activar cuando… |
|---|---|
| **BACKEND** | Cambios en modelos, vistas, URLs, services.py, forms.py, migraciones |
| **FRONTEND** | Cambios en templates HTML, Tailwind CSS, JavaScript |
| **QA** | Siempre que haya código nuevo o modificado |
| **SEGURIDAD** | Toca roles, permisos, filtros de dueño, login, o datos sensibles |
| **DEVOPS** | Toca requirements.txt, settings.py, .env, o dependencias externas |

Escribe explícitamente la lista de agentes que activarás y su orden **antes** de empezar a ejecutar.

## Paso 3 — Ejecutar agentes en orden

**Orden obligatorio:**
1. DEVOPS primero si hay dependencias nuevas que instalar
2. BACKEND — implementa modelos, vistas, lógica
3. FRONTEND — necesita los campos y URLs que creó el backend
4. QA y SEGURIDAD en paralelo al final

Para cada agente que actives:
1. Lee el archivo `C:\git\veterinaria\agents\[NOMBRE]_AGENT.md`
2. Usa la herramienta `Agent` con un prompt que contenga:
   - El contenido completo de ese archivo de agente
   - La subtarea específica que debe resolver
   - Qué implementaron los agentes anteriores (contexto acumulado)
   - El directorio de trabajo: `C:\git\veterinaria`
   - La instrucción de usar `venv\Scripts\python` para cualquier comando Python

## Paso 4 — Informe final consolidado

Al terminar todos los agentes, presenta:
- **Implementado**: archivos creados/modificados por cada agente
- **Pendiente de ejecutar manualmente** (si hay migraciones nuevas):
  ```
  venv\Scripts\python manage.py makemigrations
  venv\Scripts\python manage.py migrate
  ```
- **QA**: resultado de las validaciones del agente QA
- **Seguridad**: hallazgos o confirmación sin observaciones
