from django.conf.urls import url
from django.urls import path, re_path

from curso.views import seleccionar_curso

urlpatterns = [
    re_path(r'(?P<curso_nombre>)/(?P<curso_id>[0-9]+)', seleccionar_curso),
]