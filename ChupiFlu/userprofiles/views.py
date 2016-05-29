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
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm

class CrearUsuario(CreateView):
    model = User
    success_url = reverse_lazy('usuarios:usuario')
    fields = ['first_name', 'last_name', 'email', 'username', 'is_superuser', 'is_active']

@login_required()
def UsuarioView(request):
    form = UserCreationForm()
    template = loader.get_template('auth/user_form.html')
    contex = {
        'form': form
    }
    return HttpResponse(template.render(contex, request))
