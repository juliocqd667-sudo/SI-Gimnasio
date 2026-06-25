from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.db.utils import ProgrammingError
from .models import Bitacora
from .middleware import get_current_request

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    # Avoid logging Bitacora itself to prevent infinite loop
    if sender == Bitacora:
        return
    request = get_current_request()
    user = None
    ip = None
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
        ip = request.META.get('REMOTE_ADDR')
    action = 'Creado' if created else 'Actualizado'
    descripcion = f'{sender.__name__} instance {instance.pk} {action.lower()}'
    try:
        Bitacora.objects.create(
            usuario=user,
            accion=action,
            descripcion=descripcion,
            ip_address=ip
        )
    except ProgrammingError:
        # Table doesn't exist yet (likely during migration), skip logging
        pass

@receiver(pre_delete)
def log_model_delete(sender, instance, **kwargs):
    if sender == Bitacora:
        return
    request = get_current_request()
    user = None
    ip = None
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
        ip = request.META.get('REMOTE_ADDR')
    try:
        Bitacora.objects.create(
            usuario=user,
            accion='Eliminado',
            descripcion=f'{sender.__name__} instance {instance.pk} eliminado',
            ip_address=ip
        )
    except ProgrammingError:
        # Table doesn't exist yet (likely during migration), skip logging
        pass

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    try:
        Bitacora.objects.create(
            usuario=user,
            accion='Inicio de sesión',
            descripcion=f'Usuario {user.username} inició sesión',
            ip_address=ip
        )
    except ProgrammingError:
        # Table doesn't exist yet (likely during migration), skip logging
        pass

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR') if request else None
    try:
        Bitacora.objects.create(
            usuario=user,
            accion='Cierre de sesión',
            descripcion=f'Usuario {user.username} cerró sesión',
            ip_address=ip
        )
    except ProgrammingError:
        # Table doesn't exist yet (likely during migration), skip logging
        pass

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR') if request else None
    username = credentials.get('username') if credentials else 'desconocido'
    try:
        Bitacora.objects.create(
            usuario=None,  # No user because login failed
            accion='Intento de inicio de sesión fallido',
            descripcion=f'Intento fallido para usuario {username}',
            ip_address=ip
        )
    except ProgrammingError:
        # Table doesn't exist yet (likely during migration), skip logging
        pass
