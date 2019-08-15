from django.urls import path, re_path
from evaluacion.views import *

urlpatterns = [
    path('', seleccionar_curso_para_add_evaluacion),
    re_path(r'^modulos/(?P<curso_id>[0-9]+)/$', registro_modulos_para_add_evaluacion),
    re_path(r'^listar/submodulo/(?P<modulo_id>[0-9]+)/$', registro_evaluacion),
    re_path(r'^eliminar/(?P<modulo_id>[0-9]+)/$', eliminar_evaluacion),
    re_path(r'^agregar/enunciado/(?P<submodulo_id>[0-9]+)/$', registro_enunciado),
    re_path(r'^editar/enunciado/(?P<enunciado_id>[0-9]+)/$', editar_enunciado),
    re_path(r'^eliminar/enunciado/(?P<enunciado_id>[0-9]+)/$', eliminar_enunciado),
    re_path(r'^registros/enunciado/(?P<submodulo_id>[0-9]+)/$', registros_enunciado),
]