# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
from .models import ProductoTerminado
from .models import Detalles_Formulas

class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = ProductoTerminado
        fields = ('nombre', 'descripcion', 'categoria', 'presentacion', 'costo_produccion', 'precio_venta','cantidad', 'cantidad_productos', 'estado', 'stock',)
        labels = {
            'nombre': _(u'*Nombre'),
            'descripcion': _(u'Descripción'),
            'categoria': _(u'*Categoria'),
            'costo_produccion': _(u'*Costo Producción'),
            'precio_venta': _(u'*Precio Venta'),
            'cantidad': _(u'Cantidad'),
            'cantidad_productos': _(u'*Cantidad Productos a Elaborar'),
            'stock': _(u'*Stock'),
            'presentacion': _(u'*Presentación Producto'),
        }
        error_messages = {
            'nombre': {
                'required': _('El campo nombre es obligatorio'),
            },
            'categoria': {
                'required': _('La categoria es obligatorio'),
            },
            'stock': {
                'required': _('El campo stock es obligatorio'),
            },
            'costo_produccion': {
                'required': _(u'El campo costo producción es obligatorio'),
            },
            'precio_venta': {
                'required': _('El campo precio venta es obligatorio'),
            },
            'cantidad_productos': {
                'required': _('El campo cantidad de productos es obligatorio'),
            },
            'presentacion': {
                'required': _(u'El campo presentación del producto es obligatorio'),
            },
        }

    def clean_nombre(self):
        diccionario_datos = self.cleaned_data

        nombre = diccionario_datos.get('nombre')

        if len(nombre) < 3:
            raise forms.ValidationError('El nombre del producto debe contener al menos 3 caracteres')

        return nombre


class DetalleFormulaForm(forms.ModelForm):

    class Meta:
        model = Detalles_Formulas

        fields = ('id_producto', 'id_materia_prima', 'cantidad',)
        labels = {
            'id_materia_prima': _(u'*Materia Prima'),
            'cantidad': _(u'*Cantidad'),
        }
        error_messages = {
            'id_materia_prima': {
                'required': _("El campo materia prima es obligatorio"),
            },
            'cantidad': {
                'required': _("El campo cantidad es obligatorio"),
            },
        }



DetalleFormFormSet = inlineformset_factory(ProductoTerminado, Detalles_Formulas, form=DetalleFormulaForm, extra=6, )
