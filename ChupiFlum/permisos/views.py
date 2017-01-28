from django.shortcuts import render
from rest_framework import viewsets
from .serializers import (
    ContentTypeSerializer,
    PermisosSerializer
)
from django.contrib.auth.models import Permission

class PermisosViewSet(viewsets.ModelViewSet):
    model = Permission
    queryset = Permission.objects.all()
    serializer_class = PermisosSerializer
