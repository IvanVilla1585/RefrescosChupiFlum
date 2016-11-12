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

from .models import MateriaPrima
from proveedores.mixins import JSONResponseMixin
from .forms import MateriaPrimaForm
from loginusers.mixins import LoginRequiredMixin


class ListarMateriaPrima(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = MateriaPrima
    template_name = 'materiaprima_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        data = [{
            'id': materiaprima.id,
            'value': materiaprima.nombre,
        } for materiaprima in self.object_list]

        return data

    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(nombre__icontains=nom)
        else:
            queryset = super(ListarMateriaPrima, self).get_queryset()

        return queryset

class CrearMateriaPrima(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MateriaPrima
    success_url = reverse_lazy('materiaprim:materiaPrimaForm')
    form_class = MateriaPrimaForm
    success_message = 'La materia prima %(nombre)s se registro en el sistema'

class ModificarMateriaPrima(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MateriaPrima
    slug_field = 'id'
    slug_url_kwarg = 'id'
    form_class = MateriaPrimaForm
    success_url = reverse_lazy('materiaprim:materiaPrimaForm')
    success_message = 'Los datos de la materia prima %(nombre)s se actualizaron'

class ActualizarEstadoView(JSONResponseMixin, View):
    object = None
    relacion = None
    def post(self, request):
        id = self.request.POST.get('id', None)
        materia = None
        try:
            materia = MateriaPrima.objects.get(id=id)
        except MateriaPrima.DoesNotExist as e:
            self.object = materia
        if materia is not None:
            materia.estado = False
            materia.save()
            self.object = materia
        return self.render_to_json_response()

    def get_data(self):
        if self.object is not None:
            data = {
                'message': 'Se inhabilito la materia rima',
            }
        else:
            data = {
                'message': 'Esta materia prima se encuentra asociada'
            }

        return data

class ConsultarMateriaPrima(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = MateriaPrima
    slug_field = 'id'
    slug_url_kwarg = 'id'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        if self.object is not None:
            data = {
                'status': 200,
                'materia':{
                    'id': self.object.id,
                    'nombre': self.object.nombre,
                    'descripcion': self.object.descripcion,
                    'unidad_medida': self.object.unidad_medida.nombre,
                    'categoria': self.object.categoria.nombre,
                    'cantidad': self.object.cantidad,
                    'estado': self.object.estado
                }
            }
        else:
            data = {
                'status': 404,
                'message': 'La materia prima no se encuentra registrada'
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


class MateriaPrimaView(LoginRequiredMixin, TemplateView):
    template_name = 'materiaprima/materiaprima_form.html'

    def get_context_data(self, **kwargs):
        context = super(MateriaPrimaView, self).get_context_data(**kwargs)
        context.update({'form': MateriaPrimaForm()})

        return context
