from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Muestra input tipo password

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'rol']
