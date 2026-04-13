"""
apps/citas/views.py — Vistas (T en MTV) para agenda de citas.
"""
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cita
from .forms import AgendarCitaForm, EditarEstadoCitaForm


@login_required
def menu_view(request):
    """Menú principal — equivalente a vista/menu_view.py"""
    hoy        = date.today()
    citas_hoy  = Cita.objects.filter(fecha=hoy, estado='programada').count()
    total_prog = Cita.objects.filter(estado='programada').count()

    from apps.ninos.models import Nino
    total_ninos = Nino.objects.filter(activo=1).count()

    return render(request, 'base/menu.html', {
        'citas_hoy':   citas_hoy,
        'total_prog':  total_prog,
        'total_ninos': total_ninos,
    })


@login_required
def agenda_view(request):
    """Lista de citas — equivalente a vista/agenda_view.py"""
    hoy   = date.today()
    citas = (
        Cita.objects
        .select_related('nino', 'nino__tutor')
        .filter(fecha__gte=hoy)
        .order_by('fecha', 'hora')
    )

    # Filtro por fecha opcional
    fecha_filtro = request.GET.get('fecha')
    if fecha_filtro:
        citas = citas.filter(fecha=fecha_filtro)

    return render(request, 'citas/agenda.html', {
        'citas':        citas,
        'fecha_filtro': fecha_filtro,
        'hoy':          hoy.isoformat(),
    })


@login_required
def agendar_cita_view(request):
    """Nueva cita — equivalente a vista/agendar_cita_view.py"""
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


@login_required
def editar_cita_view(request, pk):
    """Editar estado de una cita existente."""
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
