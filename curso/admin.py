from django.contrib import admin

# Register your models here.
from curso.models import *

admin.site.register(Curso)
admin.site.register(EstudianteCurso)
admin.site.register(Recurso)
admin.site.register(Item)
admin.site.register(RecursoItem)
admin.site.register(Modulo)
admin.site.register(AnteModulo)
admin.site.register(Foto)
admin.site.register(Video)
admin.site.register(Audio)
admin.site.register(SubModulo)
admin.site.register(FotoSubModulo)
admin.site.register(VideoSubModulo)
admin.site.register(AudioSubModulo)