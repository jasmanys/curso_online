from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from curso.models import *
from evaluacion.forms import EnunciadoEvaluacionForm
from evaluacion.models import *
from django.db import DatabaseError, transaction
#Imagen decoded
def decode_base64_file(data):
    def get_file_extension(file_name, decoded_file):
        import imghdr
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension

    from django.core.files.base import ContentFile
    import base64
    import six
    import uuid

    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "{}.{}".format(file_name, file_extension)

        return ContentFile(decoded_file, name=complete_file_name)
#Imagen decoded

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
    data['modulo'] = Modulo.objects.get(id=modulo_id)
    submodulos = SubModulo.objects.filter(modulo__id=modulo_id).values()
    for i in range(len(submodulos)):
        submodulos[i]['count_enunciado'] = EnunciadoEvaluacion.objects.filter(submodulo__id=submodulos[i]['id']).count()
    data['submodulos'] = submodulos
    data['eval'] = True
    return render(request, 'curso/admin/listar_submodulo.html', data)

@login_required(login_url='/login/')
def eliminar_evaluacion(request, modulo_id):
    data = {}
    data['user'] = request.user
    mod = Modulo.objects.get(id = modulo_id)
    try:
        with transaction.atomic():
            ev = Evaluacion.objects.get(modulo=mod)
            ev.delete()
    except DatabaseError:
        pass
    return redirect('/evaluacion/modulos/{}/'.format(mod.curso.id))

@login_required(login_url='/login/')
def registros_enunciado(request, submodulo_id):
    data = {}
    data['user'] = request.user
    data['submodulo'] = SubModulo.objects.get(id = submodulo_id)
    data['enunciados'] = EnunciadoEvaluacion.objects.filter(submodulo__id=submodulo_id)
    return render(request, 'curso/admin/listar_enunciado.html', data)

def ret_data_editar_enunciado(request, enunciado_id):
    data = {}
    data['user'] = request.user
    data['enunciado_evaluacion'] = EnunciadoEvaluacion.objects.get(id=enunciado_id)
    data['hidden_tipo_enunciado'] = data['enunciado_evaluacion'].tipo_respuesta
    opciones_enunciado = OpcionEnunciado.objects.filter(enunciado_evaluacion=data['enunciado_evaluacion']).values()
    for i in range(len(opciones_enunciado)):
        opciones_enunciado[i]['respuesta'] = SeleccionMultiple.objects.get(
            opcion_enunciado__id=opciones_enunciado[i]['id']).respuesta
        if opciones_enunciado[i]['imagen']:
            opciones_enunciado[i]['opcion'] = OpcionEnunciado.objects.get(id=opciones_enunciado[i]['id']).imagen_base64
        opciones_enunciado[i]['fr'] = i + 1
    data['opciones_enunciado'] = opciones_enunciado
    data['eval'] = True
    data['editar_enunciado'] = True
    return data

@login_required(login_url='/login/')
def editar_enunciado(request, enunciado_id):
    data = {}
    data = ret_data_editar_enunciado(request, enunciado_id)
    form = None
    if request.method == 'POST':
        try:
            with transaction.atomic():
                add_msg = ''
                if 'foto' in request.FILES:
                    add_msg = ' (También se adjuntó una imagen)'
                else:
                    if 'eliminar_foto_enunciado' in request.POST:
                        if request.POST['eliminar_foto_enunciado'] == 'true':
                            data['enunciado_evaluacion'].foto = None
                form = EnunciadoEvaluacionForm(request.POST, request.FILES, instance=data['enunciado_evaluacion'])
                if form.is_valid():
                    form.save()
                    opcion_enunciados = OpcionEnunciado.objects.filter(enunciado_evaluacion = form.instance).values()
                    for oe in opcion_enunciados:
                        oeo = OpcionEnunciado.objects.get(id=oe['id'])
                        seleccion_multiple = SeleccionMultiple.objects.filter(opcion_enunciado=oeo).values()
                        for sm in seleccion_multiple:
                            sml = SeleccionMultiple.objects.get(id=sm['id'])
                            sml.delete()
                        oeo.delete()
                    for lis in request.POST.getlist('lista_de_enunciados'):
                        temp = lis.split('|')
                        opcion_enunciado = OpcionEnunciado()
                        opcion_enunciado.enunciado_evaluacion = form.instance
                        if form.instance.tipo_respuesta in [0, 1]:
                            opcion_enunciado.opcion = temp[0]
                        elif form.instance.tipo_respuesta in [2, 3]:
                            opcion_enunciado.imagen = decode_base64_file(temp[0])
                        opcion_enunciado.save()
                        if form.instance.tipo_respuesta in [0, 1, 2, 3]:
                            seleccion_multiple = SeleccionMultiple()
                            seleccion_multiple.opcion_enunciado = opcion_enunciado
                            if temp[len(temp) - 1] == 'true':
                                seleccion_multiple.respuesta = True
                            else:
                                seleccion_multiple.respuesta = False
                            seleccion_multiple.save()
                    data = ret_data_editar_enunciado(request, enunciado_id)
                    data['exito'] = "Se editó el enunciado <strong>{} {}</strong>".format(form.instance.enunciado, add_msg)
                else:
                    data['error'] = "error en los datos a registrar"
        except DatabaseError:
            data['error'] = "error al guardar el enunciado"
    if form:
        data['form_enunciado_evaluacion'] = form
    else:
        data['form_enunciado_evaluacion'] = EnunciadoEvaluacionForm(instance=data['enunciado_evaluacion'])
    return render(request, 'curso/admin/form_enunciado.html', data)

@login_required(login_url='/login/')
def eliminar_enunciado(request, enunciado_id):
    data = {}
    data['user'] = request.user
    codigo = ''
    try:
        with transaction.atomic():
            en = EnunciadoEvaluacion.objects.get(id=enunciado_id)
            codigo = en.submodulo.id
            en.delete()
    except DatabaseError:
        pass
    except ObjectDoesNotExist:
        return redirect('/')
    return redirect('/evaluacion/registros/enunciado/{}/'.format(codigo))

@login_required(login_url='/login/')
def registro_enunciado(request, submodulo_id):
    data = {}
    data['user'] = request.user
    data['submodulo'] = SubModulo.objects.get(id=submodulo_id)
    data['agregar_enunciado'] = True
    data['enunciado_evaluacion'] = EnunciadoEvaluacion.objects.filter(submodulo__id=submodulo_id)
    data['eval'] = True
    form = None
    if request.method == 'POST':
        try:
            with transaction.atomic():
                add_msg = ''
                if 'foto' in request.FILES:
                    add_msg = ' (También se adjuntó una imagen)'
                form = EnunciadoEvaluacionForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    for lis in request.POST.getlist('lista_de_enunciados'):
                        temp = lis.split('|')
                        opcion_enunciado = OpcionEnunciado()
                        opcion_enunciado.enunciado_evaluacion = form.instance
                        if form.instance.tipo_respuesta in [0, 1]:
                            opcion_enunciado.opcion = temp[0]
                        elif form.instance.tipo_respuesta in [2, 3]:
                            opcion_enunciado.imagen = decode_base64_file(temp[0])
                        opcion_enunciado.save()
                        if form.instance.tipo_respuesta in [0, 1, 2, 3]:
                            seleccion_multiple = SeleccionMultiple()
                            seleccion_multiple.opcion_enunciado = opcion_enunciado
                            if temp[len(temp)-1] == 'true':
                                seleccion_multiple.respuesta = True
                            else:
                                seleccion_multiple.respuesta = False
                            seleccion_multiple.save()
                    data['exito'] = 'Se guardó el enunciado <strong><a title="¿Editar?" href="/evaluacion/editar/enunciado/{}/">{}</a> {}</strong>'.format(form.instance.id, form.instance.enunciado, add_msg)
                    form = None
                else:
                    data['error'] = "error en los datos a registrar"
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