from django.shortcuts import render
import json
from django.core import serializers
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.views.generic import ListView
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
from .forms import ProductoTerminadoForm
from .models import ProductoTerminado
from proveedores.mixins import JSONResponseMixin
from loginusers.mixins import LoginRequiredMixin

class CrearProducto(LoginRequiredMixin, CreateView):
    model = ProductoTerminado
    success_url = reverse_lazy('productos:listar')
    form_class = ProductoTerminadoForm

class ListarProductos(LoginRequiredMixin, ListView):
    model = ProductoTerminado

class ModificarProducto(LoginRequiredMixin, UpdateView):
    model = ProductoTerminado
    form_class = ProductoTerminadoForm
    success_url = reverse_lazy('productos:listar')

class EliminarProducto(LoginRequiredMixin, DeleteView):
    model = ProductoTerminado
    slug_field = 'nombre'
    slug_url_kwarg = 'nombre'
    success_url = reverse_lazy('productos:listar')

class ConsultarProducto(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = ProductoTerminado
    slug_field = 'nombre'
    slug_url_kwarg = 'nombre'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        data = {
            'producto':{
                'id': self.object.id,
                'nombre': self.object.nombre,
                'descripcion': self.object.descripcion,
                'categoria': self.object.categoria.id,
                'costo_produccion': self.object.costo_produccion,
                'precio_venta': self.object.precio_venta ,
                'cantidad': self.object.cantidad
            }
        }
        return data

class ProductoTerminadoView(LoginRequiredMixin, TemplateView):
    template_name = 'productos/productoterminado_form.html'


    def get_context_data(self, **kwargs):
        context = super(ProductoTerminadoView, self).get_context_data(**kwargs)
        context.update({'form': ProductoTerminadoForm()})

        return context
