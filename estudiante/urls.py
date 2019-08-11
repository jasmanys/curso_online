from django.urls import path, include, re_path
from estudiante.views import *
urlpatterns = [
    path('registros/', registros_estudiantes),
    path('nuevo/', registrar_estudiante),
    path('asignar_curso/', asignar_curso_estudiante),
    path('cursos_asignados/', registros_cursos_asignados),
    re_path(r'^cursos_asignados/editar/(?P<curso_asignado_id>[0-9]+)/$', editar_curso_asignado),
    re_path(r'^cursos_asignados/eliminar/(?P<curso_asignado_id>[0-9]+)/$', eliminar_curso_asignado),
    re_path(r'^usuario/nuevo/(?P<user_id>[0-9]+)/$', registrar_estudiante_usuario),
    re_path(r'^editar/(?P<estudiante_id>[0-9]+)/$', editar_estudiante),
    re_path(r'^eliminar/(?P<estudiante_id>[0-9]+)/$', eliminar_estudiante),
]