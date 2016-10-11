from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Pedidos/$', views.PedidoView.as_view(), name = 'pedidosForm'),
    url(r'^Pedidos/Guardar$', views.CrearPedido.as_view(), name = 'crear'),
    url(r'^Pedidos/Listar$', views.ListarPedido.as_view(), name = 'listar'),
]
