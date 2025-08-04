from django import forms
from .models import IngresosEgresos,Ventas

class IngresosEgresosform(forms.ModelForm):
    class Meta:
        model = IngresosEgresos
        exclude = ['id_admin']

class VentasForm(forms.ModelForm):
    class Meta:
        model = Ventas
        exclude = ['id_admin']