from django.shortcuts import render
import json
from django.core import serializers
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import ProveedoreForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic import TemplateView

from .models import Proveedore
from .mixins import JSONResponseMixin
from django.http import JsonResponse
from loginusers.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class ListarProveedores(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = Proveedore
    template_name = 'proveedore_list.html'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        data = [{
            'id': proveedor.id,
            'value': proveedor.empresa,
        } for proveedor in self.object_list]

        return data

    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(empresa__icontains=nom)
        else:
            queryset = super(ListarProveedores, self).get_queryset()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListarProveedores, self).get_context_data(**kwargs)
        context.update({'title': 'Proveedores'})

        return context


class EliminarProveedor(LoginRequiredMixin, DeleteView):
    model = Proveedore
    slug_field = 'nit'
    slug_url_kwarg = 'nit'
    success_url = reverse_lazy('proveedores:listar')

def eliminarProveedorAjax(request, nit):
    proveedor = Proveedore.objects.get(nit=nit)
    proveedor.estado = 'FALSE'

    proveedor.save()
    import ipdb; ipdb.set_trace()
    form = ProveedoreForm()

    template = loader.get_template('proveedores/proveedore_form.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))




class CrearProveedor(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Proveedore
    form_class = ProveedoreForm
    success_url = reverse_lazy('proveedores:crear')
    success_message = 'El proveedor %(empresa)s fue registrado en el sistema.'


class ActualizarProveedor(LoginRequiredMixin, UpdateView):
    model = Proveedore
    success_url = reverse_lazy('proveedores:listar')
    slug_field = 'nit'
    slug_url_kwarg = 'nit'
    form_class = ProveedoreForm



class ConsultarProveedor(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = Proveedore
    slug_field = 'nit'
    slug_url_kwarg = 'nit'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        data = {
            'proveedor':{
                'nit': self.object.nit,
                'nombre_empresa': self.object.empresa,
                'direccion': self.object.direccion,
                'telefono': self.object.telefono,
                'fax': self.object.fax ,
                'correo_empresa': self.object.correo_empresa ,
                'nombre_contacto': self.object.nombre_contacto,
                'apellido_contacto': self.object.apellido_contacto,
                'telefono_contacto': self.object.telefono_contacto,
                'correo_contacto': self.object.correo_contacto
            }
        }
        return data


class ProveedoresView(LoginRequiredMixin, TemplateView):
    template_name = 'proveedores/proveedore_form.html'


    def get_context_data(self, **kwargs):
        context = super(ProveedoresView, self).get_context_data(**kwargs)
        context.update({'form': ProveedoreForm(), 'title': 'Proveedores'})

        return context
