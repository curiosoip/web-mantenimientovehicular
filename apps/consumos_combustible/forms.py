from django import forms
from .models import ConsumoCombustible

class ConsumoCombustibleForm(forms.ModelForm):
    class Meta:
        model = ConsumoCombustible
        fields = [
            'vehiculo',
            'bitacora',
            'chofer',
            'fecha',
            'litros',
            'costo',
            'estacion',
        ]
