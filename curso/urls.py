from django.urls import path, re_path
from curso.views import *

urlpatterns = [
    #link's estudiante
    re_path(r'^abrir/(?P<curso_nombre>)/(?P<curso_id>[0-9]+)$', seleccionar_curso),
    #link's admin
    re_path(r'^editar/id/(?P<curso_id_ed>[0-9]+)$', editar_curso),
    re_path(r'^eliminar/id/(?P<curso_id_el>[0-9]+)/$', eliminar_curso),
    path('nuevo/', agregar_curso),
    path('modulo/nuevo/', seleccionar_curso),
    re_path(r'^submodulo/nuevo/(?P<modulo_id>[0-9]+)/$', agregar_submodulo),
    re_path(r'^modulo/nuevo/(?P<curso_id>[0-9]+)/$', agregar_modulo),
    re_path(r'^modulo/editar/(?P<modulo_id>[0-9]+)/$', editar_modulo),
    re_path(r'^modulo/eliminar/(?P<modulo_id>[0-9]+)/$', eliminar_modulo),
    re_path(r'^modulo/registros/(?P<curso_id>[0-9]+)/$', registro_modulos),
]