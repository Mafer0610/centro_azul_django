from django.urls import path
from . import views

urlpatterns = [
    path('reportes/citas/',  views.reporte_citas_view,  name='reporte_citas'),
    path('reportes/ninos/',  views.reporte_ninos_view,  name='reporte_ninos'),
]
