# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializers import UnidadMedidaSerializer
from .models import UnidadMedida
from django.contrib import admin
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from oauth2_provider.ext.rest_framework import (TokenHasReadWriteScope, TokenHasScope, IsAuthenticatedOrTokenHasScope)

class UnidadMedidaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    model = UnidadMedida
    queryset = model.objects.all()
    serializer_class = UnidadMedidaSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search:
            queryset = self.model.objects.filter(Q(nombre__icontains=search) | Q(code__icontains=search))
        else:
            queryset = super(UnidadMedidaViewSet, self).get_queryset()

        return queryset

    def destroy(self, request, *args, **kwargs):
        id = self.kwargs[self.lookup_field]
        unit = None
        if id:
            try:
                unit = self.model.objects.get(id=id)
                unit.estado = not unit.estado
                unit.save()
            except UnidadMedida.DoesNotExist as e:
                return Response({'message': 'La unidad de medida no existe'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'El id es obligatorio'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(unit)
        return Response(serializer.data, status=status.HTTP_200_OK)
