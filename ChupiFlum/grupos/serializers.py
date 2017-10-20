from django.contrib.auth.models import (
    Group,
    Permission,
)
from rest_framework import serializers
from permisos.serializers import PermisosSerializer

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
    ##permission_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Permission.objects.all(), source='permissions')
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions',)
