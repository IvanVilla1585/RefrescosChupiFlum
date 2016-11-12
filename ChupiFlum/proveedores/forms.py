# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Proveedore

class ProveedoreForm(forms.ModelForm):
    class Meta:
        model = Proveedore
        fields = ('nit', 'empresa', 'direccion', 'telefono', 'fax', 'correo_empresa', 'nombre_contacto',
                  'apellido_contacto', 'telefono_contacto', 'correo_contacto', 'estado',)
        labels = {
            'nit': _(u'*Nit'),
            'empresa': _(u'*Nombre de la Empresa'),
            'direccion': _(u'*Dirección'),
            'telefono': _(u'*Teléfono'),
            'fax': _(u'Fax'),
            'correo_empresa': _(u'Correo Empresa'),
            'nombre_contacto': _(u'*Nombres Contacto'),
            'apellido_contacto': _(u'Apellidos Contacto'),
            'telefono_contacto': _(u'*Teléfono Contacto'),
            'correo_contacto': _(u'Correo Contacto'),
            'estado': _(u'Activo'),
        }
        error_messages = {
            'nit': {
                'required': _("El campo nit es requerido"),
            },
            'empresa': {
                'required': _("El campo nombre empresa es requerido"),
            },
            'direccion': {
                'required': _(u"El campo dirección es requerido"),
            },
            'telefono': {
                'required': _(u"El campo teléfono es requerido"),
            },
            'nombre_contacto': {
                'required': _("El campo nombre contacto es requerido"),
            },
            'telefono_contacto': {
                'required': _(u"El campo teléfono contacto es requerido"),
            },
        }

    def clean_correo_empresa(self):
        diccionario_datos = self.cleaned_data

        correo_empresa = diccionario_datos.get('correo_empresa')

        if correo_empresa:
            proveedor = Proveedore.objects.filter(correo_empresa=correo_empresa)
            if proveedor:
               raise forms.ValidationError("No se puede asociar un correo a varios proveedores")

        return correo_empresa

    def clean_correo_contacto(self):
        diccionario_datos = self.cleaned_data

        correo_contacto = diccionario_datos.get('correo_contacto')
        
        if correo_contacto:
            proveedor = Proveedore.objects.filter(correo_contacto=correo_contacto)
            if proveedor:
               raise forms.ValidationError("No se puede asociar un correo a varios contactos")

        return correo_contacto
