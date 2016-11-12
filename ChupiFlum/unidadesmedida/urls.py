from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^UnidadMedida/$', views.UnidadMedidaView.as_view(), name = 'unidadForm'),
    url(r'^UnidadMedida/Guardar$', views.CrearUnidadMedida.as_view(), name = 'crear'),
    url(r'^UnidadMedida/Consultar/(?P<pk>[0-9]+)/$', views.ConsultarUnidadMedida.as_view(), name = 'consultar'),
    url(r'^UnidadMedida/Actualizar/(?P<pk>[0-9]+)/$', views.ModificarUnidadMedida.as_view(), name = 'modificar'),
    url(r'^UnidadMedida/Eliminar/$', views.ActualizarEstadoView.as_view(), name='eliminar'),
    url(r'^UnidadMedida/Listar/$', views.ListarUnidadMedidas.as_view(), name = 'listar'),
]
