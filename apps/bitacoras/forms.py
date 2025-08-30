# forms.py
from django import forms
from .models import BitacoraViaje

class BitacoraForm(forms.ModelForm):
    class Meta:
        model = BitacoraViaje
        fields = ['vehiculo', 'fecha', 'ruta', 'kilometros_recorridos', 'observaciones']  # sin 'conductor'
