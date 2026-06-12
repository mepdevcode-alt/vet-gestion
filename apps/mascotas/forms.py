from django import forms
from .models import Mascota
from apps.usuarios.models import Usuario

INPUT_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition'
SELECT_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition bg-white'


class FormularioMascota(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'foto', 'peso', 'dueno']
        labels = {
            'nombre': 'Nombre',
            'especie': 'Especie',
            'raza': 'Raza',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'foto': 'Foto',
            'peso': 'Peso (kg)',
            'dueno': 'Dueño',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': INPUT_CSS}),
            'especie': forms.Select(attrs={'class': SELECT_CSS}),
            'raza': forms.TextInput(attrs={'class': INPUT_CSS}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': INPUT_CSS, 'type': 'date'}),
            'peso': forms.NumberInput(attrs={'class': INPUT_CSS, 'step': '0.01'}),
            'dueno': forms.Select(attrs={'class': SELECT_CSS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dueno'].queryset = Usuario.objects.filter(rol=Usuario.ROL_DUENO).order_by('last_name', 'first_name')
        self.fields['foto'].required = False
