from django.contrib import admin
from .models import CustomUser, Administrativo, Cliente, Instructor, Nutricionista, Bitacora

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_cliente', 'is_instructor', 'is_nutricionista', 'is_administrativo')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_cliente', 'is_instructor', 'is_nutricionista', 'is_administrativo')

@admin.register(Administrativo)
class AdministrativoAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo', 'turno')
    search_fields = ('user__username', 'cargo')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'domicilio', 'suscripcion_activa', 'fecha_ini_mem', 'fecha_fin_mem')
    search_fields = ('user__username', 'domicilio', 'suscripcion_activa')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'especialidad')
    search_fields = ('user__username', 'especialidad')

@admin.register(Nutricionista)
class NutricionistaAdmin(admin.ModelAdmin):
    list_display = ('user', 'horario_atencion')
    search_fields = ('user__username', 'horario_atencion')

@admin.register(Bitacora)
class BitacoraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha_hora', 'ip_address')
    list_filter = ('accion', 'fecha_hora')
    search_fields = ('usuario__username', 'accion', 'descripcion')
    readonly_fields = ('usuario', 'accion', 'descripcion', 'fecha_hora', 'ip_address')
