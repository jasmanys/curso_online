from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from curso.models import *
from evaluacion.forms import EnunciadoEvaluacionForm
from evaluacion.models import *
from django.db import DatabaseError, transaction


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
    form = None
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = EnunciadoEvaluacionForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    for lis in request.POST.getlist('lista_de_enunciados'):
                        temp = lis.split('|')
                        opcion_enunciado = OpcionEnunciado()
                        opcion_enunciado.enunciado_evaluacion = form.instance
                        opcion_enunciado.opcion = temp[0]
                        opcion_enunciado.save()
                        if form.instance.tipo_respuesta in [0, 1]:
                            seleccion_multiple = SeleccionMultiple()
                            seleccion_multiple.opcion_enunciado = opcion_enunciado
                            if temp[len(temp)-1] == 'true':
                                seleccion_multiple.respuesta = True
                            else:
                                seleccion_multiple.respuesta = False
                            seleccion_multiple.save()
                    data['exito'] = "Se guardó el enunciado <strong>{}</strong>".format(form.instance.enunciado)
                    form = None
                else:
                    data['error'] = "error en el form"
        except DatabaseError:
            data['error'] = "error al guardar el enunciado"
    if form:
        data['form_enunciado_evaluacion'] = form
    else:
        if Evaluacion.objects.filter(modulo__id=data['submodulo'].modulo.id).exists():
            evaluacion = Evaluacion.objects.get(modulo__id=data['submodulo'].modulo.id)
        else:
            evaluacion = Evaluacion()
            evaluacion.modulo = Modulo.objects.get(id=data['submodulo'].modulo.id)
            evaluacion.save()
        enunciado_evaluacion = EnunciadoEvaluacion()
        enunciado_evaluacion.submodulo = data['submodulo']
        enunciado_evaluacion.evaluacion = evaluacion
        data['form_enunciado_evaluacion'] = EnunciadoEvaluacionForm(instance=enunciado_evaluacion)
    return render(request, 'curso/admin/form_enunciado.html', data)