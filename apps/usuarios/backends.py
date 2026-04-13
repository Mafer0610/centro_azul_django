"""
apps/usuarios/backends.py — Backend de autenticación con bcrypt.
Necesario para que auth_login() funcione con nuestro modelo personalizado.
"""
from .models import Usuario


class BcryptBackend:

    def authenticate(self, request, usuario=None, password=None):
        try:
            user = Usuario.objects.get(usuario=usuario)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
