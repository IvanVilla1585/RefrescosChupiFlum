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
        typelist = self.request.GET.get('typelist', None)
        if search:
            queryset = self.model.objects.filter(Q(nombre__icontains=search) | Q(code__icontains=search))
        elif typelist:
            queryset = super(UnidadMedidaViewSet, self).get_queryset()
        else:
            queryset = self.model.objects.filter(estado=True)

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

    def list(self, request, *args, **kwargs):
        typelist = self.request.GET.get('typelist', None)
        queryset = self.filter_queryset(self.get_queryset())
        print typelist
        page = self.paginate_queryset(queryset)
        if typelist is not None and page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
