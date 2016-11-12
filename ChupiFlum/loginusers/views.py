# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, RedirectView, FormView
from .forms import LoginForm
from django.utils.translation import ugettext_lazy as _


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = '/MenuPrincipal/'

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super(LoginView, self).form_valid(form)

def authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/MenuPrincipal')
    else:
        template = loader.get_template('login.html')
    return HttpResponse(template.render({}, request))

@login_required()
def menuView(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render({}, request))

def homeView(request):
    template = loader.get_template('loginusers/home.html')
    return HttpResponse(template.render({}, request))
