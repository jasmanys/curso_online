"""curso_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from autenticacion.views import index
from curso_online import settings
from django.views.generic import RedirectView
from login.views import *
from django.views.static import serve
from autenticacion.views import login_user, logout_user, forget_password
admin.site.site_header = "Administracion de Cursos"
favicon_view = RedirectView.as_view(url='/static/media/logo.ico', permanent=True)
urlpatterns = [
    #url favicon
    url(r'^favicon\.ico$', favicon_view),
    path(r'', index),
    path(r'admin/', admin.site.urls),
    path(r'autenticacion/', include(('autenticacion.urls', 'autenticacion'))),
    path(r'estudiante/', include(('estudiante.urls', 'estudiante'))),
    path(r'curso/', include('curso.urls')),
    path(r'evaluacion/', include('evaluacion.urls')),
    path(r'login/', login_user, name = 'login'),
    path(r'logout/', logout_user, name = 'logout'),
    path(r'forget/password/1C1CHBF_esEC825EC82569i57j0l51359j0j7/', forget_password, name = 'forget_password'),
    url(r'ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)