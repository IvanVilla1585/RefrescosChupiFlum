from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Usuarios/$', views.UsuarioView.as_view(), name='usuario'),
    url(r'^Usuarios/Guardar/$', views.CrearUsuario.as_view(), name='crear'),
    ##url(r'^MenuPrincipal/Proveedor/Actualizar', views.ActualizarProveedor.as_view(), name='actualizar'),
    ##url(r'^MenuPrincipal/Proveedor/Consultar/(?P<nit>[\w\-]+)/$', views.ConsultarProveedor.as_view(), name='consultar'),
    ##url(r'^MenuPrincipal/Proveedor/Eliminar/(?P<nit>[\w\-]+)$', views.EliminarProveedor.as_view(), name='eliminar'),
    url(r'^Usuarios/Listar', views.ListarUsuarios.as_view(), name='listar'),
]
