from django.contrib import admin
from .models import Rutina, Ejercicio, DetalleRutina, Sala, Disciplina, Horario, Reserva, Seguimiento, Antecedentes

@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(DetalleRutina)
class DetalleRutinaAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'ejercicio', 'dia', 'repeticiones', 'serie', 'peso')
    list_filter = ('dia', 'rutina')

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'capacidad')

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grupo', 'cupo', 'sala', 'hora_inicial', 'hora_final')
    list_filter = ('sala',)

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'dia', 'hora_inicial', 'hora_final')
    list_filter = ('dia', 'disciplina')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'disciplina', 'fecha', 'estado')
    list_filter = ('fecha', 'disciplina', 'estado')

@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'instructor', 'fecha', 'objetivo')
    list_filter = ('fecha', 'instructor', 'cliente')

@admin.register(Antecedentes)
class AntecedentesAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'nutricionista', 'fecha', 'peso', 'imc')
    list_filter = ('fecha', 'nutricionista', 'cliente')
