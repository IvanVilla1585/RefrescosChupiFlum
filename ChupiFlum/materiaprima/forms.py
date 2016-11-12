# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import MateriaPrima

class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ('nombre', 'descripcion', 'unidad_medida', 'categoria', 'cantidad', 'estado',)
        labels = {
            'nombre': _(u'*Nombre'),
            'descripcion': _(u'Descripción Producto'),
            'unidad_medida': _(u'*Unidad de Medida'),
            'categoria': _(u'*Categoria'),
            'cantidad': _(u'*Cantidad'),
        }
        error_messages = {
            'nombre': {
                'required': _("El campo nombre es obligatorio"),
            },
            'unidad_medida': {
                'required': _("La unidad de medida es obligatoria"),
            },
            'categoria': {
                'required': _("La categoria es obligatoria"),
            },
            'cantidad': {
                'required': _("El campo cantidad es obligatorio"),
            },
        }
