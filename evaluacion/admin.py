from django.contrib import admin
from evaluacion.models import *

admin.site.register(Evaluacion)
admin.site.register(EnunciadoEvaluacion)
admin.site.register(OpcionEnunciado)
admin.site.register(SeleccionMultiple)
admin.site.register(RelacionarConcepto)
admin.site.register(EstudianteEvaluacion)
admin.site.register(DetalleEstudianteEvaluacion)
admin.site.register(CalificacionSeleccionMultiple)
admin.site.register(CalificacionRelacionarConcepto)