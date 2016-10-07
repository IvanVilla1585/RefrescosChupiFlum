# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import KardexMateriaPrima

class KardexMateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = KardexMateriaPrima
        fields = ('pedido', 'fecha_movimiento', 'tipo_movimiento', 'materiaprima','cantidad', 'valor_unitario', 'total', 'lote', 'fecha_vencimiento',)
        labels = {
            'pedido': _(u'*Número de Pedido'),
            'fecha_movimiento': _(u'*Fecha'),
            'tipo_movimiento': _(u'*Tipo Movimiento'),
            'materiaprima': _(u'*Materia Prima'),
            'cantidad': _(u'*Cantidad'),
            'valor_unitario': _(u'*Valor Unitario'),
            'total': _(u'*Total'),
            'lote': _(u'*Lote'),
            'fecha_vencimiento': _(u'*Fecha Vencimiento'),
        }
        error_messages = {
            'pedido': {
                'required': _("El campo pedido es requerido"),
            },
            'fecha_movimiento': {
                'required': _("El campo fecha es requerido"),
            },
            'tipo_movimiento': {
                'required': _("El campo tipo movimiento es requerido"),
            },
            'materiaprima': {
                'required': _("El campo materia prima es requerido"),
            },
            'cantidad': {
                'required': _("El campo cantidad es requerido"),
            },
            'valor_unitario': {
                'required': _("El campo valor unitario es requerido"),
            },
            'total': {
                'required': _("El campo total es requerido"),
            },
            'lote': {
                'required': _("El campo lote es requerido"),
            },
            'fecha_vencimiento': {
                'required': _("El campo fecha vencimiento es requerido"),
            },
        }
