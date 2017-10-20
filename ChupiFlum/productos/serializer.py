from .models import (
    ProductoTerminado,
    Detalles_Formulas,
    Procesos_Formulas,
)
from proceso.models import Proceso
from categorias.models import Categoria
from categorias.serializer import CategoriaSerializer
from materiaprima.serializer import MateriaPrimaSerializer
from materiaprima.models import MateriaPrima
from presentaciones.models import Presentacion
from rest_framework import serializers

class DetalleFormulaSerializer(serializers.ModelSerializer):
    materia_prima = MateriaPrimaSerializer(read_only=True)
    materia_prima_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=MateriaPrima.objects.all(), source='materia_prima')
    class Meta:
        model = Detalles_Formulas
        fields = (
          'materia_prima_id', 'materia_prima', 'cantidad',
        )

class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = ('id', 'nombre', 'tiempo',)

class PresentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentacion
        fields = ('id', 'nombre',)

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Categoria.objects.all(), source="categoria")
    presentacion = PresentacionSerializer(read_only=True)
    presentacion_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Presentacion.objects.all(), source="presentacion")
    proceso = ProcesoSerializer(many=True)
    class Meta:
        model = ProductoTerminado
        fields = (
          'id', 'nombre', 'descripcion', 'categoria', 'categoria_id', 'presentacion', 'presentacion_id', 'costo_produccion', 'precio_venta',
          'cantidad', 'stock', 'proceso', 'materia_prima', 'estado'
        )  

    def create(self, validated_data):
        ##raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        print(dir(ProductoSerializer.Meta.model))
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            procesos = validated_data.pop('proceso')
            instance = ModelClass.objects.create(**validated_data)
            instance.proceso = procesos
        except TypeError as exc:
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception text was: %s.' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    exc
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                setattr(instance, field_name, value)

        return instance    