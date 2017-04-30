from django.shortcuts import render
from django.template import loader
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.views.generic import (
    ListView,
    View
)
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.template import (
    loader,
    Context
)
from django.core.mail import (
    send_mail,
    BadHeaderError
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.contrib.auth.models import Group
from proveedores.mixins import JSONResponseMixin
from loginusers.mixins import LoginRequiredMixin
from ChupiFlum import settings

class CrearUsuario(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    success_url = reverse_lazy('usuarios:usuario')
    form_class = UserForm
    template_name = 'userprofiles/user_form.html'
    success_message = 'El usuario %(username)s fue registrado en el sistema'
    html_message = None

    def form_valid(self, form):
        self.object = form.save()
        print self.object
        grup = form.cleaned_data['groups']
        grupo = Group.objects.get(id=grup)
        self.object.groups.add(grupo.id)
        ctx = {'ok': 'Mensaje enviado'}
        self.html_message = loader.get_template('userprofiles/email_templatel.html').render(Context(ctx))
        try:
            send_mail(
                'Prueba',
                'Prueba 2',
                settings.EMAIL_HOST_USER,
                [self.object.email],
                fail_silently=False,
                auth_user=None,
                auth_password=None,
                connection=None,
                html_message=self.html_message
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        return super(CrearUsuario, self).form_valid(form)


class ListarUsuarios(LoginRequiredMixin, JSONResponseMixin, ListView):
    model = User
    template_name = 'userprofiles/user_list.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_json_response()

    def get_data(self):
        data = [{
            'id': user.id,
            'value': user.username,
        } for user in self.object_list]

        return data

    def get_queryset(self):
        nom = self.request.GET.get('term', None)
        if nom:
            queryset = self.model.objects.filter(username__icontains=nom)
        else:
            queryset = super(ListarUsuarios, self).get_queryset()

        return queryset

class ActualizarUsuario(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    slug = 'id'
    slug_url_kwarg = 'id'
    form_class = UserForm
    template_name = 'userprofiles/user_form.html'
    success_url = reverse_lazy('usuarios:usuario')
    success_message = 'Los datos del usuario %(username)s se actualizaron'

class ConsultarUsuario(LoginRequiredMixin, JSONResponseMixin, DetailView):
    model = User
    slug_field = 'id'
    slug_url_kwarg = 'id'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_json_response()
    def get_data(self):
        data = {
            'status': 200,
            'usuario':{
                'id': self.object.id,
                'first_name': self.object.first_name,
                'last_name': self.object.last_name,
                'email': self.object.email,
                'username': self.object.username,
                'password': self.object.password,
                'is_active': self.object.is_active
            }
        }
        return data

class UsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'userprofiles/user_form.html'

    def get_context_data(self, **kwargs):
        context = super(UsuarioView, self).get_context_data(**kwargs)
        context.update({'form': UserForm()})

        return context
