from django.shortcuts import render

from django.shortcuts import render
from django.template import loader
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import GroupForm

class CrearGrupo(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'is_superuser', 'is_active']
    success_url = reverse_lazy('usuarios:usuario')

@login_required()
def GrupoView(request):
    form = GroupForm()
    template = loader.get_template('grupos/group_form.html')
    contex = {
        'form': form
    }
    return HttpResponse(template.render(contex, request))
