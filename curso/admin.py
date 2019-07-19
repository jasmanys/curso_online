from django.contrib import admin

# Register your models here.
from curso.models import *

admin.site.register(Curso)
admin.site.register(Modulo)
admin.site.register(SubModulo)
admin.site.register(EstudianteCurso)
#admin.site.register(Recurso)
#admin.site.register(Item)
#admin.site.register(RecursoItem)