from .models import CategoriaMateriaPrima
from rest_framework import serializers

class CategoriaMateriaPrimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaMateriaPrima
        fields = ('id', 'nombre',)
