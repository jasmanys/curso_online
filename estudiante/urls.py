from django.urls import path, include
from estudiante.views import *
urlpatterns = [
    path('registros/', registros_estudiantes),
    path('nuevo/', registrar_estudiante),
]