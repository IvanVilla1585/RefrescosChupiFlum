from .models import Proceso
from maquina.models import Maquina
from rest_framework import serializers
from maquina.serializer import MaquinaSerializer

class ProcesoSerializer(serializers.ModelSerializer):
    maquina = MaquinaSerializer(read_only=True)
    maquina_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Maquina.objects.all(), source='maquina')
    class Meta:
        model = Proceso
        fields = ('id', 'nombre', 'descripcion', 'maquina', 'maquina_id', 'tiempo', 'estado',)
