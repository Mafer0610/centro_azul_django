"""
apps/ninos/views.py — Vistas (T en MTV) para niños.
"""
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import Nino, Tutor
from .forms import RegistroNinoForm


@login_required
def lista_ninos_view(request):
    """Equivalente a vista/lista_ninos_view.py render()"""
    ninos = (
        Nino.objects
        .filter(activo=1)
        .select_related('tutor')
        .order_by('nombre_completo')
    )

    # Estadísticas
    total  = ninos.count()
    neurot = ninos.filter(diagnostico='Neurotípico').count()
    neurod = total - neurot
    masc   = ninos.filter(genero='Masculino').count()
    fem    = total - masc

    stats = {
        'total': total,
        'neurotipicos': neurot,
        'neurodivergentes': neurod,
        'masculino': masc,
        'femenino': fem,
    }

    return render(request, 'ninos/lista.html', {
        'ninos': ninos,
        'stats': stats,
    })


@login_required
def registro_nino_view(request):
    """Equivalente a vista/registro_nino_view.py render()"""
    form = RegistroNinoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        d = form.cleaned_data
        today = date.today()
        fn = d['fecha_nacimiento']
        edad = today.year - fn.year - ((today.month, today.day) < (fn.month, fn.day))

        try:
            with transaction.atomic():
                tutor = Tutor.objects.create(
                    nombre_completo=d['nombre_tutor'],
                    telefono=d['telefono'],
                    email=d['email'] or None,
                    direccion=d['direccion'] or None,
                    parentesco=d['parentesco'],
                )
                Nino.objects.create(
                    nombre_completo=d['nombre_nino'],
                    fecha_nacimiento=fn,
                    edad=edad,
                    genero=d['genero'],
                    tutor=tutor,
                    diagnostico=d['diagnostico'],
                    observaciones=d['observaciones'] or None,
                )
            messages.success(request, '¡Niño registrado exitosamente!')
            return redirect('lista_ninos')
        except Exception as e:
            messages.error(request, f'Error al registrar: {e}')

    return render(request, 'ninos/registro.html', {'form': form})
