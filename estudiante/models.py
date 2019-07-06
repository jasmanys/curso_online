from django.contrib.auth.models import User
from django.db import models

class Estudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)#incluye username, password, nombre, apellido y email
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    celular = models.CharField(verbose_name='Celular', max_length=15, unique=True,
        error_messages={
            'unique': "El numero de celular ya está registrado.",
        })
    cedula = models.CharField(verbose_name='Cédula', max_length=10, unique=True,
        error_messages={
            'unique': "El numero de cédula ya está registrado.",
        })

    def nombres(self):
        return '{}'.format(self.usuario.first_name + ' ' + self.usuario.last_name)

    def __str__(self):
        return 'Nombres: {} - e-mail: {} - Cedula: {} - Celular: {}'.format(self.nombres(), self.usuario.email, self.cedula,
                                                                                                      self.celular)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
