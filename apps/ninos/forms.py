"""
apps/ninos/forms.py — Formulario de registro de niño + tutor.
"""
from datetime import date
from django import forms


PARENTESCO_CHOICES = [
    ('', '— Selecciona —'),
    ('Madre', 'Madre'),
    ('Padre', 'Padre'),
    ('Abuelo/a', 'Abuelo/a'),
    ('Tío/a', 'Tío/a'),
    ('Otro', 'Otro'),
]

GENERO_CHOICES = [
    ('', '— Selecciona —'),
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
]

DIAGNOSTICO_CHOICES = [
    ('Neurotípico',     '🔵 Neurotípico'),
    ('Neurodivergente', '🟣 Neurodivergente'),
]


class RegistroNinoForm(forms.Form):
    # ── Datos del niño ────────────────────────────────────────────────────────
    nombre_nino      = forms.CharField(label='Nombre completo *', max_length=200)
    fecha_nacimiento = forms.DateField(
        label='Fecha de nacimiento *',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    genero           = forms.ChoiceField(label='Género *', choices=GENERO_CHOICES)
    diagnostico      = forms.ChoiceField(
        label='Diagnóstico *',
        choices=DIAGNOSTICO_CHOICES,
        widget=forms.RadioSelect,
    )
    observaciones    = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Alergias, condiciones médicas...'}),
    )

    # ── Datos del tutor ───────────────────────────────────────────────────────
    nombre_tutor = forms.CharField(label='Nombre completo del tutor *', max_length=200)
    telefono     = forms.CharField(label='Teléfono *', max_length=20)
    parentesco   = forms.ChoiceField(label='Parentesco *', choices=PARENTESCO_CHOICES)
    email        = forms.EmailField(label='Correo electrónico (opcional)', required=False)
    direccion    = forms.CharField(
        label='Dirección (opcional)',
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
    )

    def clean_genero(self):
        val = self.cleaned_data.get('genero')
        if not val:
            raise forms.ValidationError('Selecciona el género.')
        return val

    def clean_parentesco(self):
        val = self.cleaned_data.get('parentesco')
        if not val:
            raise forms.ValidationError('Selecciona el parentesco.')
        return val

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if fecha and fecha > date.today():
            raise forms.ValidationError('La fecha de nacimiento no puede ser futura.')
        return fecha
