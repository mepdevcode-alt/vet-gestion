from django import forms
from .models import Turno
from apps.mascotas.models import Mascota
from apps.usuarios.models import Usuario

INPUT_CSS    = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition'
SELECT_CSS   = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition bg-white'
TEXTAREA_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition resize-none'


class FormularioSolicitarTurno(forms.ModelForm):

    class Meta:
        model = Turno
        fields = ['mascota', 'veterinario', 'tipo_consulta', 'fecha_hora', 'motivo']
        labels = {
            'mascota':       'Mascota',
            'veterinario':   'Veterinario',
            'tipo_consulta': 'Tipo de consulta',
            'fecha_hora':    'Fecha y hora',
            'motivo':        'Motivo de la consulta',
        }
        widgets = {
            'mascota':       forms.Select(attrs={'class': SELECT_CSS}),
            'veterinario':   forms.Select(attrs={'class': SELECT_CSS}),
            'tipo_consulta': forms.Select(attrs={'class': SELECT_CSS}),
            'fecha_hora':    forms.DateTimeInput(attrs={'class': INPUT_CSS, 'type': 'datetime-local'}),
            'motivo':        forms.TextInput(attrs={'class': INPUT_CSS, 'placeholder': 'Describí brevemente el motivo de la consulta'}),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario and usuario.es_dueno():
            self.fields['mascota'].queryset = Mascota.objects.filter(dueno=usuario)
        else:
            self.fields['mascota'].queryset = Mascota.objects.all()
        self.fields['veterinario'].queryset = Usuario.objects.filter(rol=Usuario.ROL_VETERINARIO)
        self.fields['veterinario'].required = False


class FormularioRechazarTurno(forms.Form):
    motivo_rechazo = forms.CharField(
        label='Motivo de rechazo',
        widget=forms.Textarea(attrs={
            'class': TEXTAREA_CSS,
            'rows': 3,
            'placeholder': 'Indicá el motivo por el que se rechaza el turno',
        }),
    )


class FormularioCancelarTurno(forms.Form):
    motivo_cancelacion = forms.CharField(
        label='Motivo de cancelación',
        widget=forms.Textarea(attrs={
            'class': TEXTAREA_CSS,
            'rows': 3,
            'placeholder': 'Indicá el motivo por el que se cancela el turno',
        }),
    )
