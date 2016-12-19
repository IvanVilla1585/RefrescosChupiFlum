from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Usuarios/$', views.UsuarioView.as_view(), name='usuario'),
    url(r'^Usuarios/Guardar/$', views.CrearUsuario.as_view(), name='crear'),
    url(r'^Usuarios/Actualizar', views.ActualizarUsuario.as_view(), name='actualizar'),
    url(r'^Usuarios/Consultar/(?P<id>[0-9]+)/$', views.ConsultarUsuario.as_view(), name='consultar'),
    ##url(r'^Usuarios/Eliminar/(?P<id>[0-9]+)$', views.EliminarUsuario.as_view(), name='eliminar'),
    url(r'^Usuarios/Listar', views.ListarUsuarios.as_view(), name='listar'),
]
