from django import forms
from .models import Mantenimiento

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ['vehiculo', 'tipo', 'estado', 'fecha_programada', 'fecha_realizado', 'descripcion']
