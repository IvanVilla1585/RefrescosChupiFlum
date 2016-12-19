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

    def clean_nit(self):
        diccionario_datos = self.cleaned_data

        nit = diccionario_datos.get('nit')

        if len(nit) < 6:
            raise forms.ValidationError('El nit debe contener al menos 6 caracteres')

        return nit

    def clean_empresa(self):
        diccionario_datos = self.cleaned_data

        empresa = diccionario_datos.get('empresa')

        if len(empresa) < 3:
            raise forms.ValidationError('El nombre de la empresa debe contener al menos 3 caracteres')

        return empresa

    def clean_nombre_contacto(self):
        diccionario_datos = self.cleaned_data

        nombre_contacto = diccionario_datos.get('nombre_contacto')

        if len(nombre_contacto) < 3:
            raise forms.ValidationError('El nombre del contacto debe contener al menos 3 caracteres')

        return nombre_contacto

    def clean_telefono(self):
        diccionario_datos = self.cleaned_data

        telefono = diccionario_datos.get('telefono')

        if len(telefono) < 7:
            raise forms.ValidationError(u'El teléfono debe contener al menos 7 caracteres')

        return telefono

    def clean_telefono_contacto(self):
        diccionario_datos = self.cleaned_data

        telefono_contacto = diccionario_datos.get('telefono_contacto')

        if len(telefono_contacto) < 7:
            raise forms.ValidationError(u'El teléfono debe contener al menos 7 caracteres')

        return telefono_contacto

    def clean_direccion(self):
        diccionario_datos = self.cleaned_data

        direccion = diccionario_datos.get('direccion')

        if len(direccion) < 7:
            raise forms.ValidationError(u'La dirección debe contener al menos 7 caracteres')

        return direccion
