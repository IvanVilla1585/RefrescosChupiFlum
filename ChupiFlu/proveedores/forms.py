# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Proveedore

class ProveedoreForm(forms.ModelForm):
    class Meta:
        model = Proveedore
        fields = ('nit', 'nombre_empresa', 'direccion', 'telefono', 'fax', 'correo_empresa', 'nombre_contacto',
                  'apellido_contacto', 'telefono_contacto', 'correo_contacto')
        labels = {
            'nit': _(u'*Nit'),
            'nombre_empresa': _(u'*Nombre de la Empresa'),
            'direccion': _(u'*Dirección'),
            'telefono': _(u'*Teléfono'),
            'fax': _(u'Fax'),
            'correo_empresa': _(u'Correo Empresa'),
            'nombre_contacto': _(u'*Nombres Contacto'),
            'apellido_contacto': _(u'Apellidos Contacto'),
            'telefono_contacto': _(u'*Teléfono Contacto'),
            'correo_contacto': _(u'Correo Contacto'),
        }
        error_messages = {
            'nit': {
                'required': _("El campo nit es requerido"),
            },
            'nombre_empresa': {
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
