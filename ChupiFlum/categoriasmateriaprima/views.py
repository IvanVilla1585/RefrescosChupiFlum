# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializer import CategoriaMateriaPrimaSerializer
from .models import CategoriaMateriaPrima
from django.contrib import admin
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from oauth2_provider.ext.rest_framework import (TokenHasReadWriteScope, TokenHasScope, IsAuthenticatedOrTokenHasScope)

class CategoriaMateriaPrimaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    model = CategoriaMateriaPrima
    queryset = model.objects.all()
    serializer_class = CategoriaMateriaPrimaSerializer
