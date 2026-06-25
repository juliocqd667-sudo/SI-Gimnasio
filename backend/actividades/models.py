from django.db import models
from core.models import Cliente, Instructor, Nutricionista
from finanzas.models import Comprobante

class Rutina(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class DetalleRutina(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    dia = models.CharField(max_length=9)
    repeticiones = models.CharField(max_length=2)
    serie = models.CharField(max_length=2)
    peso = models.CharField(max_length=5)

class Sala(models.Model):
    descripcion = models.CharField(max_length=100)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.descripcion

class Disciplina(models.Model):
    nombre = models.CharField(max_length=20)
    grupo = models.IntegerField()
    cupo = models.IntegerField()
    hora_inicial = models.TextField() # keeping text as in original or TimeField
    hora_final = models.TextField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Horario(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    dia = models.CharField(max_length=9)
    hora_inicial = models.TimeField()
    hora_final = models.TimeField()

class Reserva(models.Model):
    fecha = models.DateField()
    estado = models.CharField(max_length=1)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE)

class Seguimiento(models.Model):
    fecha = models.DateField()
    observaciones = models.TextField()
    objetivo = models.TextField()
    fecha_prox_consulta = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)

class Antecedentes(models.Model):
    fecha = models.DateField()
    diagnostico = models.TextField()
    recomendaciones = models.TextField()
    objetivo = models.TextField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    imc = models.DecimalField(max_digits=5, decimal_places=2)
    gc = models.DecimalField(max_digits=5, decimal_places=2)
    mm = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_prox_consulta = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE)

