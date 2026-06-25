from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Crea los grupos de usuario y asigna sus permisos por defecto'

    def handle(self, *args, **options):
        # Definición de Roles y sus permisos (formato: app_label.action_modelname)
        roles = {
            'Administrativo': [
                # Core
                'core.view_customuser', 'core.add_customuser', 'core.change_customuser', 'core.delete_customuser',
                'core.view_administrativo', 'core.add_administrativo', 'core.change_administrativo', 'core.delete_administrativo',
                'core.view_cliente', 'core.add_cliente', 'core.change_cliente', 'core.delete_cliente',
                'core.view_instructor', 'core.add_instructor', 'core.change_instructor', 'core.delete_instructor',
                'core.view_nutricionista', 'core.add_nutricionista', 'core.change_nutricionista', 'core.delete_nutricionista',
                # Finanzas
                'finanzas.view_promocion', 'finanzas.add_promocion', 'finanzas.change_promocion', 'finanzas.delete_promocion',
                'finanzas.view_suscripcion', 'finanzas.add_suscripcion', 'finanzas.change_suscripcion', 'finanzas.delete_suscripcion',
                'finanzas.view_pago', 'finanzas.add_pago', 'finanzas.change_pago', 'finanzas.delete_pago',
                'finanzas.view_comprobante', 'finanzas.add_comprobante', 'finanzas.change_comprobante', 'finanzas.delete_comprobante',
                # Actividades (Gestión de base)
                'actividades.view_sala', 'actividades.add_sala', 'actividades.change_sala', 'actividades.delete_sala',
                'actividades.view_disciplina', 'actividades.add_disciplina', 'actividades.change_disciplina', 'actividades.delete_disciplina',
                'actividades.view_horario', 'actividades.add_horario', 'actividades.change_horario', 'actividades.delete_horario',
                'actividades.view_reserva', 'actividades.add_reserva', 'actividades.change_reserva', 'actividades.delete_reserva',
            ],
            'Instructor': [
                # Actividades (Específicas de su trabajo)
                'actividades.view_rutina', 'actividades.add_rutina', 'actividades.change_rutina', 'actividades.delete_rutina',
                'actividades.view_ejercicio', 'actividades.add_ejercicio', 'actividades.change_ejercicio', 'actividades.delete_ejercicio',
                'actividades.view_detallerutina', 'actividades.add_detallerutina', 'actividades.change_detallerutina', 'actividades.delete_detallerutina',
                'actividades.view_seguimiento', 'actividades.add_seguimiento', 'actividades.change_seguimiento', 'actividades.delete_seguimiento',
                # Lectura de apoyo
                'actividades.view_sala', 'actividades.view_disciplina', 'actividades.view_horario',
                'core.view_cliente',
            ],
            'Nutricionista': [
                # Actividades (Específicas)
                'actividades.view_antecedentes', 'actividades.add_antecedentes', 'actividades.change_antecedentes', 'actividades.delete_antecedentes',
                # Lectura de apoyo
                'core.view_cliente',
            ],
            'Cliente': [
                # Sus propias cosas (esto se filtrará en las views, pero necesitan permiso de base)
                'actividades.view_rutina', 'actividades.view_ejercicio', 'actividades.view_detallerutina',
                'actividades.view_disciplina', 'actividades.view_horario',
                'actividades.view_reserva', 'actividades.add_reserva',
                'finanzas.view_suscripcion',
                'finanzas.view_pago', 'finanzas.add_pago',
                'finanzas.view_comprobante',
            ]
        }

        for role_name, permissions in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{role_name}" creado.'))
            
            # Limpiar permisos actuales para evitar duplicados o basura
            group.permissions.clear()

            for perm_code in permissions:
                app_label, codename = perm_code.split('.')
                try:
                    permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Permiso "{codename}" no encontrado en "{app_label}".'))

            self.stdout.write(self.style.SUCCESS(f'Permisos asignados al grupo "{role_name}".'))

        self.stdout.write(self.style.SUCCESS('Sincronización de roles completada con éxito.'))

        # Sincronizar usuarios existentes
        self.stdout.write('Sincronizando grupos para usuarios existentes...')
        from core.models import CustomUser
        users = CustomUser.objects.all()
        for user in users:
            # Esto disparará el signal post_save que ya implementamos
            user.save()
        self.stdout.write(self.style.SUCCESS(f'Se han sincronizado {users.count()} usuarios.'))
