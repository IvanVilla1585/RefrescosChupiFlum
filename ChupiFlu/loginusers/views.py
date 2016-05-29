from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.template import loader


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
