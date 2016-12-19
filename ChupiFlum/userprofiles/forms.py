# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'groups', 'is_active',)
        labels = {
            'first_name': _(u'Nombre'),
            'last_name': _(u'Apellido'),
            'email': _(u'Correo'),
            'username': _(u'*Nombre de Usuario'),
            'is_active': _(u'Activo'),
            'groups': _(u'*Grupo'),
            'password1': _(u'*Contraseña'),
            'password2': _(u'*Repetir Contraseña'),
        }

        error_messages = {
            'username': {
                'required': _("El campo nombre de usuario es requerido"),
            },
            'password1': {
                'required': _(u"El campo contraseña es requerido"),
                'password_mismatch': _(u'Las contraseñas no coinciden'),
            },
            'groups': {
                'required': _("Los grupos son requeridos"),
            },
        }
