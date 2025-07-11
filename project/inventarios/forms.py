from django import forms
from .models import Inventario

class ProductoFinalform(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'descripcion', 'contenido', 'precio_unitario', 'stock', 'unidad']

class Arbustosform(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['tipo_arbusto', 'nombre', 'id_lote', 'stock', 'fecha_siembra', 'renovacion']

class Agroquimicosform(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'descripcion', 'stock', 'unidad', 'contenido']

class Herramientasform(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'estado', 'stock']
