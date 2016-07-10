# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import MateriaPrima

class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ('nombre', 'descripcion', 'unidad_medida', 'categoria', 'cantidad',)
        labels = {
            'nombre': _(u'*Nombre'),
            'descripcion': _(u'Descripción Producto'),
            'unidad_medida': _(u'*Unidad de Medida'),
            'categoria': _(u'*Categoria'),
            'cantidad': _(u'*Cantidad'),
        }
        error_messages = {
            'nombre': {
                'required': _("El campo nombre es requerido"),
            },
            'unidad_medida': {
                'required': _("La unidad de medida es requerida"),
            },
            'categoria': {
                'required': _("La categoria es requerida"),
            },
            'cantidad': {
                'required': _("El campo cantidad es requerido"),
            },
        }
