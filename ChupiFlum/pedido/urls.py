from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Pedidos/$', views.PedidoView.as_view(), name = 'pedidosForm'),
    url(r'^Pedidos/Guardar/$', views.CrearPedido.as_view(), name = 'crear'),
    url(r'^Pedidos/Consultar/(?P<id>[0-9]+)/$', views.ConsultarPedido.as_view(), name = 'consultar'),
    url(r'^Pedidos/ConsultarValor/(?P<id>[0-9]+)/$', views.ConsultarValorMateria.as_view(), name = 'consultarValor'),
    url(r'^Pedidos/Modificar/(?P<id>[0-9]+)/$', views.ModificarPedido.as_view(), name = 'modificar'),
    url(r'^Pedidos/Eliminar/$', views.EliminarPedido.as_view(), name = 'eliminar'),
    url(r'^Pedidos/Listar/$', views.ListarPedido.as_view(), name = 'listar'),
    url(r'^Pedidos/ReportePedidosPDF/$', views.ReportePedidosPDF.as_view(), name = 'reporte_pdf'),
]
