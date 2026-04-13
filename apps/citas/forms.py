"""
apps/citas/forms.py — Formularios de agenda y gestión de citas.
"""
from django import forms
from apps.ninos.models import Nino


TIPO_CHOICES = [
    ('', '— Selecciona —'),
    ('evaluacion',  'Evaluación'),
    ('terapia',     'Terapia'),
    ('seguimiento', 'Seguimiento'),
    ('otro',        'Otro'),
]

ESTADO_CHOICES = [
    ('programada',  'Programada'),
    ('completada',  'Completada'),
    ('cancelada',   'Cancelada'),
    ('no_asistio',  'No asistió'),
]


class AgendarCitaForm(forms.Form):
    nino        = forms.ModelChoiceField(
        queryset=Nino.objects.filter(activo=1).order_by('nombre_completo'),
        label='Niño *',
        empty_label='— Selecciona un niño —',
    )
    fecha       = forms.DateField(
        label='Fecha *',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    hora        = forms.TimeField(
        label='Hora *',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )
    tipo_sesion = forms.ChoiceField(label='Tipo de sesión *', choices=TIPO_CHOICES)
    terapeuta   = forms.CharField(label='Terapeuta *', max_length=150)
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Notas adicionales...'}),
    )

    def clean_tipo_sesion(self):
        val = self.cleaned_data.get('tipo_sesion')
        if not val:
            raise forms.ValidationError('Selecciona el tipo de sesión.')
        return val


class EditarEstadoCitaForm(forms.Form):
    estado        = forms.ChoiceField(label='Estado', choices=ESTADO_CHOICES)
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )
