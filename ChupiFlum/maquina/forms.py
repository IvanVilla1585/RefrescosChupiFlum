# -*- coding: utf-8 -*-
from django import forms
from django.forms import TimeField
from django.utils.translation import ugettext_lazy as _
from .models import Maquina

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ('nombre', 'descripcion', 'capacidad', 'unidad_medida','tiempo', 'estado',)
        labels = {
            'nombre': _(u'*Nombre'),
            'descripcion': _(u'Descripción'),
            'capacidad': _(u'*Capacidad Producción'),
            'unidad_medida': _(u'*Unidad de Medida'),
            'tiempo': _(u'*Tiempo Producción'),
        }
        error_messages = {
            'nombre': {
                'required': _("El campo nombre de la maquina es requerido"),
            },
            'capacidad': {
                'required': _(u"El campo capacidad es requerido"),
            },
            'unidad_medida': {
                'required': _(u"Seleccione una unidad de medida"),
            },
            'tiempo': {
                'required': _(u"El campo tiempo es requerido"),
            },
        }
