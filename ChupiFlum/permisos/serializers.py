from django.contrib.auth.models import (
    Permission,
    ContentType,
)
from rest_framework import serializers

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('id', 'app_label', 'model',)

class PermisosSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer(many=False)
    class Meta:
        model = Permission
        fields = ('id', 'name', 'content_type', 'codename',)
