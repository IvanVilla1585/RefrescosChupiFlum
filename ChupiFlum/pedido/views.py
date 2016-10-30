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
from .forms import PedidoForm
from .models import Pedido
from .models import Detalle_Pedido
from estado_orden.models import EstadosOrdenes
from materiaprima.models import MateriaPrima
from proveedores.mixins import JSONResponseMixin
from loginusers.mixins import LoginRequiredMixin
from decimal import Decimal
import ast

class PedidoView(LoginRequiredMixin, TemplateView):
    template_name = 'pedido/pedido_form.html'

    def get_context_data(self, **kwargs):
        context = super(PedidoView, self).get_context_data(**kwargs)
        context.update({'form': PedidoForm(), 'title': 'Pedidos'})
        return context

class CrearPedido(LoginRequiredMixin, CreateView):
    model = Pedido
    success_url = reverse_lazy('pedidos:pedidosForm')
    form_class = PedidoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        estado = EstadosOrdenes.objects.get(id=1)
        self.object.id_etado = estado
        self.object.save()
        pedido = self.model.objects.get(id=self.object.id)
        productos = ast.literal_eval(self.request.POST.get('productos', None))
        for producto in productos:
            materia = MateriaPrima.objects.get(id=producto['productoId'])
            materia.cantidad = materia.cantidad + producto['cantidad']
            materia.save()
            detalle = Detalle_Pedido.objects.create(id_pedido=pedido, id_materia_prima=materia, cantidad=producto['cantidad'], valor_unitario=Decimal(producto['valor']))
        return super(CrearPedido, self).form_valid(form)

class ListarPedido(LoginRequiredMixin, ListView):
    model = Pedido

    def get_context_data(self, **kwargs):
        context = super(ListarPedido, self).get_context_data(**kwargs)
        context.update({'title': 'Pedidos'})
        return context

class ModificarPedido(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = Pedido
    success_url = reverse_lazy('productos:listar')

class EliminarPedido(LoginRequiredMixin, DeleteView):
    model = Pedido
    slug_field = 'nombre'
    slug_url_kwarg = 'nombre'
    success_url = reverse_lazy('productos:listar')

class ConsultarPedido(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = Pedido
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
