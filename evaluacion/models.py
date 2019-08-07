from django.db import models
from curso.models import Modulo, SubModulo
from estudiante.models import Estudiante

class Evaluacion(models.Model):
    modulo = models.OneToOneField(Modulo, verbose_name='Módulo', on_delete=models.CASCADE)
    calificacion_maxima = models.FloatField(default=100)
    calificacion_minima = models.FloatField(default=70)

    def __str__(self):
        return self.modulo

    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'

class EnunciadoEvaluacion(models.Model):
    RESPUESTA_UNICA = 0
    OPCION_MULTIPLE = 1
    RESPUESTA_UNICA_CON_IMAGEN = 2
    OPCION_MULTIPLE_CON_IMAGEN = 3
    RELACIONAR_CONCEPTO = 4
    RESPUESTA_CHOICES = (
        (RESPUESTA_UNICA, 'Respuesta única'),
        (OPCION_MULTIPLE, 'Opción múltiple'),
        (RESPUESTA_UNICA_CON_IMAGEN, 'Respuesta única (con imagen)'),
        (OPCION_MULTIPLE_CON_IMAGEN, 'Opción múltiple (con imagen)'),
        #(RELACIONAR_CONCEPTO, 'Relacionar concepto'),
    )
    tipo_respuesta_dict = dict(RESPUESTA_CHOICES)
    evaluacion = models.ForeignKey(Evaluacion, verbose_name='Evaluación', on_delete=models.CASCADE)
    submodulo = models.ForeignKey(SubModulo, verbose_name='SubModulo', on_delete=models.CASCADE)
    enunciado = models.TextField(verbose_name='Enunciado', max_length=500)
    tipo_respuesta = models.IntegerField(verbose_name='Tipo de Respuesta', choices=RESPUESTA_CHOICES)
    foto = models.ImageField(verbose_name='Imagen para el enunciado (Opcional)', upload_to='fotos_enunciado/', blank=True, null=True)

    def __str__(self):
        return self.enunciado

    def ret_tipo_respuesta(self):
        return self.tipo_respuesta_dict[self.tipo_respuesta]

    class Meta:
        verbose_name = 'Enunciado'
        verbose_name_plural = 'Enunciados'

class OpcionEnunciado(models.Model):
    enunciado_evaluacion = models.ForeignKey(EnunciadoEvaluacion, verbose_name='Enunciado Evaluacion', on_delete=models.PROTECT)
    opcion = models.TextField(verbose_name='Enunciado', max_length=200, null=True, blank=True)
    imagen = models.ImageField(verbose_name='Imagen', upload_to='fotos_opciones_enunciado/', null=True, blank=True)

    def __str__(self):
        return self.opcion

    class Meta:
        verbose_name = 'Opción del Enunciado'
        verbose_name_plural = 'Opciones del Enunciado'

class SeleccionMultiple(models.Model):
    opcion_enunciado = models.ForeignKey(OpcionEnunciado, on_delete=models.CASCADE)
    respuesta = models.BooleanField(verbose_name='Respuesta')

    def opcion(self):
        return self.opcion_enunciado.opcion

    def __str__(self):
        return 'Opcion: {} - Respuesta: {}'.format(self.opcion_enunciado.opcion, self.respuesta)

    class Meta:
        verbose_name = 'Seleccion Multiple'

class RelacionarConcepto(models.Model):
    opcion_enunciado = models.ForeignKey(OpcionEnunciado, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(OpcionEnunciado, on_delete=models.CASCADE, null=True, blank=True, related_name='fk_respuesta')

    def opcion(self):
        return self.opcion_enunciado.opcion

    def respuesta_opcion(self):
        return self.respuesta.opcion

    def __str__(self):
        return 'Opcion: {} - Respuesta: {}'.format(self.opcion_enunciado.opcion, self.respuesta.opcion)

    class Meta:
        verbose_name = 'Relacionar Concepto'
        verbose_name_plural = 'Relacionar Conceptos'

class EstudianteEvaluacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.PROTECT)
    calificacion = models.FloatField()

    def __str__(self):
        return 'Estudiante: {} - Evaluacion: {} - Calificacion: {}'.format(self.estudiante.nombres(),
                                                                           self.evaluacion.modulo.titulo,
                                                                           self.calificacion)

    class Meta:
        verbose_name = 'Evaluación del Estudiante'
        verbose_name_plural = 'Evaluaciones de los Estudiantes'

class DetalleEstudianteEvaluacion(models.Model):
    estudiante_evaluacion = models.ForeignKey(EstudianteEvaluacion, on_delete=models.PROTECT)
    enunciado_evaluacion = models.ForeignKey(EnunciadoEvaluacion, on_delete=models.PROTECT)
    calificacion_obtenida = models.FloatField()
    calificacion_maxima = models.FloatField()

    def __str__(self):
        return 'Estudiante: {} - Enunciado: {} - Calificacion: {}/{}'.format(self.estudiante_evaluacion.estudiante.nombres(),
                                                                             self.enunciado_evaluacion.enunciado,
                                                                            self.calificacion_obtenida, self.calificacion_maxima)

    class Meta:
        verbose_name = 'Detalle de la evaluación'
        verbose_name_plural = 'Detalle de Evaluaciones'

class CalificacionSeleccionMultiple(models.Model):
    estudiante = models.ForeignKey(Estudiante, verbose_name='Estudiante', on_delete=models.PROTECT)
    seleccion_multiple = models.ForeignKey(SeleccionMultiple, verbose_name='Pregunta', on_delete=models.PROTECT)
    respuesta_estudiante = models.BooleanField(verbose_name='Respuesta del Estudiante')

    def __str__(self):
        return 'Estudiante: {} - Pregunta: {}, {} - Respondió: {}'.format(self.estudiante.nombres(),
                                                                          self.seleccion_multiple.opcion(),
                                                                          self.seleccion_multiple.respuesta,
                                                                          self.respuesta_estudiante)

    class Meta:
        verbose_name = 'Calificacion de Seleccion Multiple'

class CalificacionRelacionarConcepto(models.Model):
    estudiante = models.ForeignKey(Estudiante, verbose_name='Estudiante', on_delete=models.PROTECT)
    relacionar_concepto = models.ForeignKey(RelacionarConcepto, verbose_name='Pregunta', on_delete=models.PROTECT)
    respuesta_estudiante = models.ForeignKey(OpcionEnunciado, verbose_name='Respuesta del Estudiante', on_delete=models.PROTECT)

    def __str__(self):
        return 'Estudiante: {} - Pregunta: {}, {} - Respondió: {}'.format(self.estudiante.nombres(),
                                                                          self.relacionar_concepto.opcion(),
                                                                          self.relacionar_concepto.respuesta_opcion(),
                                                                          self.respuesta_estudiante.opcion)

    class Meta:
        verbose_name = 'Calificacion Relacionar Concepto'