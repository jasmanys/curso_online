from django.urls import path, re_path
from autenticacion.views import *

urlpatterns = [
    path('usuario/registros/', registros_usuario),
    re_path(r'^usuario/(?P<user_id>[0-9]+)/mi_cuenta/$', editar_cuenta),
    re_path(r'^usuario/editar/(?P<user_id>[0-9]+)/$', editar_cuenta),
]