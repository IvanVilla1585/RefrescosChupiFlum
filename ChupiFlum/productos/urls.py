from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^Productos/$', views.ProductoTerminadoView.as_view(), name='producto'),
    url(r'^Productos/Guardar/$', views.CrearProducto.as_view(), name='crear'),
    url(r'^Productos/Actualizar/(?P<id>[0-9]+)/$', views.ModificarProducto.as_view(), name='actualizar'),
    url(r'^Productos/Consultar/(?P<id>[\w\-]+)/$', views.ConsultarProducto.as_view(), name='consultar'),
    url(r'^Productos/Eliminar/$', views.ActualizarEstadoView.as_view(), name='eliminar'),
    url(r'^Productos/Listar/$', views.ListarProductos.as_view(), name='listar'),
    url(r'^Productos/ConsultarFormula/$', views.ConsultarFormula.as_view(), name='consultarFormula'),
]
