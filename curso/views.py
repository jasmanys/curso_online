from django import forms
from django.shortcuts import render, redirect
from django.db import DatabaseError, transaction
from django.contrib.auth.decorators import login_required
from curso.forms import CursoForm
from curso.models import *

@login_required(login_url='/login/')
def seleccionar_curso(request):
    data = {}
    data['user'] = request.user
    data['cursos'] = Curso.objects.all()
    return render(request, 'curso/admin/listar_curso.html', data)
"""def seleccionar_curso(request, curso_nombre, curso_id):
    data = {}
    data['user'] = request.user
    curso = Curso.objects.get(pk = curso_id)
    data['curso'] = curso
    modulos = Modulo.objects.filter(curso__id = curso_id).values()
    for i in range(len(modulos)):
        modulos[i]['antemodulos'] = AnteModulo.objects.filter(modulo__id = modulos[i]['id']).values()
        submodulos = []#
        for j in range(len(modulos[i]['antemodulos'])):
            submodulos = SubModulo.objects.filter(antemodulo__id=modulos[i]['antemodulos'][j]['id']).values()
            modulos[i]['antemodulos'][j]['submodulos'] = submodulos
            submodulos = []  #

    data['modulos'] = modulos
    if request.user.is_superuser:
        return render(request, 'curso/admin/form_curso.html', data)
    else:
        return render(request, 'curso/modulo/indice_curso.html', data)"""

@login_required(login_url='/login/')
def agregar_curso(request):
    data = {}
    data['user'] = request.user
    data['accion'] = 'Nuevo Curso'
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            data['form'] = form
            return render(request, 'curso/admin/form_curso.html', data)
    else:
        data['form'] = CursoForm()
        return render(request, 'curso/admin/form_curso.html', data)

@login_required(login_url='/login/')
def editar_curso(request, curso_id_ed):
    data = {}
    data['accion'] = 'Editar Curso'
    data['user'] = request.user
    if request.method == 'POST':
        curso = Curso.objects.get(id = curso_id_ed)
        if request.FILES:
            form = CursoForm(request.POST, request.FILES, instance=curso)
        else:
            form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            data['form'] = form
            return render(request, 'curso/admin/form_curso.html', data)
    else:
        curso = Curso.objects.get(id = curso_id_ed)
        data['form'] = CursoForm(instance = curso)
        return render(request, 'curso/admin/form_curso.html', data)

@login_required(login_url='/login/')
def eliminar_curso(request, curso_id_el):
    data = {}
    data['accion'] = 'Eliminar Curso'
    data['user'] = request.user
    if request.method == 'POST':
        pass
    else:
        pass

@login_required(login_url='/login/')
def agregar_modulo(request, curso_id):
    data = {}
    data['user'] = request.user
    data['curso'] = Curso.objects.get(id=curso_id)
    if request.method == 'POST':
        idcurso = request.POST['id_curso']
        modulo = request.POST['titulo']
        if len(modulo) > 0:
            mod = Modulo()
            mod.curso_id = idcurso
            mod.titulo = modulo
            mod.save()
            if mod.id:
                data['exito'] = "Se guardó el módulo <strong>{}</strong> en el curso de <strong>{}</strong>".format(mod.titulo, mod.curso.nombre)
            else:
                data['titulo'] = mod.titulo
                data['error'] = "Hubo un error al guardar el módulo"
        else:
            data['error'] = "No deje campos vacíos"
        return render(request, 'curso/admin/form_modulo.html', data)
    else:
        return render(request, 'curso/admin/form_modulo.html', data)

@login_required(login_url='/login/')
def editar_modulo(request, modulo_id):
    data = {}
    data['user'] = request.user
    data['modulo'] = Modulo.objects.get(id = modulo_id)
    data['curso'] = Curso.objects.get(id=data['modulo'].curso.id)
    if request.method == 'POST':
        idmodulo = request.POST['id_modulo']
        modulo = request.POST['titulo']
        if len(modulo) > 0:
            mod = Modulo.objects.get(id = idmodulo)
            mod.titulo = modulo
            mod.save()
            if mod.id:
                return redirect('/curso/modulo/registros/{}/'.format(mod.curso.id))
            else:
                data['titulo'] = mod.titulo
                data['error'] = "Hubo un error al guardar el módulo"
        else:
            data['error'] = "No deje campos vacíos"
        return render(request, 'curso/admin/form_modulo.html', data)
    else:
        return render(request, 'curso/admin/form_modulo.html', data)

@login_required(login_url='/login/')
def eliminar_modulo(request, modulo_id):
    data = {}
    data['user'] = request.user
    modulo = Modulo.objects.get(id=modulo_id)
    curso_id = modulo.curso.id
    modulo.delete()
    return redirect('/curso/modulo/registros/{}/'.format(curso_id))

@login_required(login_url='/login/')
def registro_modulos(request, curso_id):
    data = {}
    data['user'] = request.user
    data['curso'] = Curso.objects.get(id=curso_id)
    data['modulos'] = Modulo.objects.filter(curso__id=curso_id)
    return render(request, 'curso/admin/listar_modulo.html', data)