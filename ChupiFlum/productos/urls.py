from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Productos/$', views.ProductoTerminadoView.as_view(), name='producto'),
    url(r'^Productos/Guardar/$', views.CrearProducto.as_view(), name='crear'),
    url(r'^Productos/Actualizar/(?P<pk>[0-9]+)/$', views.ModificarProducto.as_view(), name='actualizar'),
    url(r'^Productos/Consultar/(?P<nombre>[\w\-]+)/$', views.ConsultarProducto.as_view(), name='consultar'),
    url(r'^Productos/Eliminar/(?P<nombre>[\w\-]+)$', views.EliminarProducto.as_view(), name='eliminar'),
    url(r'^Productos/Listar/$', views.ListarProductos.as_view(), name='listar'),
]
