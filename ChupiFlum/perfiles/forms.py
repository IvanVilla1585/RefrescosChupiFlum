from django import forms
from .models import Perfil

class PerfilesForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
