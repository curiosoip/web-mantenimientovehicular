from django import forms
from .models import Cardex, RegistroCardex

class CardexForm(forms.ModelForm):
    class Meta:
        model = Cardex
        fields = [
            'vehiculo',
        ]


class RegistroCardexForm(forms.ModelForm):
    class Meta:
        model = RegistroCardex
        fields = [
            'cardex',
            'fecha',
            'tipo',
            'descripcion',
            'documento_respaldo',
        ]
