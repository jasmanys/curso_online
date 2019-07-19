from django import forms
from curso.models import Curso, SubModulo


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
            'descripcion': forms.Textarea(attrs={'class': 'form-control text-justify text-break', 'rows':4}),
            'comentario': forms.Textarea(attrs={'class': 'form-control text-justify text-break', 'rows':4}),
            'icono': forms.FileInput(attrs={'style':"cursor:pointer;", 'class': "form-control pb-5 pt-3"})
        }

class SubModuloForm(forms.ModelForm):
    class Meta:
        model = SubModulo
        fields = '__all__'
        widgets = {
            'numero': forms.HiddenInput(),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'modulo': forms.HiddenInput()
        }