from django.urls import path, re_path
from curso.views import *

urlpatterns = [
    re_path(r'abrir/(?P<curso_nombre>)/(?P<curso_id>[0-9]+)', seleccionar_curso),
    re_path(r'editar/id/(?P<curso_id_ed>[0-9]+)', editar_curso),
    re_path(r'eliminar/id/(?P<curso_id_el>[0-9]+)/', eliminar_curso),
    path('nuevo/', agregar_curso),
    path('modulo/nuevo/', seleccionar_curso),
    re_path('modulo/nuevo/(?P<curso_id>[0-9]+)/', agregar_modulo),
    re_path('modulo/editar/(?P<modulo_id>[0-9]+)/', editar_modulo),
    re_path('modulo/eliminar/(?P<modulo_id>[0-9]+)/', eliminar_modulo),
    re_path('modulo/registros/(?P<curso_id>[0-9]+)/', registro_modulos),
]