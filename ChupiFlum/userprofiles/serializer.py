from django.contrib.auth.models import (
    Group,
    User
)
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password', 'groups', 'is_active',)
