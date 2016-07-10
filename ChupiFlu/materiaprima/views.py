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

from .models import MateriaPrima
from proveedores.mixins import JSONResponseMixin
from .forms import MateriaPrimaForm
from loginusers.mixins import LoginRequiredMixin


class ListarMateriaPrima(LoginRequiredMixin, ListView):
    model = MateriaPrima
    template_name = 'materiaprima_list.html'
    paginate_by = 5

class CrearMateriaPrima(LoginRequiredMixin, CreateView):
    model = MateriaPrima
    success_url = reverse_lazy('materiaprim:listar')
    form_class = MateriaPrimaForm

class ModificarMateriaPrima(LoginRequiredMixin, UpdateView):
    model = MateriaPrima
    form_class = MateriaPrimaForm
    success_url = reverse_lazy('materiaprim:listar')

class ConsultarMateriaPrima(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = MateriaPrima
    slug_field = 'nombre'
    slug_url_kwarg = 'nombre'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        data = {
            'materia':{
                'id': self.object.id,
                'nombre': self.object.nombre,
                'descripcion': self.object.descripcion,
                'unidad_medida': self.object.unidad_medida.nombre,
                'categoria': self.object.categoria.nombre,
                'cantidad': self.object.cantidad
            }
        }
        return data


class MateriaPrimaView(LoginRequiredMixin, TemplateView):
    template_name = 'materiaprima/materiaprima_form.html'


    def get_context_data(self, **kwargs):
        context = super(MateriaPrimaView, self).get_context_data(**kwargs)
        context.update({'form': MateriaPrimaForm()})

        return context
