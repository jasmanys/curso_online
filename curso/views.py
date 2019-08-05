#from django import forms
from django.shortcuts import render, redirect
#from django.db import DatabaseError, transaction
from django.contrib.auth.decorators import login_required
from curso.forms import CursoForm, SubModuloForm
from curso.models import *
#from evaluacion.models import Evaluacion
from django.core.exceptions import ObjectDoesNotExist


@login_required(login_url='/login/')
def abrir_curso(request, curso_nombre, curso_id):
    data = {}
    data['user'] = request.user
    estudiante_curso = EstudianteCurso.objects.get(estudiante__usuario__username=request.user.username)
    id_cursos = [str(x[0]) for x in estudiante_curso.cursos.all().values_list('id')]
    if curso_id in id_cursos:
        if request.method == 'POST':
            pass
        else:
            curso = Curso.objects.get(pk = curso_id)
            data['curso'] = curso
            modulos = Modulo.objects.filter(curso__id = curso_id).values()
            for i in range(len(modulos)):
                if i == 0:
                    modulos[i]['habilitado'] = True
                modulos[i]['submodulos'] = SubModulo.objects.filter(modulo__id = modulos[i]['id']).values()
                try:
                    if len(modulos[i]['submodulos']) == EstudianteSubModulo.objects.get(estudiante=estudiante_curso.estudiante).submodulos.count():
                        modulos[i]['completado'] = '&nbsp;&nbsp;&nbsp;&nbsp;<i style="cursor: pointer;" title="Completado" class="fas fa-award text-success"></i>'
                        if i < len(modulos):
                            modulos[i+1]['habilitado'] = True
                except ObjectDoesNotExist:
                    pass
                for ind in range(len(modulos[i]['submodulos'])):
                    if EstudianteSubModulo.objects.filter(estudiante=estudiante_curso.estudiante, submodulos__id=modulos[i]['submodulos'][ind]['id']).exists():
                        modulos[i]['submodulos'][ind]['terminado'] = '&nbsp;&nbsp;&nbsp;&nbsp;<i style="cursor: pointer;" title="Completado" class="fas fa-check text-success"></i>'

            data['modulos'] = modulos
            return render(request, 'curso/modulo/indice_curso.html', data)
    else:
        return redirect('/')

@login_required(login_url='/login/')
def abrir_modulo(request, modulo_id):
    data = {}
    data['user'] = request.user
    modulo = Modulo.objects.get(id = modulo_id)
    estudiante_curso = EstudianteCurso.objects.get(estudiante__usuario__username=request.user.username)
    id_cursos = [x[0] for x in estudiante_curso.cursos.all().values_list('id')]
    if modulo.curso.id in id_cursos:
        if request.method == 'POST':
            pass
        else:
            data['submodulos'] = SubModulo.objects.filter(modulo = modulo).values()
            for i in range(len(data['submodulos'])):
                if EstudianteSubModulo.objects.filter(estudiante=estudiante_curso.estudiante,
                                                      submodulos__id=data['submodulos'][i]['id']).exists():
                    data['submodulos'][i]['completado'] = '&nbsp;&nbsp;&nbsp;&nbsp;<i style="cursor: pointer;" title="Completado" class="fas fa-check text-success"></i>'
            data['modulo'] = modulo
            data['curso_link'] = "/curso/abrir/{}/{}/".format(modulo.curso.nombre.replace(' ', '').lower(), modulo.curso.id)
            return render(request, 'curso/modulo/indice_modulo.html', data)
    else:
        return redirect('/')

@login_required(login_url='/login/')
def abrir_submodulo(request, submodulo_id):
    data = {}
    data['user'] = request.user
    submodulo = SubModulo.objects.get(id = submodulo_id)
    estudiante_curso = EstudianteCurso.objects.get(estudiante__usuario__username=request.user.username)
    id_cursos = [x[0] for x in estudiante_curso.cursos.all().values_list('id')]
    if submodulo.modulo.curso.id in id_cursos:
        if request.method == 'POST':
            pass
        else:
            data['submodulo'] = submodulo
            data['curso_link'] = "/curso/abrir/{}/{}/".format(submodulo.modulo.curso.nombre.replace(' ', '').lower(), submodulo.modulo.curso.id)
            data['enlaces'] = []
            if submodulo.numero > 1:
                try:
                    subm = SubModulo.objects.get(modulo=submodulo.modulo, numero=submodulo.numero - 1)
                    a = '<div class="col-lg-2 col-md-4 col-xs-12 text-break text-justify">'
                    a += '<a class="btn btn-link btn-lg btn-block" data-toggle="tooltip" data-placement="top" title="Ir a {}" href="{}"><i class="fas fa-backward"></i></a>'.format(
                        str(subm.modulo.numero) + '.' + str(subm.numero) + ' ' + subm.titulo, '/curso/submodulo/abrir/id/{}/'.format(subm.id))
                    a += '</div>'
                    data['enlaces'].append(a)
                except ObjectDoesNotExist:
                    pass
            try:
                subm = SubModulo.objects.get(modulo=submodulo.modulo, numero=submodulo.numero + 1)
                a = '<div class="col-lg-2 offset-lg-8 col-md-4 offset-md-4 col-xs-12 text-break text-justify">'
                a += '<a class="btn btn-link btn-lg btn-block" data-toggle="tooltip" data-placement="top" title="Ir a {}" href="{}"><i class="fas fa-forward"></i></a>'.format(
                    str(subm.modulo.numero) + '.' + str(subm.numero) + ' ' + subm.titulo,
                    '/curso/submodulo/abrir/id/{}/'.format(subm.id))
                a += '</div>'
                data['enlaces'].append(a)
            except ObjectDoesNotExist:
                pass
            if EstudianteSubModulo.objects.filter(estudiante=estudiante_curso.estudiante).exists():
                if not EstudianteSubModulo.objects.filter(submodulos=submodulo).exists():
                    est_sub_mod = EstudianteSubModulo.objects.get(estudiante=estudiante_curso.estudiante)
                    est_sub_mod.submodulos.add(submodulo)
            else:
                est_sub_mod = EstudianteSubModulo()
                est_sub_mod.estudiante = estudiante_curso.estudiante
                est_sub_mod.save()
                est_sub_mod.submodulos.add(submodulo)
            return render(request, 'curso/modulo/contenido_submodulo.html', data)
    else:
        return redirect('/')

@login_required(login_url='/login/')
def seleccionar_curso(request):
    data = {}
    data['user'] = request.user
    data['cursos'] = Curso.objects.all()
    return render(request, 'curso/admin/listar_curso.html', data)

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
    data['user'] = request.user
    curso = Curso.objects.get(id = curso_id_el)
    curso_eliminado = "El curso de <strong>{}</strong> fue eliminado".format(curso.nombre)
    data['eliminado'] = curso.delete()
    return redirect('/', curso_eli = curso_eliminado)

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
def agregar_submodulo(request, modulo_id):
    data = {}
    data['user'] = request.user
    data['modulo'] = Modulo.objects.get(id=modulo_id)
    data['agregar_submodulo'] = True
    if request.method == 'POST':
        form = SubModuloForm(request.POST)
        if form.is_valid():
            form.save()
            submod = SubModulo()
            submod.numero = 1
            submod.modulo = data['modulo']
            data['form'] = SubModuloForm(instance=submod)
            data['exito'] = "Se guardó el submódulo <strong>{}</strong>".format(form.instance.titulo)
        else:
            data['form'] = form
            data['error'] = "Hubo un error al guardar el submódulo"
        return render(request, 'curso/admin/form_submodulo.html', data)

    else:
        submod = SubModulo()
        submod.numero = 1
        submod.modulo = data['modulo']
        data['form'] = SubModuloForm(instance=submod)
        return render(request, 'curso/admin/form_submodulo.html', data)

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
def editar_submodulo(request, submodulo_id):
    data = {}
    data['user'] = request.user
    data['submodulo'] = SubModulo.objects.get(id=submodulo_id)
    data['modulo'] = Modulo.objects.get(id = data['submodulo'].modulo.id)
    data['curso'] = Curso.objects.get(id=data['modulo'].curso.id)
    data['form'] = SubModuloForm(instance=data['submodulo'])
    if request.method == 'POST':
        form = SubModuloForm(request.POST, instance=data['submodulo'])
        if form.is_valid():
            form.save()
            return redirect('/curso/submodulo/registros/{}/'.format(data['modulo'].id))
        else:
            data['form'] = form
            data['error'] = "Hubo un error al guardar el submódulo"
        return render(request, 'curso/admin/form_submodulo.html', data)
    else:
        return render(request, 'curso/admin/form_submodulo.html', data)

@login_required(login_url='/login/')
def eliminar_submodulo(request, submodulo_id):
    data = {}
    data['user'] = request.user
    submodulo = SubModulo.objects.get(id=submodulo_id)
    modulo_id = submodulo.modulo.id
    submodulo.delete()
    return redirect('/curso/submodulo/registros/{}/'.format(modulo_id))

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
    modulos = Modulo.objects.filter(curso__id=curso_id)
    data['modulos'] = modulos
    return render(request, 'curso/admin/listar_modulo.html', data)

@login_required(login_url='/login/')
def registro_submodulos(request, modulo_id):
    data = {}
    data['user'] = request.user
    data['modulo'] = Modulo.objects.get(id = modulo_id)
    data['submodulos'] = SubModulo.objects.filter(modulo = data['modulo'])
    return render(request, 'curso/admin/listar_submodulo.html', data)