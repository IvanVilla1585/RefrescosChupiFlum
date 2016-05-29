from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Usuarios/$', views.UsuarioView, name='usuario'),
    url(r'^Usuario/Guardar/$', views.CrearUsuario.as_view(), name='crear'),
    ##url(r'^MenuPrincipal/Proveedor/Actualizar', views.ActualizarProveedor.as_view(), name='actualizar'),
    ##url(r'^MenuPrincipal/Proveedor/Consultar/(?P<nit>[\w\-]+)/$', views.ConsultarProveedor.as_view(), name='consultar'),
    ##url(r'^MenuPrincipal/Proveedor/Eliminar/(?P<nit>[\w\-]+)$', views.EliminarProveedor.as_view(), name='eliminar'),
    ##url(r'^MenuPrincipal/Proveedor/Listar', views.ListarProveedores.as_view(), name='listar'),
]
