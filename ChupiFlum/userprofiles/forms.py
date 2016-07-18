# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'is_superuser',
                  'is_active', 'password1', 'password2', 'groups',)
        labels = {
            'first_name': _(u'Nombre'),
            'last_name': _(u'Apellido'),
            'email': _(u'Correo'),
            'username': _(u'*Nombre de Usuario'),
            'is_superuser': _(u'Super Usuario'),
            'is_active': _(u'Activo'),
            'groups': _(u'*Grupo'),
            'password1': _(u'*Contraseña'),
            'password2': _(u'*Contraseña'),
        }

        error_messages = {
            'username': {
                'required': _("El campo nombre de usuario es requerido"),
            },
            'password': {
                'required': _(u"El campo contraseña es requerido"),
            },
            'groups': {
                'required': _("Los grupos son requeridos"),
            },
        }
