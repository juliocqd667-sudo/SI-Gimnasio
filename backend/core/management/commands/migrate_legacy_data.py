from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from core.models import CustomUser, Administrativo, Cliente, Instructor, Nutricionista
from finanzas.models import Promocion, Suscripcion, Pago, Comprobante
from actividades.models import Rutina, Ejercicio, DetalleRutina, Sala, Disciplina, Horario, Reserva, Seguimiento, Antecedentes
from datetime import date, time

class Command(BaseCommand):
    help = 'Migra los datos del sistema legacy de Laravel a Django'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando migración total de datos...')

        # 1. SUSCRIPCIONES
        suscripciones_data = [
            ('Premium', 'Diario', 'Acceso a 5 disciplinas', 15.00),
            ('Premium', 'Mensual', 'Acceso a 5 disciplinas', 120.00),
            ('Premium', 'Semestral', 'Acceso a 5 disciplinas', 650.00),
            ('Premium', 'Anual', 'Acceso a 5 disciplinas', 1200.00),
            ('Estándar', 'Diario', 'Acceso a 2 disciplinas', 10.00),
            ('Estándar', 'Mensual', 'Acceso a 2 disciplinas', 80.00),
            ('Estándar', 'Semestral', 'Acceso a 2 disciplinas', 450.00),
            ('Estándar', 'Anual', 'Acceso a 2 disciplinas', 850.00),
            ('Básica', 'Diario', 'Acceso solo a aparatos', 5.00),
            ('Básica', 'Mensual', 'Acceso solo a aparatos', 50.00),
            ('Básica', 'Semestral', 'Acceso solo a aparatos', 250.00),
            ('Básica', 'Anual', 'Acceso solo a aparatos', 450.00),
        ]
        for memb, plan, desc, precio in suscripciones_data:
            Suscripcion.objects.get_or_create(membresia=memb, plan=plan, defaults={'descripcion': desc, 'precio': precio})

        # 2. PROMOCIONES
        Promocion.objects.get_or_create(id=1001, defaults={
            'nombre': 'Promoción Verano', 'tipo': 'Descuento', 'valor': 15.00, 'estado': 'A',
            'fecha_ini': '2024-06-01', 'fecha_fin': '2024-08-31', 'descripcion': '15% de descuento en verano'
        })
        Promocion.objects.get_or_create(id=1002, defaults={
            'nombre': 'Black Friday', 'tipo': 'Descuento', 'valor': 50.00, 'estado': 'A',
            'fecha_ini': '2024-11-25', 'fecha_fin': '2024-12-01', 'descripcion': '50% de descuento Black Friday'
        })

        # 3. SALAS
        sala1, _ = Sala.objects.get_or_create(id=1, defaults={'descripcion': 'Sala 1', 'capacidad': 30})
        sala2, _ = Sala.objects.get_or_create(id=2, defaults={'descripcion': 'Sala 2', 'capacidad': 20})
        sala3, _ = Sala.objects.get_or_create(id=3, defaults={'descripcion': 'Sala 3', 'capacidad': 40})

        # 4. DISCIPLINAS
        disc_data = [
            (2001, 'Yoga', 1, 30, sala1),
            (2002, 'Zumba', 3, 40, sala3),
            (2003, 'Crossfit', 4, 20, sala2),
            (2004, 'Kickboxing', 5, 30, sala1),
            (2005, 'Spinning', 6, 20, sala2),
            (2006, 'Boxeo', 8, 40, sala3),
        ]
        for d_id, nom, grp, cupo, sala in disc_data:
            Disciplina.objects.get_or_create(id=d_id, defaults={'nombre': nom, 'grupo': grp, 'cupo': cupo, 'sala': sala, 'hora_inicial': '08:00', 'hora_final': '20:00'})

        # 5. EJERCICIOS
        ejercicios_list = [
            (500, 'Press Banca', 'Ejercicio para el pecho'),
            (501, 'Sentadilla', 'Ejercicio para las piernas'),
            (502, 'Peso Muerto', 'Ejercicio de levantamiento'),
            (503, 'Dominadas', 'Ejercicio de tracción'),
            (504, 'Fondos', 'Ejercicio de empuje'),
            (505, 'Press Militar', 'Ejercicio hombros'),
            (506, 'Peso Muerto Rumano', 'Variación isquios'),
            (507, 'Remo con Barra', 'Tracción espalda'),
            (508, 'Curl Bíceps', 'Aislamiento bíceps'),
            (509, 'Tríceps Polea', 'Ejercicio tríceps'),
        ]
        for e_id, nom, desc in ejercicios_list:
            Ejercicio.objects.get_or_create(id=e_id, defaults={'nombre': nom, 'descripcion': desc})

        # 6. RUTINAS
        rutina_fuerza, _ = Rutina.objects.get_or_create(id=100, defaults={'nombre': 'Rutina Fuerza', 'descripcion': 'Enfocada en fuerza'})
        rutina_volumen, _ = Rutina.objects.get_or_create(id=101, defaults={'nombre': 'Rutina Volumen', 'descripcion': 'Aumento masa muscular'})
        rutina_def, _ = Rutina.objects.get_or_create(id=102, defaults={'nombre': 'Rutina Definición', 'descripcion': 'Definición muscular'})

        # 7. DETALLE RUTINAS
        detalles_data = [
            ('Lunes', '5', '5', '100', 100, 500), ('Lunes', '5', '5', '120', 100, 501),
            ('Martes', '5', '5', '110', 100, 505), ('Martes', '5', '5', '120', 100, 506),
            ('Lunes', '10', '4', '80', 101, 500), ('Martes', '10', '4', '60', 101, 505),
        ]
        for dia, rep, ser, peso, rut_id, ej_id in detalles_data:
            DetalleRutina.objects.get_or_create(
                rutina_id=rut_id, ejercicio_id=ej_id, dia=dia,
                defaults={'repeticiones': rep, 'serie': ser, 'peso': peso}
            )

        # 8. USUARIOS
        users_to_create = [
            (20001, 'daniel', 'DANIEL RODRIGUEZ ROCA', '69161451', 'dr520878@gmail.com', True, False, False, False, '2004-10-09', 'M', '15645959'),
            (20002, 'leandro', 'LEANDRO ALVAREZ RODRIGUEZ', '68806043', 'leandro.ar2003@gmail.com', True, False, False, False, '2004-10-09', 'M', '13700836'),
            (20003, 'gabriela', 'GABRIELA TOMICHA PEREZ', '69139278', 'gabriela.3849@gmail.com', True, False, False, False, '2004-10-09', 'F', '14191910'),
            (20004, 'pablo', 'PABLO CAMACHO VÁSQUEZ', '78956321', 'pablocamacho.54@gmail.com', True, False, False, False, '2004-10-09', 'M', '18647324'),
            (20005, 'veronica', 'VERONICA LANZA CABRERA', '69124781', 'vero_lanza_c9845@gmail.com', True, False, False, False, '2004-10-09', 'F', '45982167'),
            (20006, 'alvaro', 'ALVARO DIEGO RODRIGUEZ CASTEDO', '78952103', 'alvaro.diego87_rodriguez@gmail.com', True, False, False, False, '2004-10-09', 'M', '23458726'),
            (20007, 'yerlin', 'YERLIN SAMEJA YABETA', '78951235', 'Sameja_yabeta987456@gmail.com', False, True, False, False, '2004-10-09', 'F', '21482347'),
            (20008, 'rodrigo', 'RODRIGO ROCHA ORTIZ', '65214878', 'rodrigorocha_rod@gmail.com', False, True, False, False, '2004-10-09', 'M', '98742614'),
            (20009, 'junior', 'JUNIOR HURTADO FLORES', '78549565', 'junior_hurtado874569212@gmail.com', False, True, False, False, '2004-10-09', 'M', '24875135'),
            (20010, 'raul', 'RAUL RODRIGUEZ RIVERO', '73265410', 'rodriguezrivero.ar5498@gmail.com', False, True, False, False, '2004-10-09', 'M', '75846921'),
            (20011, 'luis', 'LUIS FERNANDO GUASICO DOLEA', '65498787', 'lfgd.luis6549@gmail.com', False, True, False, False, '2004-10-09', 'M', '24568725'),
            (20012, 'elena', 'ELENA MENACHO PEREZ', '78456256', 'elena_menacho.em782@gmail.com', False, False, False, True, '2004-10-09', 'F', '31025492'),
            (20013, 'jose', 'JOSE CORRALES HINOJOSA', '75632524', 'luisito_corraleshinojosa@gmail.com', False, False, False, True, '2004-10-09', 'M', '35045065'),
            (20014, 'maria', 'MARIA RENE CESPEDES CANDIA', '65987413', 'maria_rene_cespedes875@gmail.com', False, False, False, True, '2004-10-09', 'F', '60058460'),
            (20015, 'carla', 'CARLA SUÁREZ GÓMEZ', '70123456', 'carlasuarez@gmail.com', False, False, True, False, '2004-10-09', 'F', '18746942'),
            (1, 'messi', 'Lionel Messi', '10101010', 'messi@gmail.com', True, True, True, True, '1987-06-24', 'M', 'messi123'),
        ]

        for ci, username, nom, tel, mail, is_c, is_i, is_n, is_a, f_nac, sexo, pwd in users_to_create:
            user, created = CustomUser.objects.get_or_create(username=username, defaults={
                'email': mail, 'first_name': nom.split(' ')[0], 'last_name': ' '.join(nom.split(' ')[1:]),
                'ci': ci, 'telefono': tel, 'is_cliente': is_c, 'is_instructor': is_i, 'is_nutricionista': is_n,
                'is_administrativo': is_a, 'fecha_nacimiento': f_nac, 'sexo': sexo
            })
            if created:
                user.set_password(pwd)
                user.save()
            
            if is_c: Cliente.objects.get_or_create(user=user)
            if is_i: Instructor.objects.get_or_create(user=user, defaults={'especialidad': 'General'})
            if is_n: Nutricionista.objects.get_or_create(user=user, defaults={'horario_atencion': 'Lunes a Viernes'})
            if is_a: Administrativo.objects.get_or_create(user=user, defaults={'cargo': 'Recepcionista', 'turno': 'Mañana'})

        # 9. HORARIOS
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        for d_id in [2001, 2002, 2003, 2004, 2005, 2006]:
            disc = Disciplina.objects.get(id=d_id)
            for d in dias_semana:
                Horario.objects.get_or_create(disciplina=disc, dia=d, hora_inicial=time(8,0), hora_final=time(9,0))

        # 10. PAGOS Y COMPROBANTES
        pagos_data = [
            (50000, 'daniel', 'elena', 'Premium', 'Mensual', 102.00, date(2024, 7, 1)),
            (50001, 'leandro', 'jose', 'Básica', 'Mensual', 50.00, date(2024, 8, 10)),
            (50002, 'gabriela', 'maria', 'Básica', 'Mensual', 25.00, date(2024, 11, 28)),
            (50003, 'pablo', 'elena', 'Premium', 'Anual', 1200.00, date(2024, 10, 15)),
        ]
        for p_id, u_cli, u_adm, memb, plan, monto, fecha in pagos_data:
            cliente = Cliente.objects.get(user__username=u_cli)
            admin = Administrativo.objects.get(user__username=u_adm)
            susc = Suscripcion.objects.get(membresia=memb, plan=plan)
            
            pago, created = Pago.objects.get_or_create(id=p_id, defaults={
                'metodo_pago': 'E', 'fecha': fecha, 'monto_total': monto,
                'cliente': cliente, 'administrador': admin, 'suscripcion': susc, 'estado_pago': 'Completado'
            })
            
            # Solo crear comprobante si el pago fue creado para evitar errores de UniqueConstraint
            if created:
                Comprobante.objects.create(
                    id=7000+p_id, monto=monto, fecha_ini_mem=fecha,
                    fecha_fin_mem=date(fecha.year, (fecha.month % 12) + 1, fecha.day),
                    pago=pago, cliente=cliente
                )

        # 11. ANTECEDENTES Y SEGUIMIENTOS
        nutri1 = Nutricionista.objects.get(user__username='carla')
        cliente_d = Cliente.objects.get(user__username='daniel')
        cliente_l = Cliente.objects.get(user__username='leandro')
        inst_y = Instructor.objects.get(user__username='yerlin')
        inst_r = Instructor.objects.get(user__username='rodrigo')

        Antecedentes.objects.get_or_create(id=10, defaults={
            'cliente': cliente_d, 'nutricionista': nutri1, 'fecha': date(2024,9,20),
            'fecha_prox_consulta': date(2024,10,20), 'diagnostico': 'Saludable',
            'recomendaciones': 'Continuar', 'objetivo': 'Adelgazar',
            'peso': 70.5, 'altura': 1.75, 'imc': 23.0, 'gc': 15.0, 'mm': 55.0
        })

        Seguimiento.objects.get_or_create(id=1500, defaults={
            'fecha': date(2024,9,1), 'observaciones': 'Buen progreso', 'objetivo': 'Adelgazar',
            'fecha_prox_consulta': date(2024,10,1), 'cliente': cliente_d, 'instructor': inst_y, 'rutina': rutina_fuerza
        })
        Seguimiento.objects.get_or_create(id=1501, defaults={
            'fecha': date(2024,9,5), 'observaciones': 'Sin dificultad', 'objetivo': 'Hipertrofia',
            'fecha_prox_consulta': date(2024,10,5), 'cliente': cliente_l, 'instructor': inst_r, 'rutina': rutina_volumen
        })

        self.stdout.write(self.style.SUCCESS('Migración total completada con éxito.'))
