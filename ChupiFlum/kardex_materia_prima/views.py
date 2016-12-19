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
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import KardexMateriaPrimaForm
from .models import KardexMateriaPrima
from pedido.models import Pedido
from estado_orden.models import EstadosOrdenes
from materiaprima.models import MateriaPrima
from pedido.models import Detalle_Pedido
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

class CrearKardexMateriaPrima(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = KardexMateriaPrima
    success_url = reverse_lazy('kardexmateria:form')
    form_class = KardexMateriaPrimaForm
    success_message = 'La entrada de la materia prima se registro en el sistema'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        pedido = Pedido.objects.get(id=self.object.pedido.id)
        if pedido.id_estado.id == 3 or pedido.id_estado.id == 4 or pedido.id_estado.id == 5:
            messages.error(self.request,'El pedido no puede estar en estado cancelado o terminado')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            total = self.model.objects.filter(pedido=self.object.pedido.id, materiaprima=self.object.materiaprima.id).count()
            detalle_pedido = Detalle_Pedido.objects.get(id_pedido=self.object.pedido.id, id_materia_prima=self.object.materiaprima.id)
            if (total + self.object.cantidad) > detalle_pedido.cantidad:
                messages.error(self.request,'El pedido no puede estar en estado cancelado o terminado')
                return self.render_to_response(self.get_context_data(form=form))
            else:
                if pedido.id_estado.id == 1 and (total + self.object.cantidad) == detalle_pedido.cantidad:
                    estado = EstadosOrdenes.objects.get(id=5)
                    pedido.id_estado = estado
                    pedido.save()
                elif (total + self.object.cantidad) == pedido.cantidad:
                    estado = EstadosOrdenes.objects.get(id=5)
                    pedido.id_estado = estado
                    pedido.save()
                else:
                    estado = EstadosOrdenes.objects.get(id=2)
                    pedido.id_estado = estado
                    pedido.save()
                materia = MateriaPrima.objects.get(id=self.object.materiaprima.id)
                import ipdb; ipdb.set_trace()
                materia.cantidad = materia.cantidad + self.object.cantidad
                materia.save()
                self.object.save()
        return super(CrearKardexMateriaPrima, self).form_valid(form)
