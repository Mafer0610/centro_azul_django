"""
apps/ninos/models.py — Modelos (M en MTV) que mapean las tablas
'tutores' y 'ninos' ya existentes en PostgreSQL.
"""
from django.db import models


class Tutor(models.Model):
    nombre_completo = models.CharField(max_length=200)
    telefono        = models.CharField(max_length=20)
    email           = models.CharField(max_length=150, null=True, blank=True)
    direccion       = models.TextField(null=True, blank=True)
    parentesco      = models.CharField(max_length=50)
    fecha_registro  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tutores'  # ← tabla existente

    def __str__(self):
        return self.nombre_completo


class Nino(models.Model):
    GENERO_CHOICES = [('Masculino', 'Masculino'), ('Femenino', 'Femenino')]
    DIAGNOSTICO_CHOICES = [
        ('Neurotípico',    'Neurotípico'),
        ('Neurodivergente','Neurodivergente'),
    ]

    nombre_completo   = models.CharField(max_length=200)
    fecha_nacimiento  = models.DateField()
    edad              = models.IntegerField(null=True, blank=True)
    genero            = models.CharField(max_length=20, choices=GENERO_CHOICES)
    tutor             = models.ForeignKey(Tutor, on_delete=models.PROTECT, db_column='tutor_id')
    diagnostico       = models.CharField(max_length=30, choices=DIAGNOSTICO_CHOICES)
    observaciones     = models.TextField(null=True, blank=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    activo            = models.SmallIntegerField(default=1)

    class Meta:
        db_table = 'ninos'  # ← tabla existente

    def __str__(self):
        return self.nombre_completo
