"""ChupiFlum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ##url(r'^materiaprima-autocomplete/$', MateriaPrimaAutocomplete.as_view(), name='materiaprima-autocomplete'),
    url(r'^MenuPrincipal/', include('proveedores.urls', namespace="proveedores")),
    url(r'^MenuPrincipal/', include('userprofiles.urls', namespace="usuarios")),
    ##url(r'^MenuPrincipal/', include('grupos.urls', namespace="grupos")),
    url(r'^MenuPrincipal/', include('maquina.urls', namespace="maquinas")),
    url(r'^MenuPrincipal/', include('materiaprima.urls', namespace="materiaprim")),
    url(r'^MenuPrincipal/', include('pedido.urls', namespace="pedidos")),
    url(r'^MenuPrincipal/', include('productos.urls', namespace="productos")),
    url(r'^MenuPrincipal/', include('kardex_materia_prima.urls', namespace="kardexmateria")),
    ##url(r'^MenuPrincipal/', include('unidadesmedida.urls', namespace="unidades")),
    url(r'^api/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include('loginusers.urls', namespace='api_login')),
    url(r'^api/', include('permisos.urls', namespace='api_permisos')),
    url(r'^api/', include('grupos.urls', namespace='api_grupos')),
    url(r'^api/', include('unidadesmedida.urls', namespace='api_unidades')),
    url(r'^api/', include('maquina.urls', namespace='api_maquinas')),
    url(r'^api/', include('proceso.urls', namespace='api_procesos')),
]
