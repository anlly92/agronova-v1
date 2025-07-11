from django import forms
from .models import IngresosEgresos

class IngresosEgresosform(forms.ModelForm):
    class Meta:
        model = IngresosEgresos
        fields = '__all__'