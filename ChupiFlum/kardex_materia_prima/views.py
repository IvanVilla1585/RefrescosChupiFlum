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
from pedido.models import Pedido
from estado_orden.models import EstadosOrdenes
from materiaprima.models import MateriaPrima
from proveedores.mixins import JSONResponseMixin
from loginusers.mixins import LoginRequiredMixin
from decimal import Decimal
import ast

class KardexMateriaPrimaView(LoginRequiredMixin, TemplateView):
    template_name = 'kardex_materia_prima/kardexmateriaprima_form.html'

    def get_context_data(self, **kwargs):
        context = super(KardexMateriaPrimaView, self).get_context_data(**kwargs)
        context.update({'form': KardexMateriaPrimaForm(), 'title': 'Kardex Materia Prima'})
        return context

class CrearKardexMateriaPrima(LoginRequiredMixin, CreateView):
    model = KardexMateriaPrima
    success_url = reverse_lazy('kardexmateria:form')
    form_class = KardexMateriaPrimaForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        pedido = Pedido.objects.get(id=self.object.pedido)
        if pedido.id_etado == 3 | pedido.id_etado == 4:
            form.add_error('estado_invalido','El pedido no puede estar en estado cancelado o terminado')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            total = self.model.objects.filter(pedido=self.object.pedido, materiaprima=self.object.materiaprima).count()
            if (total + self.object.cantidad) >= pedido.cantidad:
                form.add_error('cantidad_invalida','La cantidad de ingreso supera la cantidad del pedido de este producto')
                return self.render_to_response(self.get_context_data(form=form))
            else:
                if pedido.id_etado == 1:
                    estado = EstadosOrdenes.objects.get(id=2)
                    pedido.id_estado = estado
                    pedido.save()
                else:
                    if (total + self.object.cantidad) == pedido.cantidad:
                        estado = EstadosOrdenes.objects.get(id=4)
                        pedido.id_estado = estado
                        pedido.save()
                materia = MateriaPrima.objects.get(id=self.object.materiaprima)
                materia.cantidad = materia.cantidad + self.object.cantidad
                materia.save()
                self.object.save()
        return super(CrearKardexMateriaPrima, self).form_valid(form)
