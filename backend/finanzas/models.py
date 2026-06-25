from django.db import models
from core.models import Cliente, Administrativo

class Promocion(models.Model):
    nombre = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=1)
    fecha_ini = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Suscripcion(models.Model):
    membresia = models.CharField(max_length=20)
    plan = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=40)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.membresia} - {self.plan}"

class Pago(models.Model):
    metodo_pago = models.CharField(max_length=1)
    fecha = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    administrador = models.ForeignKey(Administrativo, on_delete=models.SET_NULL, null=True)
    suscripcion = models.ForeignKey(Suscripcion, on_delete=models.CASCADE)
    promocion = models.ForeignKey(Promocion, on_delete=models.SET_NULL, null=True, blank=True)
    estado_pago = models.CharField(max_length=10)

    def __str__(self):
        return f"Pago {self.id} - Cliente: {self.cliente.user.username}"

class Comprobante(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ini_mem = models.DateField()
    fecha_fin_mem = models.DateField()
    pago = models.OneToOneField(Pago, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comprobante {self.id} - {self.cliente.user.username}"

