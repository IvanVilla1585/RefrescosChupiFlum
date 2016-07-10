# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import ProductoTerminado

class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = ProductoTerminado
        fields = ('nombre', 'descripcion', 'categoria', 'costo_produccion', 'precio_venta','cantidad')
        labels = {
            'nombre': _(u'*Nombre'),
            'descripcion': _(u'Descripción'),
            'categoria': _(u'*Categoria'),
            'costo_produccion': _(u'Costo Producción'),
            'cantidad': _(u'*Cantidad'),
        }
        error_messages = {
            'nombre': {
                'required': _("El campo nombre es requerido"),
            },
            'categoria': {
                'required': _("La categoria es requerida"),
            },
            'cantidad': {
                'required': _("El campo cantidad es requerido"),
            },
        }
