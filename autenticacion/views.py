from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction, DatabaseError
from django.db.models import Value
from django.db.models.functions import Lower, Trim, Replace, Concat
#from django.http import JsonResponse
from django.shortcuts import render, redirect

from autenticacion.forms import UserForm
from curso.models import Curso, EstudianteCurso, SubModulo
from unidecode import unidecode

@login_required(login_url='/login/')
def registros_usuario(request):
    data = {}
    data['user'] = request.user
    data['usuarios'] = User.objects.all()
    return render(request, 'usuario/listar_usuario.html', data)

@login_required(login_url='/login/')
def editar_cuenta(request, user_id):
    data = {}
    data['user'] = request.user
    data['usuario'] = User.objects.get(id=user_id)
    data['form'] = UserForm(instance=data['usuario'])
    if str(request.user.id) == str(user_id):
        data['title'] = 'Mi Cuenta'
    else:
        data['title'] = 'Editar Cuenta'
    if request.method == 'POST':
        user = data['usuario']
        if 'check_contrasena' in request.POST and 'contrasena' in request.POST and 'confirmar_contrasena' in request.POST:
            if request.POST['contrasena'] == request.POST['confirmar_contrasena']:
                user.set_password(request.POST['contrasena'])
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            data['exito'] = 'Se editó la cuenta <strong>{}</strong>'.format(form.instance.username)
        else:
            data['error'] = 'Hubo un error al editar la cuenta <strong>{}</strong>'.format(user.username)
        data['form'] = form
    if not request.user.is_superuser and request.user.id != user_id:
        return redirect('/')
    return render(request, 'usuario/form_usuario.html', data)

@login_required(login_url='/login/')
def registrar_cuenta(request):
    data = {}
    data['user'] = request.user
    data['form'] = UserForm()
    data['b'] = True
    data['title'] = 'Registrar Cuenta'
    if request.method == 'POST':
        form = UserForm(request.POST)
        m_user = User()
        if request.POST['contrasena'] == request.POST['confirmar_contrasena']:
            m_user.set_password(request.POST['contrasena'])
            form.instance = m_user
            if form.is_valid():
                form.save()
                data['exito'] = 'Se registró la cuenta <strong>{}</strong>'.format(form.instance.username)
                data['form'] = UserForm()
            else:
                data['error'] = 'Hubo un error al registrar la cuenta'
                data['form'] = form
        else:
            data['error'] = 'Contraseñas no coinciden'
            data['form'] = form
    return render(request, 'usuario/form_usuario.html', data)

@login_required(login_url='/login/')
def eliminar_cuenta(request, user_id):
    data = {}
    data['user'] = request.user
    if request.user.id != user_id:
        try:
            with transaction.atomic():
                user = User.objects.get(id=user_id)
                user.delete()
        except DatabaseError:
            pass
        except Exception:
            pass
    return redirect('/autenticacion/usuario/registros/')

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
        data['submodulos_count'] = SubModulo.objects.count()
    else:
        lista = EstudianteCurso.objects.filter(estudiante__usuario__username=user.username).values_list('cursos__id')
        for l in lista:
            l2.append(l[0])
        data['cursos'] = Curso.objects.filter(id__in=l2).annotate(nombre_link=Concat(Value('abrir/'), Replace(Lower(Trim("nombre")), Value(' '), Value('')))).values()

    for i in range(len(data['cursos'])):
        data['cursos'][i]['nombre_link'] = unidecode(data['cursos'][i]['nombre_link'])
    data['user'] = user
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    return render(request, 'home/home.html', data)

# Create your views here.
def forget_password(request):
    data = {}
    if request.method == 'POST':
        pass
    return render(request, 'login/forget_password.html', data)

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