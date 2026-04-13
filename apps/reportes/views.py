"""
apps/reportes/views.py – Generación de PDF con fpdf2.
"""
from datetime import date
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import redirect

from apps.citas.models import Cita
from apps.ninos.models import Nino


def sesion_requerida(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def _build_pdf_citas(citas, titulo='Reporte de Citas'):
    try:
        from fpdf import FPDF
    except ImportError:
        raise ImportError('Instala fpdf2: pip install fpdf2')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_fill_color(13, 27, 62)
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_xy(10, 8)
    pdf.cell(0, 10, 'Centro Azul - Acuatica Inicial', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_xy(10, 20)
    pdf.cell(0, 8, titulo, ln=True)

    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_xy(10, 40)
    pdf.cell(0, 6, f'Generado el: {date.today().strftime("%d/%m/%Y")}', ln=True)
    pdf.ln(4)

    headers = ['Nino', 'Fecha', 'Hora', 'Tipo', 'Terapeuta', 'Estado']
    widths  = [50, 25, 20, 30, 40, 25]

    pdf.set_fill_color(13, 27, 62)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 9)
    for h, w in zip(headers, widths):
        pdf.cell(w, 8, h, border=1, fill=True)
    pdf.ln()

    pdf.set_text_color(30, 30, 30)
    pdf.set_font('Helvetica', '', 8)
    fill = False
    for cita in citas:
        pdf.set_fill_color(235, 242, 255) if fill else pdf.set_fill_color(255, 255, 255)
        row = [
            cita.nino.nombre_completo[:22],
            cita.fecha.strftime('%d/%m/%Y'),
            cita.hora.strftime('%H:%M'),
            cita.tipo_sesion.capitalize(),
            cita.terapeuta[:20],
            cita.estado.replace('_', ' ').capitalize(),
        ]
        for val, w in zip(row, widths):
            pdf.cell(w, 7, str(val), border=1, fill=True)
        pdf.ln()
        fill = not fill

    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(13, 27, 62)
    pdf.cell(0, 8, f'Total de citas: {len(citas)}', ln=True)

    buf = BytesIO()
    pdf.output(buf)
    return buf.getvalue()


@sesion_requerida
def reporte_citas_view(request):
    estado = request.GET.get('estado', '')
    fecha  = request.GET.get('fecha', '')

    citas = Cita.objects.select_related('nino').order_by('fecha', 'hora')
    if estado:
        citas = citas.filter(estado=estado)
    if fecha:
        citas = citas.filter(fecha=fecha)

    citas = list(citas)
    titulo = 'Reporte de Citas'
    if estado:
        titulo += f' - {estado.replace("_", " ").capitalize()}'

    try:
        pdf_bytes = _build_pdf_citas(citas, titulo)
    except ImportError as e:
        return HttpResponse(str(e), status=500)

    filename = f'reporte_citas_{date.today().isoformat()}.pdf'
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@sesion_requerida
def reporte_ninos_view(request):
    try:
        from fpdf import FPDF
    except ImportError:
        return HttpResponse('Instala fpdf2: pip install fpdf2', status=500)

    ninos = Nino.objects.filter(activo=1).select_related('tutor').order_by('nombre_completo')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_fill_color(13, 27, 62)
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_xy(10, 8)
    pdf.cell(0, 10, 'Centro Azul - Acuatica Inicial', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_xy(10, 20)
    pdf.cell(0, 8, 'Listado de Ninos Inscritos', ln=True)

    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_xy(10, 40)
    pdf.cell(0, 6, f'Generado el: {date.today().strftime("%d/%m/%Y")}', ln=True)
    pdf.ln(4)

    headers = ['Nombre', 'Edad', 'Genero', 'Diagnostico', 'Tutor', 'Telefono']
    widths  = [55, 15, 25, 30, 45, 30]

    pdf.set_fill_color(13, 27, 62)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 9)
    for h, w in zip(headers, widths):
        pdf.cell(w, 8, h, border=1, fill=True)
    pdf.ln()

    pdf.set_text_color(30, 30, 30)
    pdf.set_font('Helvetica', '', 8)
    fill = False
    for nino in ninos:
        pdf.set_fill_color(235, 242, 255) if fill else pdf.set_fill_color(255, 255, 255)
        row = [
            nino.nombre_completo[:25],
            str(nino.edad or '-'),
            nino.genero,
            nino.diagnostico,
            nino.tutor.nombre_completo[:22],
            nino.tutor.telefono,
        ]
        for val, w in zip(row, widths):
            pdf.cell(w, 7, str(val), border=1, fill=True)
        pdf.ln()
        fill = not fill

    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(13, 27, 62)
    pdf.cell(0, 8, f'Total de ninos activos: {ninos.count()}', ln=True)

    buf = BytesIO()
    pdf.output(buf)
    filename = f'reporte_ninos_{date.today().isoformat()}.pdf'
    response = HttpResponse(buf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response