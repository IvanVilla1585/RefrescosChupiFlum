# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django import forms
from django.utils.translation import ugettext_lazy as _

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions',)
        labels = {
            'name': _(u'*Nombre del Rol'),
            'permissions': _(u'*Permisos'),
        }
        error_messages = {
            'name': {
                'required': _("El campo nombre del rol es requerido"),
            },
            'permissions': {
                'required': _(u"Seleccione al menos un permiso"),
            },
        }
