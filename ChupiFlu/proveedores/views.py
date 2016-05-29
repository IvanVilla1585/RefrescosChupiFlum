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

from .models import Proveedore
from .mixins import JSONResponseMixin
from django.http import JsonResponse


class ListarProveedores(ListView):
    model = Proveedore




class EliminarProveedor(JSONResponseMixin, DeleteView):
    model = Proveedore
    slug_field = 'nit'
    slug_url_kwarg = 'nit'
    template_name_suffix = '_list'
    success_url = reverse_lazy('proveedores:listar')



class CrearProveedor(CreateView):
    model = Proveedore
    success_url = reverse_lazy('proveedores:listar')
    fields = ['nit', 'nombre_empresa', 'direccion', 'telefono', 'fax', 'correo_empresa', 'nombre_contacto',
              'apellido_contacto', 'telefono_contacto', 'correo_contacto']


class ActualizarProveedor(UpdateView):
    model = Proveedore
    success_url = reverse_lazy('proveedores:listar')
    fields = ['nombre_empresa', 'direccion', 'telefono', 'fax', 'correo_empresa', 'nombre_contacto',
              'apellido_contacto', 'telefono_contacto', 'correo_contacto']


class ConsultarProveedor(JSONResponseMixin, DetailView):
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
                'nombre_empresa': self.object.nombre_empresa,
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


@login_required()
def proveedoresView(request):
    form = ProveedoreForm()
    template = loader.get_template('proveedores/proveedore_form.html')
    contex = {
        'form': form
    }
    return HttpResponse(template.render(contex, request))
