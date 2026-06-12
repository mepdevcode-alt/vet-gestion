from django import forms
from django.forms import inlineformset_factory
from .models import Factura, ItemFactura

INPUT_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition'
TEXTAREA_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition resize-none'
SELECT_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition bg-white'


class FormularioFactura(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['notas']
        labels = {'notas': 'Notas adicionales'}
        widgets = {
            'notas': forms.Textarea(attrs={'class': TEXTAREA_CSS, 'rows': 3}),
        }


class FormularioItem(forms.ModelForm):
    class Meta:
        model = ItemFactura
        fields = ['descripcion', 'precio_unitario', 'cantidad']
        labels = {
            'descripcion': 'Descripción',
            'precio_unitario': 'Precio unitario ($)',
            'cantidad': 'Cantidad',
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': INPUT_CSS}),
            'precio_unitario': forms.NumberInput(attrs={'class': INPUT_CSS, 'step': '0.01', 'min': '0'}),
            'cantidad': forms.NumberInput(attrs={'class': INPUT_CSS, 'min': '1'}),
        }


ItemFormSet = inlineformset_factory(
    Factura,
    ItemFactura,
    form=FormularioItem,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class FormularioCambiarEstado(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['estado']
        labels = {'estado': 'Nuevo estado'}
        widgets = {
            'estado': forms.Select(attrs={'class': SELECT_CSS}),
        }
