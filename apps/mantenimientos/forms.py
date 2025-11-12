from django import forms
from .models import SolicitudMantenimiento, OrdenServicio

class SolicitudMantenimientoForm(forms.ModelForm):
    class Meta:
        model = SolicitudMantenimiento
        fields = [
            'vehiculo',
            'descripcion',
            'tipo',
            'estado',
        ]


class OrdenServicioForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = [
            'solicitud',
            'proveedor',
            'costo_mano_obra',
            'costo_aceites',
        ]
