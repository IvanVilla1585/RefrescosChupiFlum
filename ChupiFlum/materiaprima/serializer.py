from .models import MateriaPrima
from categoriasmateriaprima.serializer import CategoriaMateriaPrimaSerializer
from categoriasmateriaprima.models import CategoriaMateriaPrima
from rest_framework import serializers
from unidadesmedida.serializers import UnidadMedidaSerializer
from unidadesmedida.models import UnidadMedida

class MateriaPrimaSerializer(serializers.ModelSerializer):
    categoria = CategoriaMateriaPrimaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CategoriaMateriaPrima.objects.all(), source='categoria')
    unidad_medida = UnidadMedidaSerializer(read_only=True)
    unidad_medida_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UnidadMedida.objects.all(), source='unidad_medida')
    class Meta:
        model = MateriaPrima
        fields = ('id', 'nombre', 'descripcion', 'unidad_medida', 'unidad_medida_id', 'categoria', 'categoria_id', 'cantidad', 'stock', 'estado',)
