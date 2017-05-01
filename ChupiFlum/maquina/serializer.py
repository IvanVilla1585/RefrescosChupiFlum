from .models import Maquina
from unidadesmedida.models import UnidadMedida
from rest_framework import serializers
from unidadesmedida.serializers import UnidadMedidaSerializer

class MaquinaSerializer(serializers.ModelSerializer):
    unidad_medida = UnidadMedidaSerializer(read_only=True)
    unidad_medida_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UnidadMedida.objects.all(), source='unidad_medida')
    class Meta:
        model = Maquina
        fields = ('id', 'nombre', 'descripcion', 'capacidad', 'unidad_medida', 'unidad_medida_id', 'estado',)
