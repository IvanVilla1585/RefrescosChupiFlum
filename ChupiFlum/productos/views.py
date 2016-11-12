from django.shortcuts import render
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
from .forms import ProductoTerminadoForm
from .models import ProductoTerminado
from proveedores.mixins import JSONResponseMixin
from loginusers.mixins import LoginRequiredMixin

class CrearProducto(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProductoTerminado
    success_url = reverse_lazy('productos:producto')
    form_class = ProductoTerminadoForm
    success_message = 'El producto %(nombre)s se registro en el sistema'

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
        data = {
            'producto':{
                'id': self.object.id,
                'nombre': self.object.nombre,
                'descripcion': self.object.descripcion,
                'categoria': self.object.categoria.id,
                'costo_produccion': self.object.costo_produccion,
                'precio_venta': self.object.precio_venta ,
                'cantidad': self.object.cantidad,
                'estado': self.object.estado
            }
        }
        return data

class ProductoTerminadoView(LoginRequiredMixin, TemplateView):
    template_name = 'productos/productoterminado_form.html'


    def get_context_data(self, **kwargs):
        context = super(ProductoTerminadoView, self).get_context_data(**kwargs)
        context.update({'form': ProductoTerminadoForm(), 'title': 'Productos Terminados'})

        return context
