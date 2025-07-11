from django import forms
from .models import Lote, Recoleccion, Pagos

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = '__all__' 

class RecoleccionForm(forms.ModelForm):
    class Meta:
        model = Recoleccion
        fields = '__all__'

class PagosForm(forms.ModelForm):
    class Meta:
        model = Pagos
        fields = '__all__'