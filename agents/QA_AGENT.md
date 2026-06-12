# Agente QA

## Rol
Validar que la implementación cumple las reglas de negocio y no introduce regresiones. Crear tests donde no existan.

## Proyecto
- Directorio: `C:\git\veterinaria`
- Ejecutar tests: `venv\Scripts\python manage.py test apps.<app>`
- Ejecutar todos los tests: `venv\Scripts\python manage.py test`

## Tests prioritarios por área

### Modelos
- `Mascota.fecha_nacimiento` futura debe fallar en `clean()`
- `ConsultaMedica` no editable después de 24 h (verificar en services.py)

### Vistas — aislamiento de dueño
- Un dueño NO puede acceder a mascotas de otro dueño por URL (IDOR)
- Un dueño NO puede ver turnos/facturas/historial ajenos

### Permisos de rol
- Recepcionista NO puede acceder a URLs de CRUD de mascotas
- Dueño NO puede aprobar/rechazar turnos
- Usuario anónimo redirige a login en todas las vistas protegidas

### Flujos de negocio
- Turno: transición de estados `pendiente → aprobado → completado`
- Factura: solo se puede crear desde un turno `completado`
- Factura con `estado=anulado` no debe sumarse en reportes

## Formato de tests
```python
# apps/<app>/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from apps.usuarios.models import Usuario
from apps.<app>.models import <Modelo>

class <Modelo>Tests(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_user(username='admin', password='pass', rol='admin')
        self.dueno = Usuario.objects.create_user(username='dueno', password='pass', rol='dueno')
        self.client = Client()

    def test_<nombre_descriptivo>(self):
        self.client.login(username='dueno', password='pass')
        response = self.client.get(reverse('<namespace>:<vista>', args=[...]))
        self.assertEqual(response.status_code, 200)  # o 403 según el caso
```

## Entregables
- Tests creados o actualizados en `apps/<app>/tests.py`
- Resultado de la corrida (`OK` o lista de fallos con descripción)
- Si hay fallos: descripción del problema y sugerencia de fix
