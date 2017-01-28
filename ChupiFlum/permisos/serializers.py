from django.contrib.auth.models import (
    Permission,
    ContentType,
)
from rest_framework import serializers

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('app_label', 'model',)

class PermisosSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer()
    class Meta:
        model = Permission
        fields = ('name', 'content_type', 'codename',)
