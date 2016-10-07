# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('descripcion', 'fecha', 'proveedor', 'usuario','total',)
        labels = {
            'descripcion': _(u'Descripción'),
            'fecha': _(u'Fecha Pedido'),
            'proveedor': _(u'*Proveedor'),
            'usuario': _(u'Usuario'),
            'total': _(u'*Total'),
            'id_materia_prima': _(u'*Materia'),
        }
        error_messages = {
            'fecha': {
                'required': _("El campo fecha es requerido"),
            },
            'proveedor': {
                'required': _("El campo proveedor es requerido"),
            },
            'usuario': {
                'required': _("El campo usuario es requerido"),
            },
            'total': {
                'required': _("El campo total es requerido"),
            },
        }
