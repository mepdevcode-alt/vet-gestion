# RULES.md - Reglas del Proyecto

## 1. Idioma Obligatorio
- **Código:** Nombres de variables, clases y funciones en **Español**.
- **Base de Datos:** Nombres de tablas y columnas en **Español**.
- **Comentarios:** Documentación y comentarios de código en **Español**.
- **Interfaz:** 100% en **Español**.

## 2. Reglas de Negocio Inviolables
- **Mascotas:** La fecha de nacimiento no puede ser mayor a la fecha actual.
- **Historial Médico:** Una vez creado un registro, solo puede editarse o eliminarse dentro de las **24 horas** posteriores. Después, es de solo lectura.
- **GPS:** El rastro en el mapa debe mostrar las últimas **5 posiciones**. El estado cambia a "Desconectado" tras **10 minutos** de inactividad.

## 3. Estándares de Código
- Seguir **PEP 8** para Python.
- Utilizar **Type Hints** en funciones y métodos.
- Las vistas de Django deben usar **Class Based Views (CBVs)** preferentemente.
- No se permiten bibliotecas de Frontend como React o Vue. Solo Django Templates + JS Vanilla.

## 4. Seguridad y Privacidad
- **Filtrado por Dueño:** Todas las queries en vistas accesibles por dueños deben filtrar por `dueño=request.user`.
- **DRF:** Los endpoints de la API deben estar protegidos por Token y tener `Throttling` configurado.
- **Secrets:** Nunca subir el archivo `.env` o credenciales al repositorio.
