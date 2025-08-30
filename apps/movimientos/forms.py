from django import forms
from .models import MovimientoRepuesto

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoRepuesto
        fields = ['repuesto', 'vehiculo', 'accion', 'cantidad', 'fecha','usuario']  # Sin usuario
