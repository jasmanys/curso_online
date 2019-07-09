from django.db import models
from django.db.models import Max

from estudiante.models import Estudiante

class Curso(models.Model):
    nombre = models.CharField(verbose_name='Nombre del Curso', max_length=50)
    descripcion = models.TextField(verbose_name='Descripción', max_length=600)
    comentario = models.TextField(verbose_name='Comentario', max_length=600)
    icono = models.TextField(verbose_name='Icono', max_length=600, blank=True, null=True)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class EstudianteCurso(models.Model):
    estudiante = models.ForeignKey(Estudiante, verbose_name='Elija al Estudiante', on_delete=models.PROTECT)
    cursos = models.ManyToManyField(Curso, verbose_name="Cursos")

    def __str__(self):
        return 'Estudiante: {}'.format(self.estudiante.nombres())

    class Meta:
        verbose_name = 'Estudiante del Curso'
        verbose_name_plural = 'Estudiantes del Curso'

class Recurso(models.Model):
    curso = models.ForeignKey(Curso, verbose_name="Curso", on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name='Descripcion', max_length=600)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

class Item(models.Model):
    descripcion = models.TextField(verbose_name='Descripción', max_length=600)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Item para Recurso'
        verbose_name_plural = 'Items para Recursos'

class RecursoItem(models.Model):
    titulo = models.CharField(verbose_name='Título', max_length=200)
    item = models.ManyToManyField(Item, verbose_name='Item')
    descripcion = models.TextField(verbose_name='Descripción', max_length=600)
    recurso = models.ForeignKey(Recurso, verbose_name='Recurso', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.titulo, self.item, self.descripcion, self.recurso)

    class Meta:
        verbose_name = 'Item de Recurso'
        verbose_name_plural = 'Items de Recursos'

class Modulo(models.Model):
    numero = models.IntegerField(verbose_name='Numero del Módulo')
    titulo = models.CharField(verbose_name='Título', max_length=200)
    curso = models.ForeignKey(Curso, verbose_name="Curso", on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - Curso: {}'.format(self.numero, self.titulo, self.curso)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ('numero',)

    def save(self, *args, **kwargs):
        if not self.id:
            if Modulo.objects.filter(curso__id = self.curso.id).exists():
                mod = Modulo.objects.filter(curso__id = self.curso.id).aggregate(max_numero = Max('numero'))
                self.numero = mod.get('max_numero') + 1
            else:
                self.numero = 1
        else:
            mod = Modulo.objects.get(id=self.id)
            self.numero = mod.numero
        super(Modulo, self).save(*args, **kwargs)

class AnteModulo(models.Model):
    numero = models.IntegerField(verbose_name='AnteMódulo')
    titulo = models.CharField(verbose_name='Título', max_length=200)
    modulo = models.ForeignKey(Modulo, verbose_name="Módulo", on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {}'.format(self.numero, self.titulo, self.modulo)

    class Meta:
        verbose_name = 'AnteMódulo'
        verbose_name_plural = 'AnteMódulos'
        ordering = ('numero',)

    def save(self, *args, **kwargs):
        if not self.id:
            if AnteModulo.objects.filter(modulo__id = self.modulo.id).exists():
                mod = AnteModulo.objects.filter(modulo__id = self.modulo.id).aggregate(max_numero = Max('numero'))
                self.numero = mod.get('max_numero') + 1
            else:
                self.numero = 1
        else:
            mod = AnteModulo.objects.get(id=self.id)
            self.numero = mod.numero
        super(AnteModulo, self).save(*args, **kwargs)

class Foto(models.Model):
    foto = models.TextField(verbose_name='Foto', max_length=600)

    def __str__(self):
        return self.foto

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'

class Video(models.Model):
    video = models.TextField(verbose_name='Link del vídeo en YouTube', max_length=600)

    def __str__(self):
        return self.video

    class Meta:
        verbose_name = 'Vídeo'
        verbose_name_plural = 'Vídeos'

class Audio(models.Model):
    audio = models.TextField(verbose_name='Audio', max_length=600)

    def __str__(self):
        return self.audio

    class Meta:
        verbose_name = 'Audio'
        verbose_name_plural = 'Audios'

class SubModulo(models.Model):
    numero = models.IntegerField(verbose_name='SubMódulo')
    titulo = models.CharField(verbose_name='Título', max_length=200)
    texto = models.TextField(verbose_name='Contenido', max_length=10000, blank=True)
    antemodulo = models.ForeignKey(AnteModulo, verbose_name="AnteModulo", on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.numero, self.titulo)

    class Meta:
        verbose_name = 'SubModulo'
        verbose_name_plural = 'SubModulos'

    def save(self, *args, **kwargs):
        if not self.id:
            if SubModulo.objects.filter(antemodulo__id = self.antemodulo.id).exists():
                mod = SubModulo.objects.filter(antemodulo__id = self.antemodulo.id).aggregate(max_numero = Max('numero'))
                self.numero = mod.get('max_numero') + 1
            else:
                self.numero = 1
        else:
            mod = SubModulo.objects.get(id=self.id)
            self.numero = mod.numero
        super(SubModulo, self).save(*args, **kwargs)

class FotoSubModulo(models.Model):
    sub_modulo = models.ForeignKey(SubModulo, on_delete=models.CASCADE)
    foto = models.ManyToManyField(Foto)

    def __str__(self):
        return self.sub_modulo.titulo

    class Meta:
        verbose_name = 'Foto de SubModulo'
        verbose_name_plural = 'Fotos de SubModulos'

class VideoSubModulo(models.Model):
    sub_modulo = models.ForeignKey(SubModulo, on_delete=models.CASCADE)
    video = models.ManyToManyField(Video)

    def __str__(self):
        return self.sub_modulo.titulo

    class Meta:
        verbose_name = 'Vídeo para SubModulo'
        verbose_name_plural = 'Vídeos para SubModulos'

class AudioSubModulo(models.Model):
    sub_modulo = models.ForeignKey(SubModulo, on_delete=models.CASCADE)
    audio = models.ManyToManyField(Audio)

    def __str__(self):
        return self.sub_modulo.titulo

    class Meta:
        verbose_name = 'Audio para SubModulo'
        verbose_name_plural = 'Audios para SubModulos'
