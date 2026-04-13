"""
apps/citas/models.py — Modelo (M en MTV) que mapea la tabla 'citas' existente.
"""
from django.db import models
from apps.ninos.models import Nino


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('programada',  'Programada'),
        ('completada',  'Completada'),
        ('cancelada',   'Cancelada'),
        ('no_asistio',  'No asistió'),
    ]
    TIPO_CHOICES = [
        ('evaluacion',  'Evaluación'),
        ('terapia',     'Terapia'),
        ('seguimiento', 'Seguimiento'),
        ('otro',        'Otro'),
    ]

    nino            = models.ForeignKey(Nino, on_delete=models.PROTECT, db_column='nino_id', related_name='citas')
    fecha           = models.DateField()
    hora            = models.TimeField()
    tipo_sesion     = models.CharField(max_length=50, choices=TIPO_CHOICES)
    terapeuta       = models.CharField(max_length=150)
    estado          = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='programada')
    observaciones   = models.TextField(null=True, blank=True)
    fecha_registro  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'citas'          # ← tabla existente
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f'{self.nino} — {self.fecha} {self.hora}'
