from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from .models import Perfil
from .forms import PerfilesForm



def listarPerfiles(request):
    perfil = Perfil.objects.order_by('id')
    template = loader.get_template('lista_perfiles.html')
    context = {
        'perfil': perfil
    }
    return HttpResponse(template.render(context, request))


def perfil(request):
    form = PerfilesForm()
    template = loader.get_template('perfil.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))

def guardar(request):
    form = PerfilesForm(request.POST)
    if form.is_valid():
        perfil = form.save()
        perfil.save()
        return HttpResponseRedirect('/')
