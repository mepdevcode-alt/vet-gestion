from django import forms
from .models import Turno
from apps.mascotas.models import Mascota
from apps.usuarios.models import Usuario

INPUT_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition'
SELECT_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition bg-white'
TEXTAREA_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition resize-none'


class FormularioSolicitarTurno(forms.ModelForm):
    """Formulario para que el Dueño solicite un turno."""

    class Meta:
        model = Turno
        fields = ['mascota', 'fecha_hora', 'motivo']
        labels = {
            'mascota': 'Mascota',
            'fecha_hora': 'Fecha y hora',
            'motivo': 'Motivo de la consulta',
        }
        widgets = {
            'mascota': forms.Select(attrs={'class': SELECT_CSS}),
            'fecha_hora': forms.DateTimeInput(attrs={'class': INPUT_CSS, 'type': 'datetime-local'}),
            'motivo': forms.TextInput(attrs={'class': INPUT_CSS}),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario and usuario.es_dueno():
            self.fields['mascota'].queryset = Mascota.objects.filter(dueno=usuario)
        else:
            self.fields['mascota'].queryset = Mascota.objects.all()


class FormularioGestionarTurno(forms.ModelForm):
    """Formulario para que Admin/Recepcionista apruebe/rechace y asigne veterinario."""

    class Meta:
        model = Turno
        fields = ['veterinario', 'notas_recepcion']
        labels = {
            'veterinario': 'Veterinario asignado',
            'notas_recepcion': 'Notas de recepción',
        }
        widgets = {
            'veterinario': forms.Select(attrs={'class': SELECT_CSS}),
            'notas_recepcion': forms.Textarea(attrs={'class': TEXTAREA_CSS, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veterinario'].queryset = Usuario.objects.filter(rol=Usuario.ROL_VETERINARIO)
        self.fields['veterinario'].required = False
