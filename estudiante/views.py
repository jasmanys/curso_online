from django.contrib.auth.models import User
from django.db import transaction, DatabaseError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from estudiante.forms import UserForm, EstudianteForm
from estudiante.models import Estudiante
import re
val_usuario = re.compile('[a-z0-9@.+-_]{4,150}')
val_contrasena = re.compile('[a-z0-9@.+-_]{4,150}')
val_celular = re.compile('[0-9]{10,15}')
val_cedula = re.compile('[0-9]{10}')

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
    #data['usuarios'] = User.objects.filter(is_active=True, is_superuser=False, is_staff=False).all()
    data['user'] = request.user
    data['form_user'] = UserForm()
    data['form_estudiante'] = EstudianteForm()
    if request.method == 'POST':
        form_user = UserForm(request.POST)
        form_estudiante = EstudianteForm(request.POST)
        try:
            with transaction.atomic():
                if form_user.is_valid() and form_estudiante.is_valid():
                    form_user.save()
                    est = Estudiante(usuario=form_user.instance)
                    form_estudiante = EstudianteForm(request.POST, instance=est)
                    form_estudiante.save()
                    data['exito'] = 'El estudiante <strong>Username: {} - Nombres: {} - Cédula: {}</strong> se registró correctamente'.format(form_user.instance.username, form_user.instance.first_name + ' ' + form_user.instance.last_name, form_estudiante.instance.cedula)
                else:
                    data['form_user'] = form_user
                    data['form_estudiante'] = form_estudiante
                    data['error'] = 'Error en los datos'
        except DatabaseError:
            data['error'] = 'Error al registrar'
    return render(request, 'estudiante/form_estudiante.html', data)

@login_required(login_url='/login/')
def editar_estudiante(request, estudiante_id):
    data = {}
    data['title'] = 'Editar Estudiante'
    #data['usuarios'] = User.objects.filter(is_active=True, is_superuser=False, is_staff=False).all()
    data['user'] = request.user
    estudiante = Estudiante.objects.get(id=estudiante_id)
    data['editar'] = True
    data['form_estudiante'] = EstudianteForm(instance=estudiante)
    if request.method == 'POST':
        estudiante = Estudiante.objects.get(id=request.POST['estudiante_id'])
        form_estudiante = EstudianteForm(request.POST, instance=estudiante)
        try:
            with transaction.atomic():
                if form_estudiante.is_valid():
                    form_estudiante.save()
                    data['exito'] = 'Se editó el registro del estudiante <strong>Username: {} - Nombres: {} - Cédula: {}</strong> correctamente'.format(form_estudiante.instance.usuario.username, form_estudiante.instance.usuario.first_name + ' ' + form_estudiante.instance.usuario.last_name, form_estudiante.instance.cedula)
                else:
                    data['form_estudiante'] = form_estudiante
                    data['error'] = 'Error en los datos'
        except DatabaseError:
            data['error'] = 'Error al registrar'
    return render(request, 'estudiante/form_estudiante.html', data)

@login_required(login_url='/login/')
def eliminar_estudiante(request, estudiante_id):
    data = {}
    data['user'] = request.user
    try:
        with transaction.atomic():
            estudiante = Estudiante.objects.get(id=estudiante_id)
            estudiante.delete()
    except DatabaseError:
        pass
    except Exception:
        pass
    return redirect('/estudiante/registros/')