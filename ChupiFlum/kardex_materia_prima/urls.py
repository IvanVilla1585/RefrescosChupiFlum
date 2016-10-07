from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^KardexMateriaPrima/$', views.KardexMateriaPrimaView.as_view(), name = 'form'),
    url(r'^KardexMateriaPrima/Crear/$', views.CrearKardexMateriaPrima.as_view(), name = 'crear'),
]
