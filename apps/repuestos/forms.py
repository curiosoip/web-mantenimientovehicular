from django import forms
from .models import Repuesto, RepuestoUsado, DevolucionRepuesto

class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = [
            'nombre',
            'descripcion',
            'codigo',
            'precio_unitario',
        ]


class RepuestoUsadoForm(forms.ModelForm):
    class Meta:
        model = RepuestoUsado
        fields = [
            'orden_servicio',
            'repuesto',
            'cantidad',
            'precio_unitario',
        ]


class DevolucionRepuestoForm(forms.ModelForm):
    class Meta:
        model = DevolucionRepuesto
        fields = [
            'orden_servicio',
            'repuesto',
            'cantidad',
            'observacion',
        ]
