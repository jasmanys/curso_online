from django import forms

from evaluacion.models import EnunciadoEvaluacion


class EnunciadoEvaluacionForm(forms.ModelForm):
    class Meta:
        model = EnunciadoEvaluacion
        fields = '__all__'
        widgets = {
            'evaluacion': forms.HiddenInput(),
            'enunciado': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tipo_respuesta': forms.Select(attrs={'style': "cursor:pointer;", 'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'style': "cursor:pointer;", 'class': "form-control pb-5 pt-3"}),
            'submodulo': forms.HiddenInput()
        }