# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)
        labels = {
            'username': _(u'*Nombre de Usuario'),
            'password': _(u'*Contraseña'),
        }

        error_messages = {
            'username': {
                'required': _("El campo nombre de usuario es requerido"),
            },
            'password': {
                'required': _(u"El campo contraseña es requerido"),
            },
        }
    ##username = forms.CharField()
    ##password = forms.CharField(widget=forms.PasswordInput)
