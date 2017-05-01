from django.conf.urls import url, include
from rest_framework import routers
from unidadesmedida.views import UnidadMedidaViewSet

router = routers.DefaultRouter()
router.register(r'unidadesmedidas', UnidadMedidaViewSet, base_name='unidadmedida')

urlpatterns = [
    url(r'^', include(router.urls)),
]
