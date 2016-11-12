# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import UnidadMedida

class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ('nombre', 'equivalencia', 'code', 'descripcion', 'estado',)
        labels = {
            'nombre': _(u'*Nombre'),
            'equivalencia': _(u'*Equivalencia'),
            'code': _(u'*Codigo'),
            'descripcion': _(u'Descripción'),
        }
        error_messages = {
            'nombre': {
                'required': _("El campo nombre es requerido"),
            },
            'equivalencia': {
                'required': _("El campo equivalencia es requerido"),
            },
            'code': {
                'required': _("El campo codigo es requerido"),
            },
        }
