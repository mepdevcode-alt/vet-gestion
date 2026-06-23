from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Carga registros de prueba en todas las tablas'

    def handle(self, *args, **options):
        from apps.usuarios.models import Usuario
        from apps.mascotas.models import Mascota
        from apps.historial.models import ConsultaMedica, HistoriaClinica
        from apps.turnos.models import Turno
        from apps.facturacion.models import Factura, ItemFactura
        from apps.adopciones.models import MascotaAdopcion

        self.stdout.write('Eliminando datos previos de prueba...')
        ItemFactura.objects.all().delete()
        Factura.objects.all().delete()
        ConsultaMedica.objects.all().delete()
        HistoriaClinica.objects.all().delete()
        Turno.objects.all().delete()
        Mascota.objects.all().delete()
        MascotaAdopcion.objects.all().delete()
        Usuario.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creando usuarios...')

        PASS_ADMIN = 'Admin123.'
        PASS_STAFF = '123456'

        admin = Usuario.objects.create_user(
            username='admin_clinica',
            password=PASS_ADMIN,
            first_name='Roberto',
            last_name='Gómez',
            email='admin@clinica.com',
            rol='admin',
            telefono='1145678901',
            is_staff=True,
            is_superuser=True,
        )

        vet1 = Usuario.objects.create_user(
            username='dra_sofia',
            password=PASS_STAFF,
            first_name='Sofía',
            last_name='Ramírez',
            email='sofia@clinica.com',
            rol='veterinario',
            telefono='1156789012',
        )

        vet2 = Usuario.objects.create_user(
            username='dr_carlos',
            password=PASS_STAFF,
            first_name='Carlos',
            last_name='Mendoza',
            email='carlos@clinica.com',
            rol='veterinario',
            telefono='1167890123',
        )

        recep = Usuario.objects.create_user(
            username='recep_lucia',
            password=PASS_STAFF,
            first_name='Lucía',
            last_name='Fernández',
            email='lucia@clinica.com',
            rol='recepcionista',
            telefono='1178901234',
        )

        dueno1 = Usuario.objects.create_user(
            username='juan_perez',
            password=PASS_STAFF,
            first_name='Juan',
            last_name='Pérez',
            email='juan@gmail.com',
            rol='dueno',
            telefono='1189012345',
        )

        dueno2 = Usuario.objects.create_user(
            username='maria_lopez',
            password=PASS_STAFF,
            first_name='María',
            last_name='López',
            email='maria@gmail.com',
            rol='dueno',
            telefono='1190123456',
        )

        dueno3 = Usuario.objects.create_user(
            username='andres_garcia',
            password=PASS_STAFF,
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

        # ── Rex ──────────────────────────────────────────────────────────────
        turno_rex1 = Turno.objects.create(
            mascota=rex, veterinario=vet1,
            tipo_consulta='vacunacion', duracion_minutos=15,
            fecha_hora=ahora - timedelta(days=30),
            motivo='Vacunación antirrábica anual',
            estado='completado',
            notas_recepcion='Paciente llegó a tiempo. Sin inconvenientes.',
        )
        turno_rex2 = Turno.objects.create(
            mascota=rex, veterinario=vet1,
            tipo_consulta='consulta_general', duracion_minutos=30,
            fecha_hora=ahora - timedelta(days=12),
            motivo='Revisión dermatológica por picazón excesiva',
            estado='completado',
            notas_recepcion='Se tomaron muestras para análisis.',
        )
        turno_rex3 = Turno.objects.create(
            mascota=rex, veterinario=vet2,
            tipo_consulta='control', duracion_minutos=20,
            fecha_hora=ahora + timedelta(days=7),
            motivo='Control post-tratamiento dermatitis',
            estado='aprobado',
            notas_recepcion='Turno confirmado vía WhatsApp.',
        )

        # ── Luna ─────────────────────────────────────────────────────────────
        turno_luna1 = Turno.objects.create(
            mascota=luna, veterinario=vet2,
            tipo_consulta='consulta_general', duracion_minutos=30,
            fecha_hora=ahora - timedelta(days=20),
            motivo='Revisión por pérdida de apetito',
            estado='completado',
            notas_recepcion='Se realizó análisis de sangre completo.',
        )
        turno_luna2 = Turno.objects.create(
            mascota=luna, veterinario=vet2,
            tipo_consulta='control', duracion_minutos=20,
            fecha_hora=ahora - timedelta(days=8),
            motivo='Control gastritis — seguimiento tratamiento',
            estado='completado',
            notas_recepcion='Mejoría notable. Se suspende medicación.',
        )
        turno_luna3 = Turno.objects.create(
            mascota=luna, veterinario=vet1,
            tipo_consulta='vacunacion', duracion_minutos=15,
            fecha_hora=ahora + timedelta(days=14),
            motivo='Vacuna triple felina',
            estado='pendiente',
            notas_recepcion='',
        )

        # ── Kiwi ─────────────────────────────────────────────────────────────
        turno_kiwi1 = Turno.objects.create(
            mascota=kiwi, veterinario=vet1,
            tipo_consulta='consulta_general', duracion_minutos=30,
            fecha_hora=ahora - timedelta(days=45),
            motivo='Primera consulta — revisión general',
            estado='completado',
            notas_recepcion='Ave en buen estado. Pico y plumaje normales.',
        )
        turno_kiwi2 = Turno.objects.create(
            mascota=kiwi, veterinario=None,
            tipo_consulta='control', duracion_minutos=20,
            fecha_hora=ahora + timedelta(days=3),
            motivo='Control de peso y plumaje',
            estado='pendiente',
            notas_recepcion='',
        )
        turno_kiwi3 = Turno.objects.create(
            mascota=kiwi, veterinario=vet1,
            tipo_consulta='consulta_general', duracion_minutos=30,
            fecha_hora=ahora - timedelta(days=5),
            motivo='Dificultad respiratoria leve',
            estado='rechazado',
            notas_recepcion='',
            motivo_rechazo='Veterinario sin disponibilidad. Se reagendó.',
        )

        # ── Max ───────────────────────────────────────────────────────────────
        turno_max1 = Turno.objects.create(
            mascota=max_, veterinario=vet1,
            tipo_consulta='consulta_general', duracion_minutos=30,
            fecha_hora=ahora - timedelta(days=60),
            motivo='Consulta por cojera en pata trasera derecha',
            estado='completado',
            notas_recepcion='Radiografía solicitada.',
        )
        turno_max2 = Turno.objects.create(
            mascota=max_, veterinario=vet1,
            tipo_consulta='control', duracion_minutos=20,
            fecha_hora=ahora - timedelta(days=7),
            motivo='Desparasitación trimestral',
            estado='aprobado',
            notas_recepcion='Turno confirmado vía telefónica.',
        )
        turno_max3 = Turno.objects.create(
            mascota=max_, veterinario=vet2,
            tipo_consulta='cirugia', duracion_minutos=90,
            fecha_hora=ahora + timedelta(days=21),
            motivo='Extirpación lipoma — zona lumbar',
            estado='aprobado',
            notas_recepcion='Pre-quirúrgico solicitado. Ayuno de 12 h previo.',
        )

        # ── Mimi ─────────────────────────────────────────────────────────────
        turno_mimi1 = Turno.objects.create(
            mascota=mimi, veterinario=vet2,
            tipo_consulta='cirugia', duracion_minutos=90,
            fecha_hora=ahora - timedelta(days=5),
            motivo='Castración programada',
            estado='rechazado',
            notas_recepcion='',
            motivo_rechazo='Propietario canceló. Reagendar próxima semana.',
        )
        turno_mimi2 = Turno.objects.create(
            mascota=mimi, veterinario=vet2,
            tipo_consulta='cirugia', duracion_minutos=90,
            fecha_hora=ahora + timedelta(days=15),
            motivo='Castración — reagendado',
            estado='aprobado',
            notas_recepcion='Pre-quirúrgico ya realizado. Ayuno confirmado.',
        )
        turno_mimi3 = Turno.objects.create(
            mascota=mimi, veterinario=vet1,
            tipo_consulta='vacunacion', duracion_minutos=15,
            fecha_hora=ahora + timedelta(days=8),
            motivo='Vacuna antirrábica pendiente',
            estado='pendiente',
            notas_recepcion='',
        )

        # ── Rocky ─────────────────────────────────────────────────────────────
        turno_rocky1 = Turno.objects.create(
            mascota=rocky, veterinario=vet1,
            tipo_consulta='urgencia', duracion_minutos=45,
            fecha_hora=ahora - timedelta(days=3),
            motivo='Ingesta accidental de cable eléctrico',
            estado='completado',
            notas_recepcion='Atención urgente. Propietario llegó sin turno.',
        )
        turno_rocky2 = Turno.objects.create(
            mascota=rocky, veterinario=vet1,
            tipo_consulta='control', duracion_minutos=20,
            fecha_hora=ahora + timedelta(days=10),
            motivo='Control post-urgencia — revisión digestiva',
            estado='aprobado',
            notas_recepcion='Turno asignado correctamente.',
        )
        turno_rocky3 = Turno.objects.create(
            mascota=rocky, veterinario=vet2,
            tipo_consulta='consulta_general', duracion_minutos=30,
            fecha_hora=ahora + timedelta(days=25),
            motivo='Control de peso y dieta',
            estado='pendiente',
            notas_recepcion='',
        )

        # ── Hoy (para que los veterinarios vean turnos en "Mis Turnos de Hoy") ──
        hoy_10 = ahora.replace(hour=10, minute=0, second=0, microsecond=0)
        hoy_11 = ahora.replace(hour=11, minute=30, second=0, microsecond=0)
        hoy_14 = ahora.replace(hour=14, minute=0, second=0, microsecond=0)
        hoy_15 = ahora.replace(hour=15, minute=30, second=0, microsecond=0)

        Turno.objects.create(
            mascota=rex, veterinario=vet1,
            tipo_consulta='control', duracion_minutos=20,
            fecha_hora=hoy_10,
            motivo='Control rutinario — seguimiento peso',
            estado='aprobado',
            notas_recepcion='Confirmado. Propietario avisado.',
        )
        Turno.objects.create(
            mascota=luna, veterinario=vet1,
            tipo_consulta='vacunacion', duracion_minutos=15,
            fecha_hora=hoy_11,
            motivo='Vacuna triple felina anual',
            estado='aprobado',
            notas_recepcion='Primer turno del día para Dra. Sofía.',
        )
        Turno.objects.create(
            mascota=max_, veterinario=vet2,
            tipo_consulta='consulta_general', duracion_minutos=30,
            fecha_hora=hoy_14,
            motivo='Revisión post-radiografía pata trasera',
            estado='aprobado',
            notas_recepcion='Propietario trae las placas.',
        )
        Turno.objects.create(
            mascota=rocky, veterinario=vet2,
            tipo_consulta='control', duracion_minutos=20,
            fecha_hora=hoy_15,
            motivo='Control digestivo post-urgencia',
            estado='aprobado',
            notas_recepcion='',
        )

        self.stdout.write(self.style.SUCCESS(f'  OK {Turno.objects.count()} turnos creados'))

        # referencias para facturas (turnos completados)
        turno1      = turno_rex1
        turno2      = turno_luna1
        turno3      = turno_max2
        turno5      = turno_mimi1

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

        self.stdout.write('Creando historias clínicas...')

        # ── Rex ──────────────────────────────────────────────────────────────
        HistoriaClinica.objects.create(
            mascota=rex,
            creado_por=vet1,
            veterinario_responsable=vet1,
            propietario_nombre='Juan Pérez',
            propietario_documento='30456789',
            propietario_direccion='Av. Corrientes 1234, CABA',
            propietario_telefono='1189012345',
            propietario_email='juan@gmail.com',
            paciente_sexo='M',
            paciente_color_pelaje='Dorado / caramelo uniforme',
            paciente_microchip='941000023456781',
            paciente_procedencia='Criadero La Pampa Dogs',
            paciente_fin_zootecnico='Mascota de compañía',
            paciente_senas_particulares='Cicatriz pequeña en oreja derecha por mordedura de cachorro.',
            motivo_consulta='Control anual y vacunación antirrábica. Propietario refiere picazón ocasional en zona dorsal.',
            dieta='Balanceado premium adulto 400 g/día. Sin premios extras.',
            enfermedades_previas='Dermatitis atópica estacional diagnosticada en 2023.',
            medicacion_actual='Ninguna al momento de la consulta.',
            vacunacion='Antirrábica (2024), Séxtuple (2024), Bordetella (2023).',
            desparasitacion='Interna: Milbemax cada 3 meses. Externa: Bravecto cada 4 meses.',
            esterilizado=False,
            observaciones_anamnesis='Animal sociable, sin historia de agresividad. Convive con gata Luna.',
            temperatura=Decimal('38.6'),
            frecuencia_cardiaca=88,
            frecuencia_respiratoria=22,
            peso_actual=Decimal('28.50'),
            diagnostico_presuntivo='Dermatitis alérgica estacional recurrente.',
            diagnostico_definitivo='Dermatitis alérgica estacional. Estado general óptimo.',
            tratamiento='Antihistamínico oral 5 mg/kg por 5 días. Baño semanal con shampoo hipoalergénico.',
            medicacion_prescrita='Cetirizina 10 mg — 1 comprimido diario por 5 días.',
            observaciones_clinicas='Se recomienda evitar contacto con pasto recién cortado. Próximo control en 30 días.',
            proxima_visita=date(2026, 7, 22),
            evolucion='Mejoría significativa a los 7 días del tratamiento. Sin nuevos episodios de rascado.',
        )

        HistoriaClinica.objects.create(
            mascota=rex,
            creado_por=vet2,
            veterinario_responsable=vet2,
            propietario_nombre='Juan Pérez',
            propietario_documento='30456789',
            propietario_direccion='Av. Corrientes 1234, CABA',
            propietario_telefono='1189012345',
            propietario_email='juan@gmail.com',
            paciente_sexo='M',
            paciente_color_pelaje='Dorado / caramelo uniforme',
            paciente_microchip='941000023456781',
            paciente_procedencia='Criadero La Pampa Dogs',
            paciente_fin_zootecnico='Mascota de compañía',
            motivo_consulta='Seguimiento post-vacuna antirrábica. Control dermatológico.',
            dieta='Balanceado premium adulto 400 g/día.',
            medicacion_actual='Cetirizina suspendida hace 2 semanas.',
            vacunacion='Al día. Ver HC anterior.',
            desparasitacion='Al día.',
            esterilizado=False,
            temperatura=Decimal('38.4'),
            frecuencia_cardiaca=84,
            frecuencia_respiratoria=20,
            peso_actual=Decimal('28.80'),
            diagnostico_presuntivo='Control post-tratamiento.',
            diagnostico_definitivo='Resolución completa del cuadro de dermatitis. Sin nuevas lesiones.',
            tratamiento='Sin medicación. Continuar con shampoo hipoalergénico quincenal.',
            observaciones_clinicas='Peso estable. Pelaje en buen estado. Alta definitiva del episodio.',
            proxima_visita=date(2026, 12, 1),
            evolucion='Paciente sin síntomas. Alta médica.',
        )

        # ── Luna ─────────────────────────────────────────────────────────────
        HistoriaClinica.objects.create(
            mascota=luna,
            creado_por=vet2,
            veterinario_responsable=vet2,
            propietario_nombre='Juan Pérez',
            propietario_documento='30456789',
            propietario_direccion='Av. Corrientes 1234, CABA',
            propietario_telefono='1189012345',
            propietario_email='juan@gmail.com',
            paciente_sexo='H',
            paciente_color_pelaje='Crema con puntos seal en cara, patas y cola',
            paciente_microchip='',
            paciente_procedencia='Adopción particular',
            paciente_fin_zootecnico='Mascota de compañía',
            paciente_senas_particulares='Ojos azules. Cola con curvatura leve hacia la izquierda.',
            motivo_consulta='Pérdida de apetito progresiva de 5 días. Vómito ocasional (2 episodios).',
            dieta='Alimento húmedo y seco mixto. 150 g/día.',
            enfermedades_previas='Sin antecedentes relevantes.',
            medicacion_actual='Ninguna.',
            vacunacion='Triple felina (2025). Rabia (2025).',
            desparasitacion='Profender spot-on cada 6 meses.',
            esterilizado=True,
            observaciones_anamnesis='Animal de interior. No accede a la calle. Convive con perro Rex.',
            temperatura=Decimal('38.9'),
            frecuencia_cardiaca=180,
            frecuencia_respiratoria=28,
            peso_actual=Decimal('4.20'),
            diagnostico_presuntivo='Gastritis aguda. Posible intolerancia alimentaria.',
            diagnostico_definitivo='Gastritis leve. Análisis de sangre sin alteraciones relevantes.',
            tratamiento='Omeprazol 2.5 mg/kg cada 24 h por 7 días. Dieta blanda 5 días.',
            medicacion_prescrita='Omeprazol 10 mg — 1/4 comprimido diario por 7 días.',
            observaciones_clinicas='Controlar ingesta de agua. Consultar si no mejora en 72 h.',
            proxima_visita=date(2026, 7, 5),
            evolucion='A los 3 días recuperó el apetito. Completó el tratamiento sin inconvenientes.',
        )

        # ── Kiwi ─────────────────────────────────────────────────────────────
        HistoriaClinica.objects.create(
            mascota=kiwi,
            creado_por=vet1,
            veterinario_responsable=vet1,
            propietario_nombre='María López',
            propietario_documento='27891234',
            propietario_direccion='Calle Rivadavia 567, GBA',
            propietario_telefono='1190123456',
            propietario_email='maria@gmail.com',
            paciente_sexo='M',
            paciente_color_pelaje='Verde con amarillo en pecho. Manchas azules en mejillas.',
            paciente_microchip='',
            paciente_procedencia='Pajarera El Colibri',
            paciente_fin_zootecnico='Mascota de compañía',
            paciente_senas_particulares='Anilla naranja en pata izquierda.',
            motivo_consulta='Primera consulta veterinaria. Propietaria refiere que el ave come poco y tiene las plumas erizadas.',
            dieta='Mezcla de semillas comercial. Acceso a agua fresca.',
            enfermedades_previas='Sin antecedentes.',
            medicacion_actual='Ninguna.',
            vacunacion='No aplica en aves de compañía.',
            desparasitacion='Sin desparasitación previa.',
            esterilizado=False,
            observaciones_anamnesis='Ave adquirida hace 3 meses. Convive sola en jaula amplia. Temperatura ambiente 22°C.',
            temperatura=Decimal('40.5'),
            frecuencia_cardiaca=None,
            frecuencia_respiratoria=None,
            peso_actual=Decimal('0.08'),
            diagnostico_presuntivo='Síndrome de plumas erizadas. Posible estrés o deficiencia nutricional.',
            diagnostico_definitivo='Déficit nutricional leve. Estado general aceptable para la edad.',
            tratamiento='Suplemento vitamínico en agua 0.5 ml/día por 15 días. Agregar frutas y verduras a la dieta.',
            medicacion_prescrita='Vitaminol Aves — 5 gotas en bebedero diariamente.',
            observaciones_clinicas='Cubrir jaula por las noches. Evitar corrientes de aire. Control en 30 días.',
            proxima_visita=date(2026, 7, 15),
            evolucion='A los 15 días las plumas mejoraron notablemente. Aumentó la ingesta.',
        )

        # ── Max ───────────────────────────────────────────────────────────────
        HistoriaClinica.objects.create(
            mascota=max_,
            creado_por=vet1,
            veterinario_responsable=vet1,
            propietario_nombre='María López',
            propietario_documento='27891234',
            propietario_direccion='Calle Rivadavia 567, GBA',
            propietario_telefono='1190123456',
            propietario_email='maria@gmail.com',
            paciente_sexo='M',
            paciente_color_pelaje='Dorado oscuro. Pelaje liso y abundante.',
            paciente_microchip='941000034567892',
            paciente_procedencia='Refugio municipal GBA Norte',
            paciente_fin_zootecnico='Mascota de compañía',
            paciente_senas_particulares='Nevo pequeño despigmentado en región lumbar derecha (lipoma en seguimiento).',
            motivo_consulta='Cojera progresiva en miembro posterior derecho de 2 semanas de evolución. Sin traumatismo previo conocido.',
            dieta='Balanceado adulto raza grande 450 g/día + suplemento articular.',
            enfermedades_previas='Sin antecedentes de importancia.',
            medicacion_actual='Condroitín + glucosamina oral desde hace 2 meses.',
            vacunacion='Séxtuple (2025). Antirrábica (2025). Leptospirosis (2025).',
            desparasitacion='Interna y externa al día.',
            esterilizado=False,
            cirugias_previas='Sin cirugías previas.',
            observaciones_anamnesis='Animal de alta actividad. Paseos 2 veces al día, 40 min c/u. Escaleras en domicilio.',
            temperatura=Decimal('38.7'),
            frecuencia_cardiaca=76,
            frecuencia_respiratoria=18,
            peso_actual=Decimal('32.10'),
            diagnostico_presuntivo='Displasia de cadera leve o lesión ligamentaria. Se solicita radiografía.',
            diagnostico_definitivo='Laxitud ligamentaria rodilla derecha. Sin evidencia de displasia en placas. Lipoma lumbar estable.',
            tratamiento='Reposo relativo 3 semanas. Continuar suplemento articular. AINEs 3 días. Reevaluar en 21 días.',
            medicacion_prescrita='Meloxicam 0.1 mg/kg una vez al día por 3 días con comida.',
            observaciones_clinicas='Radiografía archivada en legajo. Vigilar el lipoma: si crece, extirpación quirúrgica.',
            proxima_visita=date(2026, 7, 13),
            evolucion='Mejoría de la cojera a los 10 días. Se suspendió AINE. Lipoma estable sin crecimiento.',
        )

        HistoriaClinica.objects.create(
            mascota=max_,
            creado_por=vet2,
            veterinario_responsable=vet2,
            propietario_nombre='María López',
            propietario_documento='27891234',
            propietario_direccion='Calle Rivadavia 567, GBA',
            propietario_telefono='1190123456',
            propietario_email='maria@gmail.com',
            paciente_sexo='M',
            paciente_color_pelaje='Dorado oscuro.',
            paciente_microchip='941000034567892',
            paciente_procedencia='Refugio municipal GBA Norte',
            paciente_fin_zootecnico='Mascota de compañía',
            motivo_consulta='Control post-tratamiento laxitud ligamentaria. Evaluación lipoma lumbar para decisión quirúrgica.',
            dieta='Balanceado adulto raza grande 450 g/día.',
            medicacion_actual='Condroitín + glucosamina. Sin AINEs.',
            vacunacion='Al día.',
            desparasitacion='Al día.',
            esterilizado=False,
            temperatura=Decimal('38.5'),
            frecuencia_cardiaca=78,
            frecuencia_respiratoria=19,
            peso_actual=Decimal('32.40'),
            diagnostico_presuntivo='Lipoma en crecimiento. Indicación quirúrgica.',
            diagnostico_definitivo='Lipoma lumbar con aumento de 1.5 cm respecto a control anterior. Se indica extirpación.',
            tratamiento='Cirugía programada. Pre-quirúrgico completo solicitado. Ayuno de 12 h previo.',
            medicacion_prescrita='Amoxicilina + ácido clavulánico 20 mg/kg cada 12 h por 7 días post-cirugía (a confirmar).',
            observaciones_clinicas='Turno quirúrgico coordinado. Propietaria informada de riesgos y procedimiento.',
            proxima_visita=date(2026, 7, 22),
            evolucion='Pendiente de cirugía.',
        )

        # ── Mimi ─────────────────────────────────────────────────────────────
        HistoriaClinica.objects.create(
            mascota=mimi,
            creado_por=vet2,
            veterinario_responsable=vet2,
            propietario_nombre='Andrés García',
            propietario_documento='25678901',
            propietario_direccion='Belgrano 890, GBA Sur',
            propietario_telefono='1101234567',
            propietario_email='andres@gmail.com',
            paciente_sexo='H',
            paciente_color_pelaje='Blanco con manchas grises en lomo. Pelo largo y sedoso.',
            paciente_microchip='',
            paciente_procedencia='Criadero felino CABA',
            paciente_fin_zootecnico='Mascota de compañía / exposición',
            paciente_senas_particulares='Ojos ámbar. Bigotes extralargas. Cola muy poblada.',
            motivo_consulta='Consulta pre-quirúrgica castración. Propietario solicita esterilización.',
            dieta='Alimento seco premium adulto 120 g/día.',
            enfermedades_previas='Sin antecedentes.',
            medicacion_actual='Ninguna.',
            vacunacion='Triple felina (2025). Leucemia felina (2024).',
            desparasitacion='Profender cada 6 meses. Al día.',
            esterilizado=False,
            observaciones_anamnesis='Gata de interior exclusivo. Sin contacto con otros animales. En celo cada 3 semanas aprox.',
            temperatura=Decimal('38.8'),
            frecuencia_cardiaca=172,
            frecuencia_respiratoria=26,
            peso_actual=Decimal('3.80'),
            diagnostico_presuntivo='Paciente en condiciones para cirugía.',
            diagnostico_definitivo='Animal sano. Apto para anestesia general y ovariohisterectomía.',
            tratamiento='Programar cirugía. Pre-quirúrgico: hemograma + bioquímica. Ayuno 8 h previo.',
            medicacion_prescrita='Pre-anestésico según protocolo clínico el día de la cirugía.',
            observaciones_clinicas='Propietario firmó consentimiento informado. Turno reagendado por cancelación previa.',
            proxima_visita=date(2026, 7, 7),
            evolucion='Pendiente de cirugía. Pre-quirúrgico sin alteraciones.',
        )

        # ── Rocky ─────────────────────────────────────────────────────────────
        HistoriaClinica.objects.create(
            mascota=rocky,
            creado_por=vet1,
            veterinario_responsable=vet1,
            propietario_nombre='Andrés García',
            propietario_documento='25678901',
            propietario_direccion='Belgrano 890, GBA Sur',
            propietario_telefono='1101234567',
            propietario_email='andres@gmail.com',
            paciente_sexo='M',
            paciente_color_pelaje='Blanco con mancha marrón en ojo derecho. Orejas caídas.',
            paciente_microchip='',
            paciente_procedencia='Tienda de mascotas ZooPet',
            paciente_fin_zootecnico='Mascota de compañía',
            paciente_senas_particulares='Pata trasera derecha con leve desviación congénita. No genera limitación.',
            motivo_consulta='Urgencia: propietario refiere que el conejo ingirió parte de un cable eléctrico hace 2 horas. Sin convulsiones. Come.',
            dieta='Heno Timothy ad libitum. Pellets 30 g/día. Verduras frescas.',
            enfermedades_previas='Sin antecedentes.',
            medicacion_actual='Ninguna.',
            vacunacion='VHD (Enfermedad Hemorrágica del Conejo) al día.',
            desparasitacion='Sin desparasitación formal. Ambiente interior.',
            esterilizado=False,
            observaciones_anamnesis='Conejo de interior. Acceso libre a sala de estar. Propietario no pudo cuantificar cantidad ingerida.',
            temperatura=Decimal('38.2'),
            frecuencia_cardiaca=210,
            frecuencia_respiratoria=55,
            peso_actual=Decimal('2.30'),
            diagnostico_presuntivo='Posible intoxicación por ingesta de aislante plástico. Descartar obstrucción digestiva.',
            diagnostico_definitivo='Irritación gástrica leve por ingesta de material plástico. Sin obstrucción. Sin signos neurológicos.',
            tratamiento='Carbón activado 1 g/kg VO dosis única. Protector gástrico 3 días. Dieta blanda 48 h. Control en 24 h.',
            medicacion_prescrita='Carbón activado 2.3 g en 5 ml agua VO — dosis única administrada en clínica.\nOmeprazol conejo 0.5 mg/kg cada 24 h por 3 días.',
            observaciones_clinicas='Se administró carbón en clínica. Animal estable al alta. Propietario instruido sobre señales de alarma: anorexia, distensión abdominal, convulsiones.',
            proxima_visita=date(2026, 6, 25),
            evolucion='Control a las 24 h: deposiciones normales. Sin distensión. Alta definitiva a las 48 h.',
        )

        self.stdout.write(self.style.SUCCESS(f'  OK {HistoriaClinica.objects.count()} historias clínicas creadas'))

        self.stdout.write('Creando mascotas en adopción...')

        MascotaAdopcion.objects.create(
            nombre='Bruno',
            especie='perro',
            raza='Labrador mix',
            edad='2 años',
            sexo='macho',
            tamanio='grande',
            descripcion='Bruno es un perro muy cariñoso y juguetón. Le encanta correr y jugar con pelotas. Lleva 3 meses en el refugio y busca una familia con espacio al aire libre.',
            vacunado=True,
            castrado=True,
            disponible=True,
            destacado=True,
            fecha_ingreso=date(2026, 3, 10),
            ubicacion='Buenos Aires',
            refugio='Refugio Patitas Felices',
        )

        MascotaAdopcion.objects.create(
            nombre='Mochi',
            especie='gato',
            raza='Mestizo',
            edad='8 meses',
            sexo='hembra',
            tamanio='pequeño',
            descripcion='Mochi es una gatita muy curiosa y activa. Fue rescatada de la calle siendo cachorra. Ideal para departamento, convive bien con otros gatos.',
            vacunado=True,
            castrado=False,
            disponible=True,
            destacado=True,
            fecha_ingreso=date(2026, 4, 1),
            ubicacion='Buenos Aires',
            refugio='Refugio Patitas Felices',
        )

        MascotaAdopcion.objects.create(
            nombre='Toto',
            especie='perro',
            raza='Beagle',
            edad='4 años',
            sexo='macho',
            tamanio='mediano',
            descripcion='Toto fue abandonado por su anterior familia al mudarse. Es tranquilo, obediente y ya sabe varios comandos básicos. Excelente con niños.',
            vacunado=True,
            castrado=True,
            disponible=True,
            destacado=False,
            fecha_ingreso=date(2026, 2, 20),
            ubicacion='GBA Norte',
            refugio='Hogar Transitorio Canino',
        )

        MascotaAdopcion.objects.create(
            nombre='Nala',
            especie='gato',
            raza='Angora mix',
            edad='3 años',
            sexo='hembra',
            tamanio='mediano',
            descripcion='Nala es una gata independiente pero muy cariñosa con quien se gana su confianza. Prefiere ambientes tranquilos y sin perros.',
            vacunado=True,
            castrado=True,
            disponible=True,
            destacado=False,
            fecha_ingreso=date(2026, 1, 15),
            ubicacion='Buenos Aires',
            refugio='Refugio Patitas Felices',
        )

        MascotaAdopcion.objects.create(
            nombre='Pipa',
            especie='conejo',
            raza='Holandés enano',
            edad='1 año',
            sexo='hembra',
            tamanio='pequeño',
            descripcion='Pipa es una coneja muy dócil y sociable. Come bien, no da problemas y es perfecta para quienes buscan una mascota tranquila. Viene con jaula.',
            vacunado=False,
            castrado=False,
            disponible=True,
            destacado=False,
            fecha_ingreso=date(2026, 5, 3),
            ubicacion='GBA Sur',
            refugio='Rescate Pequeños Amigos',
        )

        MascotaAdopcion.objects.create(
            nombre='Thor',
            especie='perro',
            raza='Pastor Alemán mix',
            edad='1 año',
            sexo='macho',
            tamanio='grande',
            descripcion='Thor es joven y tiene muchísima energía. Necesita actividad física diaria y espacio para correr. Está en proceso de socialización con otros perros.',
            vacunado=True,
            castrado=False,
            disponible=True,
            destacado=True,
            fecha_ingreso=date(2026, 5, 18),
            ubicacion='Buenos Aires',
            refugio='Hogar Transitorio Canino',
        )

        self.stdout.write(self.style.SUCCESS(f'  OK {MascotaAdopcion.objects.count()} mascotas en adopción creadas'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Datos de prueba cargados exitosamente ==='))
        self.stdout.write('')
        self.stdout.write('Credenciales de acceso:')
        self.stdout.write('  admin_clinica  / Admin123.  (Admin — superusuario)')
        self.stdout.write('  dra_sofia      / 123456     (Veterinario)')
        self.stdout.write('  dr_carlos      / 123456     (Veterinario)')
        self.stdout.write('  recep_lucia    / 123456     (Recepcionista)')
        self.stdout.write('  juan_perez     / 123456     (Dueño)')
        self.stdout.write('  maria_lopez    / 123456     (Dueño)')
        self.stdout.write('  andres_garcia  / 123456     (Dueño)')
