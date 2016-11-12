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
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin

from .models import UnidadMedida
from proveedores.mixins import JSONResponseMixin
from .forms import UnidadMedidaForm
from loginusers.mixins import LoginRequiredMixin


class ListarUnidadMedidas(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = UnidadMedida
    template_name = 'unidadmedida_list.html'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        data = [{
            'id': unidad.id,
            'value': unidad.nombre,
        } for unidad in self.object_list]

        return data

    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(nombre__icontains=nom)
        else:
            queryset = super(ListarUnidadMedidas, self).get_queryset()

        return queryset


class CrearUnidadMedida(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = UnidadMedida
    success_url = reverse_lazy('unidades:unidadForm')
    form_class = UnidadMedidaForm
    success_message = "La unidad de meidida %(nombre)s fue registrada en el sistema."

class ModificarUnidadMedida(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    success_url = reverse_lazy('unidades:unidadForm')
    success_message = "La unidad de meidida %(nombre)s fue actualizada."

class ConsultarUnidadMedida(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = UnidadMedida
    slug_field = 'id'
    slug_url_kwarg = 'id'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        data = {
            'status': 200,
            'unidad':{
                'id': self.object.id,
                'nombre': self.object.nombre,
                'equivalencia': self.object.equivalencia,
                'code': self.object.code,
                'descripcion': self.object.descripcion,
                'estado': self.object.estado
            }
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

class ActualizarEstadoView(JSONResponseMixin, View):
    object = None
    relacion = None
    def post(self, request):
        id = self.request.POST.get('id', None)
        unidad = None
        try:
            unidad = UnidadMedida.objects.get(id=id)
        except UnidadMedida.DoesNotExist as e:
            self.object = unidad
        if unidad is not None:
            unidad.estado = False
            unidad.save()
            self.object = unidad
        return self.render_to_json_response()

    def get_data(self):
        if self.object is not None:
            data = {
                'message': 'Se inhabilito la unidad de medida',
            }
        else:
            data = {
                'message': 'Esta unidad de medida se encuentra asociada a productos'
            }

        return data

class UnidadMedidaView(LoginRequiredMixin, TemplateView):
    template_name = 'unidadesmedida/unidadmedida_form.html'

    def get_context_data(self, **kwargs):
        context = super(UnidadMedidaView, self).get_context_data(**kwargs)
        context.update({'form': UnidadMedidaForm()})

        return context
