from django import forms
from django.contrib.auth.models import User

from estudiante.models import Estudiante


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'pattern':"[a-z0-9@.+-_]{4,150}"}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control '}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'password': forms.PasswordInput(attrs={'class': "form-control"}),
        }

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ('fecha_nacimiento', 'celular', 'cedula')
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'pattern':"[0-9]{10,15}"}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'pattern':"[0-9]{10}"}),
        }