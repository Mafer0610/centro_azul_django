"""
apps/usuarios/models.py — Modelo (M en MTV).
Mapea la tabla 'usuarios' existente en PostgreSQL.
Usa bcrypt igual que la app Streamlit original.
"""
import bcrypt
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):

    def create_user(self, usuario, password=None):
        if not usuario:
            raise ValueError('El usuario es obligatorio.')
        user = self.model(usuario=usuario)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password=None):
        return self.create_user(usuario, password)


class Usuario(AbstractBaseUser):
    """
    Modelo personalizado que mapea directamente la tabla 'usuarios'
    ya existente en PostgreSQL (misma estructura que usaba PHP/Streamlit).
    """
    usuario        = models.CharField(max_length=100, unique=True)
    password       = models.CharField(max_length=255, db_column='password')
    fecha_creacion = models.DateTimeField(null=True, blank=True)

    # Sin campos extras de Django (is_staff, etc.)
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD  = 'usuario'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'usuarios'  # ← misma tabla de la BD existente

    def __str__(self):
        return self.usuario

    # ── Bcrypt personalizado (igual que Streamlit) ────────────────────────────
    def set_password(self, raw_password):
        """Hashea con bcrypt, igual que bcrypt.hashpw() en el código original."""
        hashed = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt(rounds=12))
        self.password = hashed.decode()

    def check_password(self, raw_password):
        """Verifica con bcrypt, igual que bcrypt.checkpw() en el código original."""
        try:
            return bcrypt.checkpw(raw_password.encode(), self.password.encode())
        except Exception:
            return False

    # Requeridos por Django admin (stubs mínimos)
    def has_perm(self, perm, obj=None): return self.is_staff
    def has_module_perms(self, app_label): return self.is_staff
