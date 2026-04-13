"""
apps/citas/models.py – Mapea la tabla 'citas' existente en PostgreSQL.
"""
from django.db import models
from apps.ninos.models import Nino


class Cita(models.Model):
    STATUS_CHOICES = [
        ('pendiente',   'Pendiente'),
        ('confirmada',  'Confirmada'),
        ('completada',  'Completada'),
        ('cancelada',   'Cancelada'),
    ]
    TIPO_CHOICES = [
        ('CEMS',        'CEMS'),
        ('AI',          'AI'),
        ('OCUPACIONAL', 'Ocupacional'),
        ('BABY SPA',    'Baby Spa'),
        ('MUESTRA',     'Muestra'),
        ('REPOSICIÓN',  'Reposición'),
    ]

    nino               = models.ForeignKey(Nino, on_delete=models.PROTECT, db_column='nino_id', related_name='citas')
    tipo               = models.CharField(max_length=50, choices=TIPO_CHOICES, db_column='tipo')
    fecha              = models.DateField()
    hora_inicio        = models.TimeField(db_column='hora_inicio')
    duracion_min       = models.IntegerField(default=60)
    responsable        = models.CharField(max_length=200, null=True, blank=True)
    notas              = models.TextField(null=True, blank=True)
    status             = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    motivo_cancelacion = models.TextField(null=True, blank=True)
    creado_por         = models.IntegerField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'citas'
        managed  = False  # La tabla ya existe, Django no la toca
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f'{self.nino} – {self.fecha} {self.hora_inicio}'