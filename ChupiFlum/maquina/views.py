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

from .models import Maquina
from proveedores.mixins import JSONResponseMixin
from .forms import MaquinaForm
from loginusers.mixins import LoginRequiredMixin


class ListarMaquinas(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = Maquina
    template_name = 'maquina_list.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        if self.object_list is not None:
            data = [{
                'id': maquina.id,
                'value': maquina.nombre,
            } for maquina in self.object_list]
        else:
            data = [{
                'id': '0',
                'value': 'No hay maquinas',
            }]

        return data

    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(nombre__icontains=nom)
        else:
            queryset = super(ListarMaquinas, self).get_queryset()

        return queryset

class ActualizarEstadoView(JSONResponseMixin, View):
    object = None
    relacion = None
    def post(self, request):
        id = self.request.POST.get('id', None)
        maquina = None
        try:
            maquina = Maquina.objects.get(id=id)
        except Maquina.DoesNotExist as e:
            self.object = maquina
        if maquina is not None:
            maquina.estado = False
            maquina.save()
            self.object = maquina
        return self.render_to_json_response()

    def get_data(self):
        if self.object is not None:
            data = {
                'message': 'Se inhabilito la maquina',
            }
        else:
            data = {
                'message': 'Esta maquina se encuentra asociada a procesos'
            }

        return data

class CrearMaquina(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Maquina
    success_url = reverse_lazy('maquinas:maquinaForm')
    form_class = MaquinaForm
    success_message = "La maquina %(nombre)s se registro en el sistema"

class ModificarMaquina(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Maquina
    form_class = MaquinaForm
    success_url = reverse_lazy('maquinas:maquinaForm')
    success_message = "La maquina %(nombre)s fue actualizada"

class ConsultarMaquina(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = Maquina
    slug_field = 'id'
    slug_url_kwarg = 'id'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        if self.object is not None:
            data = {
                'status': 200,
                'maquina':{
                    'id': self.object.id,
                    'nombre': self.object.nombre,
                    'descripcion': self.object.descripcion,
                    'unidad_medida': self.object.unidad_medida.nombre,
                    'capacidad': self.object.capacidad,
                    'tiempo': self.object.tiempo,
                    'estado': self.object.estado
                }
            }
        else:
            data = {
                'status': 404,
                'message': 'No se encuentra ninguna maquina asociada a la busqueda'
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

class MaquinaView(LoginRequiredMixin, TemplateView):
    template_name = 'maquina/maquina_form.html'


    def get_context_data(self, **kwargs):
        context = super(MaquinaView, self).get_context_data(**kwargs)
        context.update({'form': MaquinaForm()})

        return context
