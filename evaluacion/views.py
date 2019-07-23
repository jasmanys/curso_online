from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from curso.models import *
from evaluacion.forms import EnunciadoEvaluacionForm
from evaluacion.models import *


@login_required(login_url='/login/')
def view(request):
    pass

@login_required(login_url='/login/')
def seleccionar_curso_para_add_evaluacion(request):
    data = {}
    data['user'] = request.user
    cursos = Curso.objects.all().values()
    """for i in range(len(cursos)):
        cursos[i]['eval_count'] = Evaluacion.objects.filter(curso__id = cursos[i]['id']).count()"""
    data['eval'] = True
    data['cursos'] = cursos
    return render(request, 'curso/admin/listar_curso.html', data)

@login_required(login_url='/login/')
def registro_modulos_para_add_evaluacion(request, curso_id):
    data = {}
    data['user'] = request.user
    data['curso'] = Curso.objects.get(id=curso_id)
    modulos = Modulo.objects.filter(curso__id=curso_id).values()
    for i in range(len(modulos)):
        modulos[i]['eval_count'] = Evaluacion.objects.filter(modulo__id=modulos[i]['id']).count()
    data['modulos'] = modulos
    data['eval'] = True
    return render(request, 'curso/admin/listar_modulo.html', data)

@login_required(login_url='/login/')
def registro_evaluacion(request, modulo_id):
    data = {}
    data['user'] = request.user
    submodulos = SubModulo.objects.filter(modulo__id=modulo_id).values()
    for i in range(len(submodulos)):
        submodulos[i]['count_enunciado'] = EnunciadoEvaluacion.objects.filter(submodulo__id=submodulos[i]['id']).count()
    data['submodulos'] = submodulos
    data['eval'] = True
    return render(request, 'curso/admin/listar_submodulo.html', data)

@login_required(login_url='/login/')
def registro_enunciado(request, submodulo_id):
    data = {}
    data['user'] = request.user
    data['submodulo'] = SubModulo.objects.get(id=submodulo_id)
    data['enunciado_evaluacion'] = EnunciadoEvaluacion.objects.filter(submodulo__id=submodulo_id)
    data['eval'] = True
    if request.method == 'POST':
        pass
    if Evaluacion.objects.filter(modulo__id=data['submodulo'].modulo.id).exists():
        evaluacion = Evaluacion.objects.get(modulo__id=data['submodulo'].modulo.id)
    else:
        evaluacion = Evaluacion()
        evaluacion.modulo = Modulo.objects.get(id = data['submodulo'].modulo.id)
        evaluacion.save()
    enunciado_evaluacion = EnunciadoEvaluacion()
    enunciado_evaluacion.submodulo = data['submodulo']
    enunciado_evaluacion.evaluacion = evaluacion
    data['form_enunciado_evaluacion'] = EnunciadoEvaluacionForm(instance=enunciado_evaluacion)
    return render(request, 'curso/admin/form_enunciado.html', data)