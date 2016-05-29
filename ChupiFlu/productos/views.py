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
from .forms import ProductoTerminadoForm
from .models import ProductoTerminado

class CrearProducto(CreateView):
    model = ProductoTerminado
    success_url = reverse_lazy('productos:producto')
    fields = ['nombre', 'descripcion', 'categoria', 'costo_produccion', 'precio_venta']

@login_required()
def productoTerminadoView(request):
    form = ProductoTerminadoForm()
    template = loader.get_template('productos/productoterminado_form.html')
    contex = {
        'form': form
    }
    return HttpResponse(template.render(contex, request))
