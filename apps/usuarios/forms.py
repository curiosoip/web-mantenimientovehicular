# apps/usuarios/forms.py
from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "rol",
            "departamento",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("El email es obligatorio")
        return email
