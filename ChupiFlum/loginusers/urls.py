from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name = 'login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^MenuPrincipal/$', views.menuView, name = 'menu'),
    url(r'^$', views.homeView, name = 'home'),
]
