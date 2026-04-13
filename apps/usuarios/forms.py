"""
apps/usuarios/forms.py — Formularios de Login y Registro.
"""
from django import forms


class LoginForm(forms.Form):
    usuario  = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario', 'autocomplete': 'username'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'autocomplete': 'current-password'}),
    )


class RegistroUsuarioForm(forms.Form):
    usuario   = forms.CharField(
        label='Usuario',
        min_length=4,
        widget=forms.TextInput(attrs={'placeholder': 'Mínimo 4 caracteres'}),
    )
    password  = forms.CharField(
        label='Contraseña',
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 6 caracteres'}),
    )
    confirmar = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite tu contraseña'}),
    )

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('password')
        cpw = cleaned.get('confirmar')
        if pw and cpw and pw != cpw:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned
