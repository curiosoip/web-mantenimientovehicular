# apps/vehiculos/forms.py
from django import forms
from .models import Vehiculo, AsignacionVehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            "departamento",
            "placa",
            "marca",
            "modelo",
            "anio",
            "numero_motor",
            "numero_chasis",
            "estado",
        ]


class AsignacionVehiculoForm(forms.ModelForm):
    class Meta:
        model = AsignacionVehiculo
        fields = [
            "vehiculo",
            "chofer",
            "fecha_inicio",
            "fecha_fin",
        ]
