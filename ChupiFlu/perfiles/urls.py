from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.listarPerfiles, name = 'heloword'),
    url(r'^perfil/', views.perfil, name = 'perfil'),
    url(r'^perfil/guardar', views.guardar, name = 'perfil'),
]
