from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ci = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=8, null=True, blank=True)
    is_cliente = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_nutricionista = models.BooleanField(default=False)
    is_administrativo = models.BooleanField(default=False)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"

class Administrativo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    cargo = models.CharField(max_length=20)
    turno = models.CharField(max_length=6)

    def __str__(self):
        return f"Admin: {self.user.username}"

class Cliente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    domicilio = models.CharField(max_length=255, null=True, blank=True)
    suscripcion_activa = models.CharField(max_length=10, null=True, blank=True)
    fecha_ini_mem = models.DateField(null=True, blank=True)
    fecha_fin_mem = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Cliente: {self.user.username}"

class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=25)

    def __str__(self):
        return f"Instructor: {self.user.username}"

class Nutricionista(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    horario_atencion = models.CharField(max_length=50)

    def __str__(self):
        return f"Nutricionista: {self.user.username}"


class Bitacora(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha_hora}"

    class Meta:
        verbose_name = "BitÃ¡cora"
        verbose_name_plural = "BitÃ¡coras"
        ordering = ['-fecha_hora']



