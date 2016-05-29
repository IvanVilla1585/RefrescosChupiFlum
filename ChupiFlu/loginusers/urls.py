from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.authentication, name = 'login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^MenuPrincipal/$', views.menuView, name = 'menu'),
]
