from django.urls import path, include, re_path
from estudiante.views import *
urlpatterns = [
    path('registros/', registros_estudiantes),
    path('nuevo/', registrar_estudiante),
    re_path(r'^editar/(?P<estudiante_id>[0-9]+)/$', editar_estudiante),
    re_path(r'^eliminar/(?P<estudiante_id>[0-9]+)/$', eliminar_estudiante),
]