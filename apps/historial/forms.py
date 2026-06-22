from django import forms
from .models import ConsultaMedica, HistoriaClinica

INPUT_CSS    = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition'
TEXTAREA_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition resize-none'

HC_INPUT    = 'w-full px-3 py-2 border border-sky-200 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 transition text-sm bg-white'
HC_TEXTAREA = 'w-full px-3 py-2 border border-sky-200 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 transition text-sm resize-none bg-white'
HC_SELECT   = 'w-full px-3 py-2 border border-sky-200 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-400 transition text-sm bg-white'


class FormularioHistoriaClinica(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        exclude = ['numero_hc', 'creado_por', 'fecha_creacion', 'fecha_actualizacion']
        widgets = {
            # Metadatos
            'mascota': forms.Select(attrs={'class': HC_SELECT}),
            'estado':  forms.Select(attrs={'class': HC_SELECT}),
            # Sección 1
            'propietario_nombre':    forms.TextInput(attrs={'class': HC_INPUT}),
            'propietario_documento': forms.TextInput(attrs={'class': HC_INPUT}),
            'propietario_direccion': forms.TextInput(attrs={'class': HC_INPUT}),
            'propietario_telefono':  forms.TextInput(attrs={'class': HC_INPUT}),
            'propietario_email':     forms.EmailInput(attrs={'class': HC_INPUT}),
            # Sección 2
            'paciente_sexo':               forms.Select(attrs={'class': HC_SELECT}),
            'paciente_color_pelaje':       forms.TextInput(attrs={'class': HC_INPUT}),
            'paciente_microchip':          forms.TextInput(attrs={'class': HC_INPUT}),
            'paciente_procedencia':        forms.TextInput(attrs={'class': HC_INPUT}),
            'paciente_fin_zootecnico':     forms.TextInput(attrs={'class': HC_INPUT}),
            'paciente_senas_particulares': forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            # Sección 3
            'motivo_consulta':         forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 3}),
            'dieta':                   forms.TextInput(attrs={'class': HC_INPUT}),
            'enfermedades_previas':    forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            'medicacion_actual':       forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            'cirugias_previas':        forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            'vacunacion':              forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            'desparasitacion':         forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            'partos':                  forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            'observaciones_anamnesis': forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            # Sección 4
            'temperatura':             forms.NumberInput(attrs={'class': HC_INPUT, 'step': '0.1'}),
            'frecuencia_cardiaca':     forms.NumberInput(attrs={'class': HC_INPUT}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': HC_INPUT}),
            'peso_actual':             forms.NumberInput(attrs={'class': HC_INPUT, 'step': '0.01'}),
            'diagnostico_presuntivo':  forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            'diagnostico_definitivo':  forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 3}),
            'tratamiento':             forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 3}),
            'medicacion_prescrita':    forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            'observaciones_clinicas':  forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 2}),
            # Sección 5
            'proxima_visita':           forms.DateInput(attrs={'class': HC_INPUT, 'type': 'date'}),
            'evolucion':                forms.Textarea(attrs={'class': HC_TEXTAREA, 'rows': 3}),
            'veterinario_responsable':  forms.Select(attrs={'class': HC_SELECT}),
        }


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
