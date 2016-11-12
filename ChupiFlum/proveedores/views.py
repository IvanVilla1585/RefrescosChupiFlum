# -*- coding: utf-8 -*-
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
from django.views.generic import TemplateView

from .models import Proveedore
from .mixins import JSONResponseMixin
from django.http import JsonResponse
from loginusers.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class ListarProveedores(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = Proveedore
    template_name = 'proveedore_list.html'
    paginate_by = 6

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


class EliminarProveedor(LoginRequiredMixin, JSONResponseMixin, DeleteView):
    model = Proveedore
    success_url = reverse_lazy('proveedores:proveedor')

    def get_queryset(self):
        nit = self.request.POST.get('nit', None)
        id = self.request.POST.get('pk', None)
        if id:
            queryset = self.model.objects.get(id=id)
        else:
            queryset = super(EliminarProveedor, self).get_queryset()
        return queryset

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        return self.render_to_json_response()

    def get_data(self):

        data = {
            'message': 'Se cambio el estado del proveedor a inctivo',
        }

        return data

class ActualizarEstadoView(JSONResponseMixin, View):
  object = None
  def post(self, request):
    id = self.request.POST.get('id', None)
    nit = self.request.POST.get('nit', None)
    proveedor = None
    try:
        proveedor = Proveedore.objects.get(id=id, nit=nit)
    except Proveedore.DoesNotExist as e:
        self.object = proveedor
    if proveedor is not None:
        proveedor.estado = False
        proveedor.save()
        self.object = proveedor
    return self.render_to_json_response()

  def get_data(self):
      if self.object is not None:
          data = {
              'message': 'Se inhabilito el usuario',
          }
      else:
          data = {
              'message': 'Este proveeedor no se encuentra registrado'
          }

      return data

class CrearProveedor(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Proveedore
    form_class = ProveedoreForm
    success_url = reverse_lazy('proveedores:proveedor')
    success_message = 'El proveedor %(empresa)s fue registrado en el sistema.'


class ActualizarProveedor(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Proveedore
    success_url = reverse_lazy('proveedores:proveedor')
    slug_field = 'id'
    slug_url_kwarg = 'id'
    form_class = ProveedoreForm
    success_message = u'La información del proveedor %(empresa)s fue actualizada'



class ConsultarProveedor(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = Proveedore
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()

    def get_data(self):
        if self.object is not None:
            data = {
                'status': 200,
                'proveedor':{
                    'nit': self.object.nit,
                    'nombre_empresa': self.object.empresa,
                    'direccion': self.object.direccion,
                    'telefono': self.object.telefono,
                    'fax': self.object.fax,
                    'correo_empresa': self.object.correo_empresa,
                    'nombre_contacto': self.object.nombre_contacto,
                    'apellido_contacto': self.object.apellido_contacto,
                    'telefono_contacto': self.object.telefono_contacto,
                    'correo_contacto': self.object.correo_contacto,
                    'estado': self.object.estado
                }
            }
        else:
            data = {
                'status': 404,
                'message': 'El proveedor no se encuentra registrado'
            }
        return data

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            obj = None
        return obj



class ProveedoresView(LoginRequiredMixin, TemplateView):
    template_name = 'proveedores/proveedore_form.html'


    def get_context_data(self, **kwargs):
        context = super(ProveedoresView, self).get_context_data(**kwargs)
        context.update({'form': ProveedoreForm()})

        return context
