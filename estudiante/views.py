from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from estudiante.models import Estudiante


@login_required(login_url='/login/')
def registros_estudiantes(request):
    data = {}
    data['user'] = request.user
    data['estudiantes'] = Estudiante.objects.all()
    return render(request, 'estudiante/listar_estudiante.html', data)

@login_required(login_url='/login/')
def registrar_estudiante(request):
    data = {}
    data['title'] = 'Registrar Estudiante'
    data['usuarios'] = User.objects.filter(is_active=True, is_superuser=False).all()
    data['user'] = request.user
    if request.method == 'POST':
        pass
    return render(request, 'estudiante/form_estudiante.html', data)