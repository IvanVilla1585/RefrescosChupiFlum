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
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import JsonResponse
from django.views.generic import TemplateView

from .models import Maquina
from proveedores.mixins import JSONResponseMixin
from .forms import MaquinaForm
from loginusers.mixins import LoginRequiredMixin


class ListarMaquinas(LoginRequiredMixin, ListView):
    model = Maquina
    template_name = 'maquina_list.html'
    paginate_by = 5


class CrearMaquina(LoginRequiredMixin, CreateView):
    model = Maquina
    success_url = reverse_lazy('maquinas:maquinaForm')
    form_class = MaquinaForm

class ModificarMaquina(LoginRequiredMixin, UpdateView):
    model = Maquina
    form_class = MaquinaForm
    success_url = reverse_lazy('maquinas:listar')

class ConsultarMaquina(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = Maquina
    slug_field = 'nombre'
    slug_url_kwarg = 'nombre'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        data = {
            'maquina':{
                'id': self.object.id,
                'nombre': self.object.nombre,
                'descripcion': self.object.descripcion,
                'unidad_medida': self.object.unidad_medida.nombre,
                'capacidad': self.object.capacidad,
                'tiempo': self.object.tiempo
            }
        }
        return data

class MaquinaView(LoginRequiredMixin, TemplateView):
    template_name = 'maquina/maquina_form.html'


    def get_context_data(self, **kwargs):
        context = super(MaquinaView, self).get_context_data(**kwargs)
        context.update({'form': MaquinaForm(), 'title': 'Maquina'})

        return context
