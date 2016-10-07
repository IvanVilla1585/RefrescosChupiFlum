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
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
from django.contrib.auth.models import Group
from proveedores.mixins import JSONResponseMixin
from loginusers.mixins import LoginRequiredMixin

class CrearUsuario(LoginRequiredMixin, CreateView):
    model = User
    success_url = reverse_lazy('usuarios:usuario')
    form_class = UserCreationForm

    def form_valid(self, form):
        self.object = form.save()
        grup = form.cleaned_data['groups']
        grupo = Group.objects.get(id=grup)
        self.object.groups.add(grupo.id)
        return super(CrearUsuario, self).form_valid(form)


class ListarUsuarios(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    paginate_by = 5

class ModificarUsuario(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('maquinas:listar')

class ConsultarUsuario(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = User
    slug_field = 'nombre'
    slug_url_kwarg = 'nombre'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        data = {
            'maquina':{
                'id': self.object.id,
                'nombre': self.object.nombre,
                'descripcion': self.object.descripcion,
                'unidad_medida': self.object.unidad_medida.nombre,
                'capacidad': self.object.capacidad,
                'tiempo': self.object.tiempo
            }
        }
        return data

class UsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/user_form.html'

    def get_context_data(self, **kwargs):
        context = super(UsuarioView, self).get_context_data(**kwargs)
        context.update({'form': UserCreationForm()})

        return context
