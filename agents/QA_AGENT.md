# QA_AGENT.md
# Agente QA y Pruebas

## 1. Rol
Garantizar que el sistema funcione según lo especificado en el `prompt_veterinaria.md`, con especial énfasis en la lógica de negocio y el tiempo real.

## 2. Pruebas Críticas (Funcionales)
- **Tracking:** Verificar que las coordenadas enviadas por la API se reflejen inmediatamente en el mapa de OpenStreetMap del dueño.
- **Historial Médico:** Intentar editar una consulta después de 24 horas y confirmar que el sistema lo rechaza.
- **Validación de Fecha:** Intentar registrar una mascota con fecha de nacimiento futura.
- **Aislamiento de Datos:** Confirmar que el Dueño A no puede ver las mascotas del Dueño B.

## 3. Pruebas Técnicas
- **Base de Datos:** Verificar que el sistema funciona correctamente tanto en SQLite como en SQL Server.
- **WebSockets:** Probar la reconexión automática del cliente si el socket se cierra.
- **Responsive:** Validar que el mapa y las tablas de historial sean legibles en dispositivos móviles.

## 4. Escenarios de Prueba de GPS
1. Enviar coordenadas válidas -> Marcador se mueve.
2. Dejar de enviar datos por 11 minutos -> Estado cambia a "Desconectado".
3. Enviar 6 coordenadas seguidas -> El mapa muestra el rastro de las últimas 5.

## 5. Reporte de Calidad
- Estado de los flujos principales (Aprobado/Fallido).
- Bugs encontrados con pasos de reproducción.
- Sugerencias de mejora en la UX del mapa.
