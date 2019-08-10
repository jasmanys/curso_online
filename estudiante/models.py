from django.contrib.auth.models import User
from django.db import models
from django.db.models import CheckConstraint, Q
from django.db.models.functions import Length


class Estudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)#incluye username, password, nombre, apellido y email
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    celular = models.CharField(verbose_name='Celular', max_length=15, unique=True,
                                error_messages={
                                    'unique': "El numero de celular ya está registrado.",
                                    'celular_validar_length': "El numero de celular debe tener de 10 a 15 dígitos.",
                                }, help_text='De 10 a 15 números')
    cedula = models.CharField(verbose_name='Cédula', max_length=10, unique=True,
        error_messages={
            'unique': "El numero de cédula ya está registrado.",
            'cedula_validar_length': "La cédula debe contener 10 dígitos.",
        }, help_text='10 números')

    CheckConstraint(
        name='celular_validar_length',
        check= Q(Length('celular') in range(10,16))
    )
    CheckConstraint(
        name='cedula_validar_length',
        check=Q(Length('cedula') == 10)
    )

    def nombres(self):
        return '{}'.format(self.usuario.first_name + ' ' + self.usuario.last_name)

    def __str__(self):
        return 'Nombres: {} - e-mail: {} - Cedula: {} - Celular: {} - Username: {}'.format(self.nombres(), self.usuario.email, self.cedula,
                                                                                                      self.celular, self.usuario.username)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        """Para otro día
        constraints = [
            CheckConstraint(
                    name='celular_validar_length2',
                    check= Q(Length('celular') in range(10,16))
            ),
            CheckConstraint(
                name='cedula_validar_length2',
                check=Q(Length('cedula') == 10)
            )
        ]"""