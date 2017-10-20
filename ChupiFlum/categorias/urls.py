from django.conf.urls import url, include
from rest_framework import routers
from .views import CategoriaViewSet

router = routers.DefaultRouter()
router.register(r'categoria', CategoriaViewSet, base_name='categoria')

urlpatterns = [
    url(r'^', include(router.urls)),
]
