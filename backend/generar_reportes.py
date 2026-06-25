# generar_reportes.py — Script auxiliar para generar reportes desde shell de Django

from api.views import (
    ReporteUsuariosExcelView, ReporteUsuariosPDFView,
    ReportePagosExcelView, ReportePagosPDFView,
    ReporteSuscripcionesExcelView, ReporteSuscripcionesPDFView,
    ReportePromocionesExcelView, ReportePromocionesPDFView,
    ReporteRutinasExcelView, ReporteRutinasPDFView,
    ReporteHorariosExcelView, ReporteHorariosPDFView,
    ReporteAntecedentesExcelView, ReporteAntecedentesPDFView,
)
import io

reportes = {
    'usuarios_excel': ReporteUsuariosExcelView(),
    'usuarios_pdf': ReporteUsuariosPDFView(),
    'pagos_excel': ReportePagosExcelView(),
    'pagos_pdf': ReportePagosPDFView(),
    'suscripciones_excel': ReporteSuscripcionesExcelView(),
    'suscripciones_pdf': ReporteSuscripcionesPDFView(),
    'promociones_excel': ReportePromocionesExcelView(),
    'promociones_pdf': ReportePromocionesPDFView(),
    'rutinas_excel': ReporteRutinasExcelView(),
    'rutinas_pdf': ReporteRutinasPDFView(),
    'horarios_excel': ReporteHorariosExcelView(),
    'horarios_pdf': ReporteHorariosPDFView(),
    'antecedentes_excel': ReporteAntecedentesExcelView(),
    'antecedentes_pdf': ReporteAntecedentesPDFView(),
}

tipo = input("Ingrese tipo de reporte (ej: pagos_pdf, usuarios_excel): ").strip()
if tipo in reportes:
    view = reportes[tipo]
    response = view.get(None)
    ext = 'xlsx' if 'excel' in tipo else 'pdf'
    filename = f"{tipo.replace('_' + ext, '')}.{ext}"
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Reporte guardado: {filename}")
else:
    print("Tipo no válido. Opciones:")
    for k in reportes:
        print(" -", k)
