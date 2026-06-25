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
    path('reportes/pagos/excel/', views.ReportePagosExcelView.as_view(), name='reporte-pagos-excel'),
    path('reportes/pagos/pdf/', views.ReportePagosPDFView.as_view(), name='reporte-pagos-pdf'),
    path('reportes/suscripciones/excel/', views.ReporteSuscripcionesExcelView.as_view(), name='reporte-suscripciones-excel'),
    path('reportes/suscripciones/pdf/', views.ReporteSuscripcionesPDFView.as_view(), name='reporte-suscripciones-pdf'),
    path('reportes/promociones/excel/', views.ReportePromocionesExcelView.as_view(), name='reporte-promociones-excel'),
    path('reportes/promociones/pdf/', views.ReportePromocionesPDFView.as_view(), name='reporte-promociones-pdf'),
    path('reportes/rutinas/excel/', views.ReporteRutinasExcelView.as_view(), name='reporte-rutinas-excel'),
    path('reportes/rutinas/pdf/', views.ReporteRutinasPDFView.as_view(), name='reporte-rutinas-pdf'),
    path('reportes/horarios/excel/', views.ReporteHorariosExcelView.as_view(), name='reporte-horarios-excel'),
    path('reportes/horarios/pdf/', views.ReporteHorariosPDFView.as_view(), name='reporte-horarios-pdf'),
    path('reportes/antecedentes/excel/', views.ReporteAntecedentesExcelView.as_view(), name='reporte-antecedentes-excel'),
    path('reportes/antecedentes/pdf/', views.ReporteAntecedentesPDFView.as_view(), name='reporte-antecedentes-pdf'),
    path('reportes/seguimientos/excel/', views.ReporteSeguimientosExcelView.as_view(), name='reporte-seguimientos-excel'),
    path('reportes/seguimientos/pdf/', views.ReporteSeguimientosPDFView.as_view(), name='reporte-seguimientos-pdf'),
    path('reportes/reservas/excel/', views.ReporteReservasExcelView.as_view(), name='reporte-reservas-excel'),
    path('reportes/reservas/pdf/', views.ReporteReservasPDFView.as_view(), name='reporte-reservas-pdf'),
    path('reportes/disciplinas/excel/', views.ReporteDisciplinasExcelView.as_view(), name='reporte-disciplinas-excel'),
    path('reportes/disciplinas/pdf/', views.ReporteDisciplinasPDFView.as_view(), name='reporte-disciplinas-pdf'),
    path('reportes/salas/excel/', views.ReporteSalasExcelView.as_view(), name='reporte-salas-excel'),
    path('reportes/salas/pdf/', views.ReporteSalasPDFView.as_view(), name='reporte-salas-pdf'),
    path('reportes/ejercicios/excel/', views.ReporteEjerciciosExcelView.as_view(), name='reporte-ejercicios-excel'),
    path('reportes/ejercicios/pdf/', views.ReporteEjerciciosPDFView.as_view(), name='reporte-ejercicios-pdf'),
    path('', include(router.urls)),
]
