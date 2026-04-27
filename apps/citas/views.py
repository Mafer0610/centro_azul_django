"""
apps/citas/views.py
"""
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cita
from .forms import AgendarCitaForm, EditarEstadoCitaForm


def sesion_requerida(view_func):
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
    # Traemos TODAS las citas para pintar el calendario completo
    citas = (
        Cita.objects
        .select_related('nino')
        .order_by('fecha', 'hora_inicio')
    )
    return render(request, 'citas/agenda.html', {'citas': citas})


@sesion_requerida
def agendar_cita_view(request):
    form = AgendarCitaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        d = form.cleaned_data
        try:
            Cita.objects.create(
                nino=d['nino'],
                fecha=d['fecha'],
                hora_inicio=d['hora'],
                tipo=d['tipo_sesion'],
                responsable=d['terapeuta'],
                notas=d['observaciones'] or None,
                duracion_min=60,
                status='pendiente',
            )
            messages.success(request, 'Cita agendada correctamente.')
            return redirect('agenda')
        except Exception as e:
            messages.error(request, f'Error al agendar: {e}')
    return render(request, 'citas/agendar.html', {'form': form})


@sesion_requerida
def editar_cita_view(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    form = EditarEstadoCitaForm(
        request.POST or None,
        initial={'estado': cita.status, 'observaciones': cita.notas},
    )
    if request.method == 'POST' and form.is_valid():
        cita.status = form.cleaned_data['estado']
        cita.notas  = form.cleaned_data['observaciones'] or None
        cita.save()
        messages.success(request, 'Cita actualizada.')
        return redirect('agenda')
    return render(request, 'citas/editar.html', {'form': form, 'cita': cita})