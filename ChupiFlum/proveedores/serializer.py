from .models import Proveedore
from rest_framework import serializers

class ProveedoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedore
        fields = ('id', 'nit', 'empresa', 'direccion', 'telefono', 'fax', 'correo_empresa', 'nombre_contacto', 'apellido_contacto', 'telefono_contacto', 'correo_contacto', 'estado',)