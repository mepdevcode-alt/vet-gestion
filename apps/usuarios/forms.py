from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario

INPUT_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition'
SELECT_CSS = 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 transition bg-white'


class FormularioLogin(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': INPUT_CSS, 'placeholder': 'Nombre de usuario'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': INPUT_CSS, 'placeholder': '••••••••'}),
    )


class FormularioCrearDueno(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': INPUT_CSS}),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': INPUT_CSS}),
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': INPUT_CSS}),
            'first_name': forms.TextInput(attrs={'class': INPUT_CSS}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CSS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CSS}),
            'telefono': forms.TextInput(attrs={'class': INPUT_CSS}),
        }

    def clean(self):
        datos = super().clean()
        if datos.get('password1') != datos.get('password2'):
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return datos

    def save(self, commit: bool = True) -> Usuario:
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password1'])
        usuario.rol = Usuario.ROL_DUENO
        if commit:
            usuario.save()
        return usuario
