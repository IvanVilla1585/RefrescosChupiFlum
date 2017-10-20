# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializer import ProveedoreSerializer
from .models import Proveedore
from django.contrib import admin
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from oauth2_provider.ext.rest_framework import (TokenHasReadWriteScope, TokenHasScope, IsAuthenticatedOrTokenHasScope)

class ProveedoresViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    model = Proveedore
    queryset = model.objects.all()
    serializer_class = ProveedoreSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        typelist = self.request.GET.get('typelist', None)
        if search:
            queryset = self.model.objects.filter(Q(nombre__icontains=search) | Q(code__icontains=search))
        elif typelist:
            queryset = super(ProveedoresViewSet, self).get_queryset()
        else:
            queryset = self.model.objects.filter(estado=True)

        return queryset

    def destroy(self, request, *args, **kwargs):
        id = self.kwargs[self.lookup_field]
        proveedor = None
        if id:
            try:
                proveedor = self.model.objects.get(id=id)
                proveedor.estado = not proveedor.estado
                proveedor.save()
            except Proveedore.DoesNotExist as e:
                return Response({'message': 'El proveedor no existe'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'El id es obligatorio'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(proveedor)
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
