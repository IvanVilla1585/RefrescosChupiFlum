from django.conf.urls import url, include
from rest_framework import routers
from .views import MaquinaViewSet

router = routers.DefaultRouter()
router.register(r'maquinas', MaquinaViewSet, base_name='maquina')

urlpatterns = [
    url(r'^', include(router.urls)),
]
