from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Carga registros de prueba en todas las tablas'

    def handle(self, *args, **options):
        from apps.usuarios.models import Usuario
        from apps.mascotas.models import Mascota
        from apps.historial.models import ConsultaMedica
        from apps.turnos.models import Turno
        from apps.facturacion.models import Factura, ItemFactura

        self.stdout.write('Eliminando datos previos de prueba...')
        ItemFactura.objects.all().delete()
        Factura.objects.all().delete()
        ConsultaMedica.objects.all().delete()
        Turno.objects.all().delete()
        Mascota.objects.all().delete()
        Usuario.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creando usuarios...')

        admin = Usuario.objects.create_user(
            username='admin_clinica',
            password='Test1234!',
            first_name='Roberto',
            last_name='Gómez',
            email='admin@clinica.com',
            rol='admin',
            telefono='1145678901',
            is_staff=True,
        )

        vet1 = Usuario.objects.create_user(
            username='dra_sofia',
            password='Test1234!',
            first_name='Sofía',
            last_name='Ramírez',
            email='sofia@clinica.com',
            rol='veterinario',
            telefono='1156789012',
        )

        vet2 = Usuario.objects.create_user(
            username='dr_carlos',
            password='Test1234!',
            first_name='Carlos',
            last_name='Mendoza',
            email='carlos@clinica.com',
            rol='veterinario',
            telefono='1167890123',
        )

        recep = Usuario.objects.create_user(
            username='recep_lucia',
            password='Test1234!',
            first_name='Lucía',
            last_name='Fernández',
            email='lucia@clinica.com',
            rol='recepcionista',
            telefono='1178901234',
        )

        dueno1 = Usuario.objects.create_user(
            username='juan_perez',
            password='Test1234!',
            first_name='Juan',
            last_name='Pérez',
            email='juan@gmail.com',
            rol='dueno',
            telefono='1189012345',
        )

        dueno2 = Usuario.objects.create_user(
            username='maria_lopez',
            password='Test1234!',
            first_name='María',
            last_name='López',
            email='maria@gmail.com',
            rol='dueno',
            telefono='1190123456',
        )

        dueno3 = Usuario.objects.create_user(
            username='andres_garcia',
            password='Test1234!',
            first_name='Andrés',
            last_name='García',
            email='andres@gmail.com',
            rol='dueno',
            telefono='1101234567',
        )

        self.stdout.write(self.style.SUCCESS(f'  OK {Usuario.objects.count()} usuarios creados'))

        self.stdout.write('Creando mascotas...')

        rex = Mascota.objects.create(
            nombre='Rex',
            especie='perro',
            raza='Labrador Retriever',
            fecha_nacimiento=date(2019, 3, 15),
            peso=Decimal('28.50'),
            dueno=dueno1,
        )

        luna = Mascota.objects.create(
            nombre='Luna',
            especie='gato',
            raza='Siamés',
            fecha_nacimiento=date(2021, 7, 22),
            peso=Decimal('4.20'),
            dueno=dueno1,
        )

        kiwi = Mascota.objects.create(
            nombre='Kiwi',
            especie='ave',
            raza='Periquito Australiano',
            fecha_nacimiento=date(2022, 1, 10),
            peso=Decimal('0.08'),
            dueno=dueno2,
        )

        max_ = Mascota.objects.create(
            nombre='Max',
            especie='perro',
            raza='Golden Retriever',
            fecha_nacimiento=date(2020, 11, 5),
            peso=Decimal('32.10'),
            dueno=dueno2,
        )

        mimi = Mascota.objects.create(
            nombre='Mimi',
            especie='gato',
            raza='Angora',
            fecha_nacimiento=date(2018, 6, 30),
            peso=Decimal('3.80'),
            dueno=dueno3,
        )

        rocky = Mascota.objects.create(
            nombre='Rocky',
            especie='otro',
            raza='Conejo Belier',
            fecha_nacimiento=date(2023, 4, 18),
            peso=Decimal('2.30'),
            dueno=dueno3,
        )

        self.stdout.write(self.style.SUCCESS(f'  OK {Mascota.objects.count()} mascotas creadas'))

        self.stdout.write('Creando turnos...')

        ahora = timezone.now()

        turno1 = Turno.objects.create(
            mascota=rex,
            veterinario=vet1,
            fecha_hora=ahora - timedelta(days=30),
            motivo='Control anual y vacunación antirrábica',
            estado='completado',
            notas_recepcion='Paciente llegó a tiempo. Sin inconvenientes.',
        )

        turno2 = Turno.objects.create(
            mascota=luna,
            veterinario=vet2,
            fecha_hora=ahora - timedelta(days=15),
            motivo='Revisión por pérdida de apetito',
            estado='completado',
            notas_recepcion='Se realizó análisis de sangre.',
        )

        turno3 = Turno.objects.create(
            mascota=max_,
            veterinario=vet1,
            fecha_hora=ahora - timedelta(days=7),
            motivo='Desparasitación trimestral',
            estado='aprobado',
            notas_recepcion='Turno confirmado vía telefónica.',
        )

        turno4 = Turno.objects.create(
            mascota=kiwi,
            veterinario=None,
            fecha_hora=ahora + timedelta(days=3),
            motivo='Primera consulta - revisión general',
            estado='pendiente',
            notas_recepcion='',
        )

        turno5 = Turno.objects.create(
            mascota=mimi,
            veterinario=vet2,
            fecha_hora=ahora - timedelta(days=5),
            motivo='Castración programada',
            estado='rechazado',
            notas_recepcion='Propietario canceló. Reagendar próxima semana.',
        )

        turno6 = Turno.objects.create(
            mascota=rocky,
            veterinario=vet1,
            fecha_hora=ahora + timedelta(days=10),
            motivo='Control de peso y dieta',
            estado='aprobado',
            notas_recepcion='Turno asignado correctamente.',
        )

        turno7 = Turno.objects.create(
            mascota=rex,
            veterinario=vet2,
            fecha_hora=ahora + timedelta(days=1),
            motivo='Seguimiento post-vacuna',
            estado='pendiente',
            notas_recepcion='',
        )

        self.stdout.write(self.style.SUCCESS(f'  OK {Turno.objects.count()} turnos creados'))

        self.stdout.write('Creando consultas médicas...')

        ConsultaMedica.objects.create(
            mascota=rex,
            veterinario=vet1,
            motivo='Control anual y vacunación antirrábica',
            diagnostico='Animal en buen estado general. Peso adecuado para su raza y edad.',
            tratamiento='Vacuna antirrábica aplicada. Próxima dosis en 12 meses.',
            observaciones='Se recomienda reducir levemente la porción diaria.',
        )

        ConsultaMedica.objects.create(
            mascota=luna,
            veterinario=vet2,
            motivo='Revisión por pérdida de apetito',
            diagnostico='Gastritis leve. Análisis de sangre sin alteraciones relevantes.',
            tratamiento='Omeprazol 2.5 mg/kg cada 24 horas por 7 días. Dieta blanda.',
            observaciones='Controlar ingesta de agua. Traer en 10 días si no mejora.',
        )

        ConsultaMedica.objects.create(
            mascota=rex,
            veterinario=vet1,
            motivo='Revisión dermatológica por picazón excesiva',
            diagnostico='Dermatitis alérgica estacional.',
            tratamiento='Antihistamínico oral 5 mg/kg por 5 días. Baño con shampoo hipoalergénico.',
            observaciones='Evitar contacto con pasto recién cortado.',
        )

        self.stdout.write(self.style.SUCCESS(f'  OK {ConsultaMedica.objects.count()} consultas médicas creadas'))

        self.stdout.write('Creando facturas e ítems...')

        factura1 = Factura.objects.create(
            turno=turno1,
            dueno=dueno1,
            estado='pagado',
            notas='Pago realizado en efectivo.',
        )
        ItemFactura.objects.create(
            factura=factura1,
            descripcion='Consulta veterinaria general',
            precio_unitario=Decimal('3500.00'),
            cantidad=1,
        )
        ItemFactura.objects.create(
            factura=factura1,
            descripcion='Vacuna antirrábica',
            precio_unitario=Decimal('2800.00'),
            cantidad=1,
        )
        ItemFactura.objects.create(
            factura=factura1,
            descripcion='Antiparasitario externo',
            precio_unitario=Decimal('1200.00'),
            cantidad=2,
        )

        factura2 = Factura.objects.create(
            turno=turno2,
            dueno=dueno1,
            estado='pendiente',
            notas='Pendiente de cobro. Cliente avisó que paga el viernes.',
        )
        ItemFactura.objects.create(
            factura=factura2,
            descripcion='Consulta veterinaria especializada',
            precio_unitario=Decimal('4500.00'),
            cantidad=1,
        )
        ItemFactura.objects.create(
            factura=factura2,
            descripcion='Análisis de sangre completo',
            precio_unitario=Decimal('6000.00'),
            cantidad=1,
        )
        ItemFactura.objects.create(
            factura=factura2,
            descripcion='Omeprazol 10 mg (blister)',
            precio_unitario=Decimal('950.00'),
            cantidad=1,
        )

        factura3 = Factura.objects.create(
            turno=turno3,
            dueno=dueno2,
            estado='pendiente',
            notas='',
        )
        ItemFactura.objects.create(
            factura=factura3,
            descripcion='Desparasitación interna y externa',
            precio_unitario=Decimal('2200.00'),
            cantidad=1,
        )
        ItemFactura.objects.create(
            factura=factura3,
            descripcion='Consulta veterinaria general',
            precio_unitario=Decimal('3500.00'),
            cantidad=1,
        )

        factura4 = Factura.objects.create(
            turno=turno5,
            dueno=dueno3,
            estado='anulado',
            notas='Turno rechazado. Factura anulada automáticamente.',
        )
        ItemFactura.objects.create(
            factura=factura4,
            descripcion='Castración felina',
            precio_unitario=Decimal('12000.00'),
            cantidad=1,
        )

        self.stdout.write(self.style.SUCCESS(f'  OK {Factura.objects.count()} facturas creadas'))
        self.stdout.write(self.style.SUCCESS(f'  OK {ItemFactura.objects.count()} ítems de factura creados'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Datos de prueba cargados exitosamente ==='))
        self.stdout.write('')
        self.stdout.write('Credenciales de acceso:')
        self.stdout.write('  admin_clinica  / Test1234!  (Admin)')
        self.stdout.write('  dra_sofia      / Test1234!  (Veterinario)')
        self.stdout.write('  dr_carlos      / Test1234!  (Veterinario)')
        self.stdout.write('  recep_lucia    / Test1234!  (Recepcionista)')
        self.stdout.write('  juan_perez     / Test1234!  (Dueño)')
        self.stdout.write('  maria_lopez    / Test1234!  (Dueño)')
        self.stdout.write('  andres_garcia  / Test1234!  (Dueño)')
