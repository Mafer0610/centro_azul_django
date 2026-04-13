"""
apps/usuarios/views.py – Vistas de autenticación.
"""
import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_http_methods

from .models import Usuario
from .forms import LoginForm, RegistroUsuarioForm


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.session.get('usuario_id'):
        return redirect('menu')

    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario_input = form.cleaned_data['usuario']
            password_input = form.cleaned_data['password']
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, usuario, password FROM usuarios WHERE usuario = %s",
                        [usuario_input]
                    )
                    row = cursor.fetchone()

                if row is None:
                    error = 'Usuario no encontrado. Verifique sus credenciales.'
                else:
                    uid, uname, uhash = row
                    if bcrypt.checkpw(password_input.encode(), uhash.encode()):
                        request.session['usuario_id'] = uid
                        request.session['usuario'] = uname
                        return redirect('menu')
                    else:
                        error = 'Contraseña incorrecta. Por favor, intente nuevamente.'
            except Exception as e:
                error = f'Error en el sistema: {e}'
        else:
            error = 'Por favor, complete todos los campos.'
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form, 'error': error})


@require_http_methods(['GET', 'POST'])
def registro_view(request):
    form = RegistroUsuarioForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        usuario_str = form.cleaned_data['usuario']
        password    = form.cleaned_data['password']

        if Usuario.objects.filter(usuario=usuario_str).exists():
            messages.error(request, f'El usuario "{usuario_str}" ya existe. Elige otro nombre.')
        else:
            user = Usuario(usuario=usuario_str)
            user.set_password(password)
            from django.utils import timezone
            user.fecha_creacion = timezone.now()
            user.save()
            messages.success(request, '¡Usuario registrado exitosamente! Ya puedes iniciar sesión.')
            return redirect('login')

    return render(request, 'usuarios/registro.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('login')