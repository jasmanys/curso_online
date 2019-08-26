from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse
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

def convertir_a_diccionario(valor):
    data = {}
    try:
        value = eval(valor)  # Convertir a dict
        if str(type(value)) == "<class 'dict'>":  # Comprobar que sea dict
            return value
        else:
            data['error'] = 'No pudo registrarse su evaluación, inténtelo nuevamente'
    except Exception as e:
        data['error'] = 'Datos incongruentes'
    return data

@login_required(login_url='/login/')
def evaluar_modulo(request, modulo_id):
    data = {}
    user = request.user
    estudiante_curso = EstudianteCurso.objects.get(estudiante__usuario=user)

    if request.method == 'POST':
        if 'hidden_modulo_id' in request.POST:
            hidden_modulo_id = int(request.POST['hidden_modulo_id'])
            try:
                with transaction.atomic():
                    recoger = ""
                    #Llamar a la evaluacion que se va a calificar
                    evaluacion = Evaluacion.objects.get(modulo__id=hidden_modulo_id)
                    #Llamar a todos los enunciados de la evaluación a calificar
                    enunciado_evaluacion = EnunciadoEvaluacion.objects.filter(evaluacion=evaluacion).all()
                    #Registrar al estudiante que va a ser calificado con la evaluación
                    estudiante_evaluacion = EstudianteEvaluacion(estudiante=estudiante_curso, evaluacion=evaluacion,calificacion=0)
                    estudiante_evaluacion.save()
                    #Para obtener la nota de cada enunciado respondido, se va a dividir la calificación máxima de la evaluación (100)...
                    #...entre la cantidad de enunciados que haya en la evaluación
                    nota_por_enunciado = float(evaluacion.calificacion_maxima / enunciado_evaluacion.count())
                    calificacion_total = 0
                    #Registrar los enunciados que respondió el estudiante
                    for enun in enunciado_evaluacion:
                        detalle_estudiante_evaluacion = DetalleEstudianteEvaluacion(estudiante_evaluacion=estudiante_evaluacion,
                                                                                    enunciado_evaluacion=EnunciadoEvaluacion.objects.get(id=enun.id),
                                                                                    calificacion_obtenida=0,
                                                                                    calificacion_maxima=nota_por_enunciado)
                        detalle_estudiante_evaluacion.save()
                        #Calificar pregunta de opción única
                        if enun.tipo_respuesta in [0, 2]:#Preguntar si el tipo de respuesta es de opción única
                            #Traer todos los enunciados registrados
                            opciones_del_enunciado = OpcionEnunciado.objects.filter(enunciado_evaluacion__id=enun.id)
                            #Comprobar que las respuestas se hayan enviado correctamente al servidor
                            if 'respuesta_opcion_{}'.format(enun.id) in request.POST:
                                value = convertir_a_diccionario(request.POST['respuesta_opcion_{}'.format(enun.id)])#Convertir a dict
                                if not 'error' in value:#Asegurarse que no haya algún error
                                    #Obtener la respuesta que el estudiante realizó
                                    respuesta_del_estudiante = SeleccionMultiple.objects.get(opcion_enunciado__id=value['id_opcion'])
                                    # Obtener la respuesta correcta
                                    respuesta_correcta = SeleccionMultiple.objects.get(opcion_enunciado__enunciado_evaluacion__id=enun.id,
                                                                                       respuesta=True)
                                    #Registrar la respuesta del estudiante
                                    calificacion_seleccion_multiple = CalificacionSeleccionMultiple(
                                        estudiante_evaluacion=estudiante_evaluacion, seleccion_multiple=respuesta_correcta,
                                        respuesta_estudiante=respuesta_del_estudiante.respuesta)
                                    calificacion_seleccion_multiple.save()
                                    #Preguntar si la respuesta del estudiante coincide con la correcta...
                                    if respuesta_correcta.respuesta == respuesta_del_estudiante.respuesta:
                                        #...si es así, irá aumentando su calificación
                                        calificacion_total += nota_por_enunciado

                                else:
                                    data['error'] = value['error']
                        if enun.tipo_respuesta in [1, 3]:  # Preguntar si el tipo de respuesta es de opción múltiple
                            # Comprobar que las respuestas se hayan enviado correctamente al servidor
                            if 'lista_enunciado_{}'.format(enun.id) in request.POST:
                                recoger += "entro a opcion multiple, "
                                respuestas = request.POST.getlist('lista_enunciado_{}'.format(enun.id))
                                # Obtener las respuestas correctas
                                respuestas_correctas = SeleccionMultiple.objects.filter(opcion_enunciado__enunciado_evaluacion__id=enun.id, respuesta=True)
                                nota_por_enunciado_actual = float(nota_por_enunciado / respuestas_correctas.count())
                                for res in respuestas:
                                    recoger += "entro a iterar, "
                                    value = convertir_a_diccionario(res)  # Convertir a dict
                                    if not 'error' in value:  # Asegurarse que no haya algún error
                                        # Obtener la respuesta que el estudiante realizó
                                        respuesta_del_estudiante = SeleccionMultiple.objects.get(opcion_enunciado__id=value['id_opcion'])
                                        #A razón de que el enunciado puede haber más de una respuesta correcta,...
                                        #...se debe iterar
                                        for rc in respuestas_correctas:
                                            recoger += "entro a iterar rc, "
                                            #Registrar la respuesta del estudiante
                                            if respuesta_del_estudiante.id == rc.id:
                                                calificacion_seleccion_multiple = CalificacionSeleccionMultiple(estudiante_evaluacion=estudiante_evaluacion, seleccion_multiple__id=rc.id, respuesta_estudiante=respuesta_del_estudiante.respuesta)
                                                calificacion_seleccion_multiple.save()
                                                recoger += "entro a guardar rc, "
                                            #Preguntar si la respuesta del estudiante coincide con la correcta...
                                            if respuesta_del_estudiante.respuesta == rc.respuesta:
                                                # ...si es así, irá aumentando su calificación
                                                calificacion_total += nota_por_enunciado_actual
                                                recoger += "entro a sumar rc, "
                    estudiante_evaluacion.calificacion = float(calificacion_total)
                    estudiante_evaluacion.save()
                    data['exito'] = "todo salió posi, su calificación es de {} puntos {}".format(calificacion_total, recoger)
            except ValueError:
                data['error'] = "No se pudo registrar"
            """except ObjectDoesNotExist:
                data['error'] = "No se pudo registrar"
            except MultipleObjectsReturned:
                data['error'] = "No se pudo registrar"""
    evaluacion = Evaluacion.objects.get(modulo__id=modulo_id)
    enunciado_evaluacion = EnunciadoEvaluacion.objects.filter(evaluacion=evaluacion).values()
    fr = 0
    for i in range(len(enunciado_evaluacion)):
        enunciado_evaluacion[i]['opciones_enunciado'] = OpcionEnunciado.objects.filter(enunciado_evaluacion__id=enunciado_evaluacion[i]['id']).values()
        for j in range(len(enunciado_evaluacion[i]['opciones_enunciado'])):
            fr += 1
            enunciado_evaluacion[i]['opciones_enunciado'][j]['fr'] = fr
            if enunciado_evaluacion[i]['tipo_respuesta'] in [0, 1, 2, 3]:
                enunciado_evaluacion[i]['opciones_enunciado'][j]['respuesta'] = SeleccionMultiple.objects.get(opcion_enunciado__id=enunciado_evaluacion[i]['opciones_enunciado'][j]['id']).respuesta
            if enunciado_evaluacion[i]['tipo_respuesta'] in [2, 3]:
                enunciado_evaluacion[i]['opciones_enunciado'][j]['opcion_img'] = OpcionEnunciado.objects.get(id=enunciado_evaluacion[i]['opciones_enunciado'][j]['id']).imagen_base64

    data['user'] = user
    data['estudiante_curso'] = estudiante_curso
    data['evaluacion'] = evaluacion
    data['enunciado_evaluacion'] = enunciado_evaluacion
    return render(request, 'estudiante/evaluar_modulo.html', data)

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