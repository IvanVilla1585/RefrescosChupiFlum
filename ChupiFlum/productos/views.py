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
