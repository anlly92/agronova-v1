from django import forms
from .models import Proceso

class Agricolaform(forms.ModelForm):
    class Meta:
        model = Proceso
        fields = ['id_lote', 'id_empleado', 'descripcion', 'id_inventario', 'cantidad', 'fecha']

class Procesoform(forms.ModelForm):
    class Meta:
        model = Proceso
        fields = ['id_empleado', 'tipo_producto', 'descripcion', 'cantidad', 'fecha']