"""from django.shortcuts import render
import json
from django.core import serializers
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.views.generic import (
    ListView,
    View
)
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import (
    ProductoTerminadoForm,
    DetalleFormFormSet,
)
from .models import (
    ProductoTerminado,
    Detalles_Formulas
)
from proveedores.mixins import JSONResponseMixin
from loginusers.mixins import LoginRequiredMixin

class CrearProducto(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProductoTerminado
    success_url = reverse_lazy('productos:producto')
    form_class = ProductoTerminadoForm
    success_message = 'El producto %(nombre)s se registro en el sistema'

    def get(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_formula = DetalleFormFormSet()
        return self.render_to_response(self.get_context_data(form=form, detalle_formula=detalle_formula,))

    def post(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_formula = DetalleFormFormSet(self.request.POST)
        if (form.is_valid() and detalle_formula.is_valid()):
            return self.form_valid(form, detalle_formula)
        else:
            return self.form_invalid(form, detalle_formula)

    def form_valid(self, form, detalle_formula):

        self.object = form.save()
        detalle_formula.instance = self.object
        detalle_formula.save()
        formulas = Detalles_Formulas.objects.filter(id_producto=self.object.id)

        for formula in formulas:
            formula.cantidad = formula.cantidad * formula.id_materia_prima.unidad_medida.equivalencia
            formula.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, detalle_formula):

        return self.render_to_response(self.get_context_data(form=form, detalle_formula=detalle_formula))


class ListarProductos(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = ProductoTerminado
    template_name = 'productoterminado_list.html'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        data = [{
            'id': producto.id,
            'value': producto.nombre,
        } for producto in self.object_list]

        return data


    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(nombre__icontains=nom)
        else:
            queryset = super(ListarProductos, self).get_queryset()

        return queryset

class ConsultarFormula(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = ProductoTerminado
    template_name = 'productoterminado_list.html'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        pedidos = self.request.GET.get('pedidos', None)
        if pedidos is None:
            data = {
                status: 400,
                message: 'Error al obtener los pedidos'
            }
        else:
            listPed = []
            pedidos = pedidos.replace('[', '')
            pedidos = pedidos.replace(']', '')
            array = pedidos.split(',')
            for id in array:
                listPed.append(int(id))

            data = [{
                'id': formula.id_producto.id,
                'materia': formula.id_producto.nombre,
                'producto': formula.id_materia_prima.nombre,
                'cantidad': formula.cantidad / formula.id_materia_prima.unidad_medida.equivalencia,
                'code': formula.id_materia_prima.unidad_medida.code,
            } for formula in Detalles_Formulas.objects.filter(id_producto__in=listPed)]
        return data

class ModificarProducto(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ProductoTerminado
    form_class = ProductoTerminadoForm
    success_url = reverse_lazy('productos:producto')
    slug_field = 'id'
    slug_url_kwarg = 'id'
    success_message = 'Los datos del producto %(nombre)s fueron actualizados'

class ActualizarEstadoView(JSONResponseMixin, View):
    object = None
    relacion = None
    def post(self, request):
        id = self.request.POST.get('id', None)
        producto = None
        try:
            producto = ProductoTerminado.objects.get(id=id)
        except ProductoTerminado.DoesNotExist as e:
            self.object = producto
        if producto is not None:
            producto.estado = False
            producto.save()
            self.object = producto
        return self.render_to_json_response()

    def get_data(self):
        if self.object is not None:
            data = {
                'message': 'Se inhabilito el producto',
            }
        else:
            data = {
                'message': 'Este producto se encuentra asociado a procesos'
            }

        return data

class ConsultarProducto(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = ProductoTerminado
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()

    def get_data(self):

        detalle_form = Detalles_Formulas.objects.filter(id_producto=self.object.id)

        data = {
            'producto':{
                'id': self.object.id,
                'nombre': self.object.nombre,
                'descripcion': self.object.descripcion,
                'categoria': self.object.categoria.id,
                'costo_produccion': self.object.costo_produccion,
                'precio_venta': self.object.precio_venta ,
                'cantidad': self.object.cantidad,
                'cantidad_productos': self.object.cantidad_productos,
                'prsentacion': self.object.presentacion.id,
                'stock': self.object.stock,
                'estado': self.object.estado,
                'formula': [{
                    'id': form.id_materia_prima.id,
                    'cantidad': (form.cantidad/form.id_materia_prima.unidad_medida.equivalencia),
                } for form in detalle_form]
            }
        }

        return data

class ProductoTerminadoView(LoginRequiredMixin, TemplateView):

    template_name = 'productos/productoterminado_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProductoTerminadoView, self).get_context_data(**kwargs)
        detalle_formula = DetalleFormFormSet()
        context.update({'form': ProductoTerminadoForm(), 'detalle_formula': detalle_formula })

        return context

"""
# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializer import ProductoSerializer
from .models import ProductoTerminado
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
    model = ProductoTerminado
    queryset = model.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search:
            queryset = self.model.objects.filter(Q(nombre__icontains=search))
        else:
            queryset = super(ProveedoresViewSet, self).get_queryset()

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