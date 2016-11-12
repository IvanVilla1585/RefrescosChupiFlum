# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import ProductoTerminado

class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = ProductoTerminado
        fields = ('nombre', 'descripcion', 'categoria', 'costo_produccion', 'precio_venta','cantidad', 'estado',)
        labels = {
            'nombre': _(u'*Nombre'),
            'descripcion': _(u'Descripción'),
            'categoria': _(u'*Categoria'),
            'costo_produccion': _(u'*Costo Producción'),
            'precio_venta': _(u'*Precio Venta'),
            'cantidad': _(u'*Cantidad'),
        }
        error_messages = {
            'nombre': {
                'required': _('El campo nombre es obligatorio'),
            },
            'categoria': {
                'required': _('La categoria es obligatorio'),
            },
            'cantidad': {
                'required': _('El campo cantidad es obligatorio'),
            },
            'costo_produccion': {
                'required': _(u'El campo costo producción es obligatorio'),
            },
            'precio_venta': {
                'required': _('El campo precio venta es obligatorio'),
            },
        }
