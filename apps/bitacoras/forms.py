from django import forms
from .models import Bitacora

class BitacoraForm(forms.ModelForm):
    class Meta:
        model = Bitacora
        fields = [
            'vehiculo',
            'chofer',
            'fecha',
            'km_inicial',
            'km_final',
            'combustible_cargado',
            'costo_combustible',
            'observaciones',
            'foto_odometro_inicio',
            'foto_odometro_fin',
        ]
