from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Lower, Trim, Replace, Concat
from django.http import JsonResponse
from django.shortcuts import render, redirect

from curso.models import Curso, EstudianteCurso
from unidecode import unidecode

@login_required(login_url='/login/')
def index(request):
    data = {}
    user = request.user
    l2 = []
    if user.is_superuser:
        cursos  = Curso.objects.all().values()
        for i in range(len(cursos)):
            cursos[i]['nombre_link'] = 'editar/id'
        data['cursos'] = cursos
    else:
        lista = EstudianteCurso.objects.filter(estudiante__usuario__username=user.username).values_list('cursos__id')
        for l in lista:
            l2.append(l[0])
        data['cursos'] = Curso.objects.filter(id__in=l2).annotate(nombre_link=Concat(Value('abrir/'), Replace(Lower(Trim("nombre")), Value(' '), Value('')))).values()

    for i in range(len(data['cursos'])):
        data['cursos'][i]['nombre_link'] = unidecode(data['cursos'][i]['nombre_link'])
    data['user'] = user
    return render(request, 'home/home.html', data)

# Create your views here.
def login_user(request):
    data = {}
    if not request.user.id:
        if request.method == 'POST':
            usuario = request.POST['username']
            contrasena = request.POST['password']
            data['username'] = usuario
            data['password'] = contrasena
            if '@' in usuario:
                if User.objects.filter(email=usuario).exists():
                    us = ""
                    us = User.objects.get(email=usuario).username
                    user = authenticate(username=us, password=contrasena)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            data['user'] = user
                            return redirect('/')
                        else:
                            return redirect('/login/?error=no-active')
                    else:
                        return redirect('/login/?error=pass-error')
                else:
                    return redirect('/login/?error=email-error')
            else:
                if User.objects.filter(username=usuario).exists():
                    user = authenticate(username=usuario, password=contrasena)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            data['user'] = user
                            return redirect('/')
                        else:
                            return redirect('/login/?error=no-active')
                    else:
                        return redirect('/login/?error=pass-error')
                else:
                    return redirect('/login/?error=username-error')
        else:
            if 'error' in request.GET:
                data['error'] = request.GET['error']
            return render(request, 'login/login.html', data)
    else:
        return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')