"""from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Usuarios/$', views.UsuarioView.as_view(), name='usuario'),
    url(r'^Usuarios/Guardar/$', views.CrearUsuario.as_view(), name='crear'),
    url(r'^Usuarios/Actualizar', views.ActualizarUsuario.as_view(), name='actualizar'),
    url(r'^Usuarios/Consultar/(?P<id>[0-9]+)/$', views.ConsultarUsuario.as_view(), name='consultar'),
    ##url(r'^Usuarios/Eliminar/(?P<id>[0-9]+)$', views.EliminarUsuario.as_view(), name='eliminar'),
    url(r'^Usuarios/Listar', views.ListarUsuarios.as_view(), name='listar'),
]
"""
from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
user_active_account = UserViewSet.as_view({
    'get': 'decode_token'
})

##router.register(r'users', UserViewSet, base_name='usuario')

urlpatterns = [
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^users/account/$', user_active_account, name='decode-token'),
]
