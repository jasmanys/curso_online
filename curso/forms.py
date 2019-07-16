from django import forms
from curso.models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        labels = {
            'nombre': 'Nombre del Curso',
            'descripcion': 'Descripción',
            'comentario': 'Comentario',
            'icono': 'Ícono'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Ej: Electricidad, Electrónica, etc."}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control text-justify text-break', 'rows':3}),
            'comentario': forms.Textarea(attrs={'class': 'form-control text-justify text-break', 'rows':3}),
            'icono': forms.FileInput(attrs={'style':"cursor:pointer;", 'class': "form-control pb-5 pt-3"})
        }