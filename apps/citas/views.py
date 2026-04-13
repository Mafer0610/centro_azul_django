"""
apps/citas/views.py – Vistas para agenda de citas.
"""
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cita
from .forms import AgendarCitaForm, EditarEstadoCitaForm


def sesion_requerida(view_func):
    """Equivalente a @login_required pero usando nuestra sesión propia."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@sesion_requerida
def menu_view(request):
    hoy        = date.today()
    citas_hoy  = Cita.objects.filter(fecha=hoy, status='pendiente').count()
    total_prog = Cita.objects.filter(status='pendiente').count()
    from apps.ninos.models import Nino
    total_ninos = Nino.objects.filter(activo=1).count()
    return render(request, 'base/menu.html', {
        'citas_hoy':   citas_hoy,
        'total_prog':  total_prog,
        'total_ninos': total_ninos,
    })


@sesion_requerida
def agenda_view(request):
    hoy   = date.today()
    citas = (
        Cita.objects
        .select_related('nino', 'nino__tutor')
        .filter(fecha__gte=hoy)
        .order_by('fecha', 'hora_inicio')
    )
    fecha_filtro = request.GET.get('fecha')
    if fecha_filtro:
        citas = citas.filter(fecha=fecha_filtro)
    return render(request, 'citas/agenda.html', {
        'citas':        citas,
        'fecha_filtro': fecha_filtro,
        'hoy':          hoy.isoformat(),
    })


@sesion_requerida
def agendar_cita_view(request):
    form = AgendarCitaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        d = form.cleaned_data
        try:
            Cita.objects.create(
                nino=d['nino'],
                fecha=d['fecha'],
                hora=d['hora'],
                tipo_sesion=d['tipo_sesion'],
                terapeuta=d['terapeuta'],
                observaciones=d['observaciones'] or None,
            )
            messages.success(request, '✅ Cita agendada correctamente.')
            return redirect('agenda')
        except Exception as e:
            messages.error(request, f'Error al agendar: {e}')
    return render(request, 'citas/agendar.html', {'form': form})


@sesion_requerida
def editar_cita_view(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    form = EditarEstadoCitaForm(
        request.POST or None,
        initial={'estado': cita.estado, 'observaciones': cita.observaciones},
    )
    if request.method == 'POST' and form.is_valid():
        cita.estado        = form.cleaned_data['estado']
        cita.observaciones = form.cleaned_data['observaciones'] or None
        cita.save()
        messages.success(request, '✅ Cita actualizada.')
        return redirect('agenda')
    return render(request, 'citas/editar.html', {'form': form, 'cita': cita})