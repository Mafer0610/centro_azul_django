from django.urls import path
from . import views

urlpatterns = [
    path('ninos/',           views.lista_ninos_view,   name='lista_ninos'),
    path('ninos/registro/',  views.registro_nino_view, name='registro_nino'),
]
