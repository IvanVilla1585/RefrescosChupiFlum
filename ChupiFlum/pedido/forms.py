# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
from .models import Pedido, Detalle_Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('descripcion', 'fecha', 'proveedor','total',)
        labels = {
            'descripcion': _(u'Descripción'),
            'fecha': _(u'*Fecha Pedido'),
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


class DetallePedidoForm(forms.ModelForm):

    class Meta:
        model = Detalle_Pedido

        fields = ('id_materia_prima', 'cantidad', 'valor_unitario',)
        labels = {
            'id_materia_prima': _(u'*Materia Prima'),
            'cantidad': _(u'*Cantidad'),
            'valor_unitario': _(u'*Valor Unitario'),
        }
        error_messages = {
            'id_materia_prima': {
                'required': _("El campo materia prima es obligatorio"),
            },
            'cantidad': {
                'required': _("El campo cantidad es obligatorio"),
            },
            'valor_unitario': {
                'required': _("El campo valor unitario es obligatorio"),
            },
        }


PedidoMateriaFormSet = inlineformset_factory(Pedido, Detalle_Pedido, form=DetallePedidoForm, extra=4, )
