from django.urls import path
from . import views

urlpatterns = [
    path('menu/',                    views.menu_view,        name='menu'),
    path('citas/',                   views.agenda_view,      name='agenda'),
    path('citas/agendar/',           views.agendar_cita_view, name='agendar_cita'),
    path('citas/editar/<int:pk>/',   views.editar_cita_view,  name='editar_cita'),
]
