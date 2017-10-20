from django.conf.urls import url, include
from rest_framework import routers
from .views import ProveedoresViewSet

router = routers.DefaultRouter()
router.register(r'proveedores', ProveedoresViewSet, base_name='proveedores')

urlpatterns = [
    url(r'^', include(router.urls)),
]