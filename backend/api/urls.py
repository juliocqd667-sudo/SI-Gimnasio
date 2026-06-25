from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# Core
router.register(r'users', views.CustomUserViewSet)
router.register(r'clientes', views.ClienteViewSet)
router.register(r'instructores', views.InstructorViewSet)
router.register(r'nutricionistas', views.NutricionistaViewSet)
router.register(r'administrativos', views.AdministrativoViewSet)

# Finanzas
router.register(r'promociones', views.PromocionViewSet)
router.register(r'suscripciones', views.SuscripcionViewSet)
router.register(r'pagos', views.PagoViewSet)
router.register(r'comprobantes', views.ComprobanteViewSet)

# Actividades
router.register(r'rutinas', views.RutinaViewSet)
router.register(r'ejercicios', views.EjercicioViewSet)
router.register(r'detalles-rutina', views.DetalleRutinaViewSet)
router.register(r'salas', views.SalaViewSet)
router.register(r'disciplinas', views.DisciplinaViewSet)
router.register(r'horarios', views.HorarioViewSet)
router.register(r'reservas', views.ReservaViewSet)
router.register(r'seguimientos', views.SeguimientoViewSet)
router.register(r'antecedentes', views.AntecedentesViewSet)

urlpatterns = [
    path('users/me/', views.CurrentUserView.as_view(), name='current_user'),
    path('reportes/usuarios/excel/', views.ReporteUsuariosExcelView.as_view(), name='reporte-usuarios-excel'),
    path('reportes/usuarios/pdf/', views.ReporteUsuariosPDFView.as_view(), name='reporte-usuarios-pdf'),
    path('', include(router.urls)),
]
