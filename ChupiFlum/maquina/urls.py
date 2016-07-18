from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Maquina/$', views.MaquinaView.as_view(), name = 'maquinaForm'),
    url(r'^Maquina/Guardar$', views.CrearMaquina.as_view(), name = 'crear'),
    url(r'^Maquina/Consultar/(?P<nombre>[\w\-]+)/$', views.ConsultarMaquina.as_view(), name = 'consultar'),
    url(r'^Maquina/Actualizar/(?P<pk>[0-9]+)/$', views.ModificarMaquina.as_view(), name = 'modificar'),
    url(r'^Maquina/Listar$', views.ListarMaquinas.as_view(), name = 'listar'),
]
