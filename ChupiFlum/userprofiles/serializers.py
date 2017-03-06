from django.contrib.auth.models import (
    Permission,
    ContentType,
    User
)
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
