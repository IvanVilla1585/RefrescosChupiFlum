from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^MateriaPrima/$', views.MateriaPrimaView.as_view(), name = 'materiaPrimaForm'),
    url(r'^MateriaPrima/Crear/$', views.CrearMateriaPrima.as_view(), name = 'crear'),
    url(r'^MateriaPrima/Consultar/(?P<id>[0-9]+)/$', views.ConsultarMateriaPrima.as_view(), name = 'consultar'),
    url(r'^MateriaPrima/Modificar/(?P<id>[0-9]+)/$', views.ModificarMateriaPrima.as_view(), name = 'modificar'),
    url(r'^MateriaPrima/Eliminar/$', views.ActualizarEstadoView.as_view(), name = 'eliminar'),
    url(r'^MateriaPrima/Listar/$', views.ListarMateriaPrima.as_view(), name = 'listar'),
]
