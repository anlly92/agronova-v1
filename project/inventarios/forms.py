from django import forms
from .models import Inventario

class ProductoFinalform(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'descripcion', 'contenido', 'precio_unitario', 'stock', 'unidad','fecha_siembra']

class Arbustosform(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['tipo_arbusto', 'nombre', 'id_lote', 'stock', 'fecha_siembra', 'renovacion', 'nombre_lote', 'tala']

class Agroquimicosform(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'descripcion', 'stock', 'unidad', 'contenido']

class Herramientasform(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'estado', 'stock', 'categoria']
