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
from .forms import KardexMateriaPrimaForm
from .models import KardexMateriaPrima
from proveedores.mixins import JSONResponseMixin
from loginusers.mixins import LoginRequiredMixin
from decimal import Decimal
import ast

class KardexMateriaPrimaView(LoginRequiredMixin, TemplateView):
    template_name = 'kardex_materia_prima/kardexmateriaprima_form.html'

    def get_context_data(self, **kwargs):
        context = super(KardexMateriaPrimaView, self).get_context_data(**kwargs)
        context.update({'form': KardexMateriaPrimaForm()})
        return context

class CrearKardexMateriaPrima(LoginRequiredMixin, CreateView):
    model = KardexMateriaPrima
    success_url = reverse_lazy('kardexmateria:form')
    form_class = KardexMateriaPrimaForm
