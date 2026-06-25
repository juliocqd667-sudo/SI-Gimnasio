from django.contrib import admin
from .models import Promocion, Suscripcion, Pago, Comprobante

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'valor', 'estado', 'fecha_ini', 'fecha_fin')
    search_fields = ('nombre',)
    list_filter = ('tipo', 'estado')

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ('membresia', 'plan', 'precio')
    search_fields = ('membresia', 'plan')
    list_filter = ('membresia', 'plan')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'monto_total', 'fecha', 'metodo_pago', 'estado_pago')
    search_fields = ('cliente__user__username', 'id')
    list_filter = ('metodo_pago', 'estado_pago', 'fecha')

@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'pago', 'cliente', 'monto', 'fecha_ini_mem', 'fecha_fin_mem')
    search_fields = ('cliente__user__username', 'id', 'pago__id')
