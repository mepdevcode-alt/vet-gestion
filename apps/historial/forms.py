from django import forms
from .models import ConsultaMedica

INPUT_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition'
TEXTAREA_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition resize-none'


class FormularioConsulta(forms.ModelForm):
    class Meta:
        model = ConsultaMedica
        fields = ['motivo', 'diagnostico', 'tratamiento', 'observaciones']
        labels = {
            'motivo': 'Motivo de consulta',
            'diagnostico': 'Diagnóstico',
            'tratamiento': 'Tratamiento',
            'observaciones': 'Observaciones adicionales',
        }
        widgets = {
            'motivo': forms.TextInput(attrs={'class': INPUT_CSS}),
            'diagnostico': forms.Textarea(attrs={'class': TEXTAREA_CSS, 'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'class': TEXTAREA_CSS, 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': TEXTAREA_CSS, 'rows': 3}),
        }
