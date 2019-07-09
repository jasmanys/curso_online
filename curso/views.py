from django.shortcuts import render

from curso.models import Modulo, AnteModulo, SubModulo


def seleccionar_curso(request, curso_nombre, curso_id):
    data = {}
    modulos = Modulo.objects.filter(curso__id = curso_id).values()
    for i in range(len(modulos)):
        modulos[i]['antemodulos'] = AnteModulo.objects.filter(modulo__id = modulos[i]['id']).values()
        submodulos = []#
        for j in range(len(modulos[i]['antemodulos'])):
            submodulos = SubModulo.objects.filter(antemodulo__id=modulos[i]['antemodulos'][j]['id']).values()
            modulos[i]['antemodulos'][j]['submodulos'] = submodulos
            submodulos = []  #

    data['modulos'] = modulos
    return render(request, 'curso/modulo/indice_curso.html', data)