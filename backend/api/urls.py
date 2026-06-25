from django.urls import path, include, re_path
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
    re_path(r'^reportes/usuarios/excel/+$', views.ReporteUsuariosExcelView.as_view(), name='reporte-usuarios-excel'),
    re_path(r'^reportes/usuarios/pdf/+$', views.ReporteUsuariosPDFView.as_view(), name='reporte-usuarios-pdf'),
    re_path(r'^reportes/pagos/excel/+$', views.ReportePagosExcelView.as_view(), name='reporte-pagos-excel'),
    re_path(r'^reportes/pagos/pdf/+$', views.ReportePagosPDFView.as_view(), name='reporte-pagos-pdf'),
    re_path(r'^reportes/suscripciones/excel/+$', views.ReporteSuscripcionesExcelView.as_view(), name='reporte-suscripciones-excel'),
    re_path(r'^reportes/suscripciones/pdf/+$', views.ReporteSuscripcionesPDFView.as_view(), name='reporte-suscripciones-pdf'),
    re_path(r'^reportes/promociones/excel/+$', views.ReportePromocionesExcelView.as_view(), name='reporte-promociones-excel'),
    re_path(r'^reportes/promociones/pdf/+$', views.ReportePromocionesPDFView.as_view(), name='reporte-promociones-pdf'),
    re_path(r'^reportes/rutinas/excel/+$', views.ReporteRutinasExcelView.as_view(), name='reporte-rutinas-excel'),
    re_path(r'^reportes/rutinas/pdf/+$', views.ReporteRutinasPDFView.as_view(), name='reporte-rutinas-pdf'),
    re_path(r'^reportes/horarios/excel/+$', views.ReporteHorariosExcelView.as_view(), name='reporte-horarios-excel'),
    re_path(r'^reportes/horarios/pdf/+$', views.ReporteHorariosPDFView.as_view(), name='reporte-horarios-pdf'),
    re_path(r'^reportes/antecedentes/excel/+$', views.ReporteAntecedentesExcelView.as_view(), name='reporte-antecedentes-excel'),
    re_path(r'^reportes/antecedentes/pdf/+$', views.ReporteAntecedentesPDFView.as_view(), name='reporte-antecedentes-pdf'),
    re_path(r'^reportes/seguimientos/excel/+$', views.ReporteSeguimientosExcelView.as_view(), name='reporte-seguimientos-excel'),
    re_path(r'^reportes/seguimientos/pdf/+$', views.ReporteSeguimientosPDFView.as_view(), name='reporte-seguimientos-pdf'),
    re_path(r'^reportes/reservas/excel/+$', views.ReporteReservasExcelView.as_view(), name='reporte-reservas-excel'),
    re_path(r'^reportes/reservas/pdf/+$', views.ReporteReservasPDFView.as_view(), name='reporte-reservas-pdf'),
    re_path(r'^reportes/disciplinas/excel/+$', views.ReporteDisciplinasExcelView.as_view(), name='reporte-disciplinas-excel'),
    re_path(r'^reportes/disciplinas/pdf/+$', views.ReporteDisciplinasPDFView.as_view(), name='reporte-disciplinas-pdf'),
    re_path(r'^reportes/salas/excel/+$', views.ReporteSalasExcelView.as_view(), name='reporte-salas-excel'),
    re_path(r'^reportes/salas/pdf/+$', views.ReporteSalasPDFView.as_view(), name='reporte-salas-pdf'),
    re_path(r'^reportes/ejercicios/excel/+$', views.ReporteEjerciciosExcelView.as_view(), name='reporte-ejercicios-excel'),
    re_path(r'^reportes/ejercicios/pdf/+$', views.ReporteEjerciciosPDFView.as_view(), name='reporte-ejercicios-pdf'),
    path('', include(router.urls)),
]
