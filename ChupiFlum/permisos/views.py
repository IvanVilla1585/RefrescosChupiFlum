from django.shortcuts import render
from .serializers import (
    ContentTypeSerializer,
    PermisosSerializer
)
from django.contrib.auth.models import Permission
from django.contrib import admin
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from oauth2_provider.ext.rest_framework import (TokenHasReadWriteScope, TokenHasScope, IsAuthenticatedOrTokenHasScope)

class PermisosViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    model = Permission
    queryset = Permission.objects.all()
    serializer_class = PermisosSerializer
