from django import forms
from .models import Administrador

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        exclude = ['contraseña']

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['correo', 'telefono']