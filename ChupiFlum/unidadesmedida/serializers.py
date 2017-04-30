from .models import UnidadMedida
from rest_framework import serializers

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = ('id', 'nombre', 'equivalencia', 'code', 'descripcion', 'estado',)
