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
from django.contrib.auth.models import Group
from loginusers.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import GroupForm

class CrearGrupo(CreateView):
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('grupos:grupo')

class GroupView(LoginRequiredMixin, TemplateView):
    template_name = 'grupos/group_form.html'

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        context.update({'form': GroupForm()})
        return context


@login_required()
def grupoView(request):
    form = GroupForm()
    template = loader.get_template('grupos/group_form.html')
    contex = {
        'form': form
    }
    return HttpResponse(template.render(contex, request))
